#!/usr/bin/env python3
"""Verificacao rapida de blocos Mermaid dentro de arquivos Markdown.

Nao e um parser completo do Mermaid: e uma rede de seguranca para os erros que mais
quebram a renderizacao de uma pagina inteira. Um bloco invalido derruba o diagrama e,
em alguns renderizadores, o resto do documento.

Uso:
    python check_mermaid.py docs/                 # varre recursivamente
    python check_mermaid.py docs/arquitetura.md   # arquivo unico

Codigo de saida 1 se houver erro, 0 se estiver limpo. Sem dependencias externas.
"""

import re
import sys
from pathlib import Path

TIPOS_VALIDOS = {
    "flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
    "stateDiagram-v2", "erDiagram", "journey", "gantt", "pie", "requirementDiagram",
    "gitGraph", "mindmap", "timeline", "quadrantChart", "C4Context", "C4Container",
    "C4Component", "C4Dynamic", "C4Deployment", "sankey-beta", "xychart-beta",
    "block-beta", "architecture-beta", "packet-beta", "kanban", "radar", "treemap",
}

RE_BLOCO = re.compile(r"^```mermaid\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
RE_ID_NO = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*[\[\(\{]")


def verificar_bloco(codigo: str, linha_inicial: int) -> list:
    problemas = []
    linhas = [l for l in codigo.split("\n")]
    uteis = [l for l in linhas if l.strip() and not l.strip().startswith("%%")]

    if not uteis:
        return [(linha_inicial, "bloco mermaid vazio")]

    primeira = uteis[0].strip()
    tipo = primeira.split()[0] if primeira.split() else ""
    if tipo not in TIPOS_VALIDOS:
        problemas.append(
            (linha_inicial, f"tipo de diagrama desconhecido: '{tipo}' — "
                            f"verifique a grafia (ex.: stateDiagram-v2, sequenceDiagram)")
        )

    eh_fluxo = tipo in {"flowchart", "graph"}

    for deslocamento, linha in enumerate(linhas):
        n = linha_inicial + deslocamento
        despida = linha.strip()
        if not despida or despida.startswith("%%"):
            continue

        # As checagens de sintaxe de no valem so para flowchart/graph: em classDiagram,
        # erDiagram e C4 chaves e virgulas sao sintaxe legitima.
        if eh_fluxo:
            # Parenteses/colchetes desbalanceados na linha (fora de aspas)
            fora_de_aspas = re.sub(r'"[^"]*"', "", linha)
            if not despida.startswith(("subgraph", "end")):
                for abre, fecha, nome in (
                    ("[", "]", "colchete"), ("(", ")", "parêntese"), ("{", "}", "chave"),
                ):
                    if fora_de_aspas.count(abre) != fora_de_aspas.count(fecha):
                        problemas.append(
                            (n, f"{nome} desbalanceado fora de aspas: {despida[:60]}")
                        )

            # Parenteses dentro do rotulo de um no, sem aspas: quebra o parser
            for padrao in (r"\w\[([^\"\[\]]*[()][^\"\[\]]*)\]",
                           r"\w\{([^\"{}]*[()][^\"{}]*)\}"):
                m = re.search(padrao, linha)
                if m:
                    problemas.append(
                        (n, f"parênteses no rótulo sem aspas — envolva o texto em aspas: "
                            f"{m.group(1)[:40]}")
                    )

            # 'end' usado como texto de no em flowchart
            if re.search(r"[\[\(\{]\s*end\s*[\]\)\}]", despida, re.IGNORECASE):
                problemas.append((n, "'end' como texto de nó quebra o flowchart — use 'Fim'"))

        # Id de no com acento ou espaco
        m = RE_ID_NO.match(linha)
        if m and not m.group(1).isascii():
            problemas.append(
                (n, f"id de nó com acento: '{m.group(1)}' — use ASCII no id e acentos no rótulo")
            )

        # Estado com espaco em stateDiagram
        if tipo.startswith("stateDiagram"):
            m = re.match(r"^\s*([\w ]+?)\s*-->", linha)
            if m and " " in m.group(1).strip():
                problemas.append(
                    (n, f"nome de estado com espaço: '{m.group(1).strip()}' — "
                        "use CamelCase ou 's1 : rótulo com espaço'")
                )

        # Relacionamento com espaco em erDiagram
        if tipo == "erDiagram" and ":" in despida and "--" in despida:
            rotulo = despida.split(":", 1)[1].strip()
            if " " in rotulo and '"' not in rotulo:
                problemas.append(
                    (n, f"rótulo de relação com espaço: '{rotulo[:30]}' — use underscore ou aspas")
                )

    return problemas


def verificar_arquivo(caminho: Path) -> list:
    texto = caminho.read_text(encoding="utf-8", errors="replace")

    abertos = len(re.findall(r"^```mermaid\s*$", texto, re.MULTILINE))
    blocos = RE_BLOCO.findall(texto)
    achados = []

    if abertos != len(blocos):
        achados.append((0, f"{abertos - len(blocos)} bloco(s) ```mermaid sem fechamento"))

    for m in RE_BLOCO.finditer(texto):
        linha_inicial = texto[: m.start()].count("\n") + 2
        achados.extend(verificar_bloco(m.group(1), linha_inicial))

    return achados


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    alvos = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_dir():
            alvos.extend(sorted(p.rglob("*.md")))
        elif p.exists():
            alvos.append(p)
        else:
            print(f"aviso: {p} não encontrado", file=sys.stderr)

    total_problemas = 0
    arquivos_com_diagrama = 0

    for arquivo in alvos:
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        if "```mermaid" not in texto:
            continue
        arquivos_com_diagrama += 1
        problemas = verificar_arquivo(arquivo)
        if problemas:
            print(f"\n{arquivo}")
            for linha, msg in problemas:
                local = f"linha {linha}" if linha else "arquivo"
                print(f"  {local}: {msg}")
            total_problemas += len(problemas)

    print(
        f"\n{arquivos_com_diagrama} arquivo(s) com diagramas verificados · "
        f"{total_problemas} problema(s) encontrado(s)"
    )
    return 1 if total_problemas else 0


if __name__ == "__main__":
    sys.exit(main())
