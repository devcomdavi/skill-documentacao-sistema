#!/usr/bin/env python3
"""Verifica a consistência dos identificadores da documentação.

Confere mecanicamente as convenções da skill:
  - RF, RNF e NR compartilham uma sequência única (o mesmo número não pode aparecer em dois tipos);
  - nenhum identificador é definido duas vezes;
  - toda referência (RF001, UC3, RN2, MSG04, ADR-0007) aponta para algo definido;
  - formatos corretos (RF com 3 ou 4 dígitos, UC/RN sem zero à esquerda, ADR com 4 dígitos);
  - todo RF ativo cita ao menos um caso de uso.

Onde cada tipo é considerado DEFINIDO:
  RF/RNF/NR  `**[RF001]**` no documento de requisitos, ou linha de tabela `| RF012 |` (ex.: deprecados)
  UC         arquivo `uc<n>-*.md` ou título `# UC<n>`
  RN         título `## RN<n>`
  MSG        linha de tabela `| MSG01 |`
  ADR        arquivo `adr-<nnnn>-*.md`

Uso:
    python check_ids.py docs/
    python check_ids.py docs/ --json

Código de saída 1 se houver erro. Avisos não alteram o código de saída. Sem dependências externas.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

RE_DEF_REQ = re.compile(r"\*\*\[(RF|RNF|NR)(\d{3,4})\]\*\*")
RE_DEF_REQ_TABELA = re.compile(r"^\|\s*(RF|RNF|NR)(\d{3,4})\s*\|", re.M)
RE_DEF_UC_TITULO = re.compile(r"^#\s+UC(\d+)\b", re.M)
RE_DEF_RN = re.compile(r"^#{2,4}\s+RN(\d+)\b", re.M)
RE_DEF_MSG = re.compile(r"^\|\s*MSG(\d+)\s*\|", re.M)

RE_REF = re.compile(r"(?<![\w-])(RF|RNF|NR|UC|RN|MSG)(\d+)(?![\w])|(?<![\w-])ADR-(\d+)(?![\w])")
RE_FORMATO_RUIM = re.compile(r"(?<![\w-])(RF|RNF|NR|UC|RN|MSG)-\d+|(?<![\w-])(RF|RNF|NR)\d{1,2}(?!\w)|(?<![\w-])(UC|RN)0\d+(?!\w)")
RE_CERCA = re.compile(r"^```.*?^```", re.M | re.S)


def chave(tipo, num):
    if tipo in ("RF", "RNF", "NR"):
        return f"{tipo}{int(num):03d}"
    if tipo == "ADR":
        return f"ADR-{int(num):04d}"
    if tipo == "MSG":
        return f"MSG{int(num):02d}"
    return f"{tipo}{int(num)}"


def linha_de(texto, pos):
    return texto.count("\n", 0, pos) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docs", nargs="?", default="docs")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    raiz = Path(a.docs)
    if not raiz.is_dir():
        print(f"erro: {raiz} não é um diretório", file=sys.stderr)
        return 2

    arquivos = sorted(p for p in raiz.rglob("*.md"))
    definidos = defaultdict(list)          # chave -> [(arquivo, linha)]
    numeros_req = defaultdict(set)         # número -> {tipos}
    referencias = []                       # (chave, arquivo, linha)
    erros, avisos = [], []
    blocos_rf = {}                         # chave RF -> texto do bloco

    for arq in arquivos:
        rel = str(arq)
        texto = arq.read_text(encoding="utf-8", errors="replace")
        sem_codigo = RE_CERCA.sub(lambda m: "\n" * m.group(0).count("\n"), texto)

        m = re.match(r"uc(\d+)-", arq.name, re.I)
        if m:
            definidos[f"UC{int(m.group(1))}"].append((rel, 1))
        m = re.match(r"adr-(\d+)-", arq.name, re.I)
        if m:
            if len(m.group(1)) != 4:
                avisos.append(f"{rel}: ADR deve ter 4 dígitos no nome do arquivo (adr-0001-...)")
            definidos[f"ADR-{int(m.group(1)):04d}"].append((rel, 1))

        defs_req = list(RE_DEF_REQ.finditer(sem_codigo))
        for i, d in enumerate(defs_req):
            k = chave(d.group(1), d.group(2))
            definidos[k].append((rel, linha_de(sem_codigo, d.start())))
            numeros_req[int(d.group(2))].add(d.group(1))
            if d.group(1) == "RF":
                fim = defs_req[i + 1].start() if i + 1 < len(defs_req) else len(sem_codigo)
                proximo_titulo = re.search(r"^#{1,3}\s", sem_codigo[d.end():fim], re.M)
                if proximo_titulo:
                    fim = d.end() + proximo_titulo.start()
                blocos_rf[k] = (rel, linha_de(sem_codigo, d.start()), sem_codigo[d.start():fim])
        for d in RE_DEF_REQ_TABELA.finditer(sem_codigo):
            k = chave(d.group(1), d.group(2))
            if k not in definidos:
                definidos[k].append((rel, linha_de(sem_codigo, d.start())))
                numeros_req[int(d.group(2))].add(d.group(1))
        for rx, tipo in ((RE_DEF_UC_TITULO, "UC"), (RE_DEF_RN, "RN"), (RE_DEF_MSG, "MSG")):
            for d in rx.finditer(sem_codigo):
                k = chave(tipo, d.group(1))
                if tipo == "UC" and any(f == rel for f, _ in definidos[k]):
                    continue  # mesmo arquivo uc<n>-*.md com título # UC<n>
                definidos[k].append((rel, linha_de(sem_codigo, d.start())))

        for r in RE_REF.finditer(sem_codigo):
            k = chave("ADR", r.group(3)) if r.group(3) else chave(r.group(1), r.group(2))
            referencias.append((k, rel, linha_de(sem_codigo, r.start())))
        for f in RE_FORMATO_RUIM.finditer(sem_codigo):
            avisos.append(f"{rel}:{linha_de(sem_codigo, f.start())}: formato fora do padrão '{f.group(0)}' "
                          "(use RF001, RNF014, NR002, UC1, RN1, MSG01, ADR-0001)")

    # 1. definição duplicada
    for k, locais in definidos.items():
        unicos = sorted(set(locais))
        if len(unicos) > 1:
            erros.append(f"{k} definido mais de uma vez: " + ", ".join(f"{a}:{l}" for a, l in unicos))
    # 2. número compartilhado entre RF/RNF/NR
    for n, tipos in sorted(numeros_req.items()):
        if len(tipos) > 1:
            erros.append(f"número {n:03d} usado por mais de um tipo ({', '.join(sorted(tipos))}): "
                         "RF, RNF e NR compartilham uma sequência única")
    # 3. referência sem definição
    vistos = set()
    for k, arq, ln in referencias:
        if k not in definidos and (k, arq) not in vistos:
            vistos.add((k, arq))
            erros.append(f"{arq}:{ln}: referência a {k}, que não está definido")
    # 4. RF sem caso de uso
    for k, (arq, ln, bloco) in sorted(blocos_rf.items()):
        if "DEPRECADO" in bloco.upper():
            continue
        if not re.search(r"(?<![\w-])UC\d+", bloco):
            avisos.append(f"{arq}:{ln}: {k} não cita nenhum caso de uso (rastreabilidade RF → UC)")
    # 5. lacunas na sequência (informativo)
    if numeros_req:
        faltando = [n for n in range(1, max(numeros_req) + 1) if n not in numeros_req]
        if faltando:
            avisos.append("números sem requisito na sequência RF/RNF/NR: "
                          + ", ".join(f"{n:03d}" for n in faltando[:20])
                          + (" ..." if len(faltando) > 20 else "")
                          + " (se foram removidos, registre como deprecados em vez de apagar)")

    resumo = defaultdict(int)
    for k in definidos:
        resumo[re.match(r"[A-Z]+", k).group(0)] += 1
    if a.json:
        print(json.dumps({"definidos": dict(resumo), "erros": erros, "avisos": avisos}, ensure_ascii=False, indent=2))
    else:
        print("Identificadores definidos: " + (", ".join(f"{t}={n}" for t, n in sorted(resumo.items())) or "nenhum"))
        for e in erros:
            print(f"ERRO   {e}")
        for w in avisos:
            print(f"aviso  {w}")
        print(f"{len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
