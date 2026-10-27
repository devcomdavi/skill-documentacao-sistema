#!/usr/bin/env python3
"""Audita a defasagem entre documentacao e codigo usando o historico do git.

Le docs/.docmap.json (mapa doc -> arquivos/globs de codigo que o originaram) e compara
a data do ultimo commit de cada documento com a do ultimo commit das suas fontes.

Uso:
    python doc_audit.py --repo .                     # relatorio completo
    python doc_audit.py --repo . --somente-defasados # so o que precisa de atencao
    python doc_audit.py --repo . --json              # saida para consumo programatico

Sem dependencias externas: apenas stdlib + git no PATH.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    resultado = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
    )
    return resultado.stdout.strip()


def ultimo_commit(repo: Path, caminhos) -> tuple:
    """Retorna (timestamp_unix, hash_curto, assunto) do ultimo commit que tocou os caminhos."""
    caminhos = [c for c in caminhos if c]
    if not caminhos:
        return (0, "", "")
    saida = git(repo, "log", "-1", "--format=%ct|%h|%s", "--", *caminhos)
    if not saida or "|" not in saida:
        return (0, "", "")
    ts, sha, assunto = saida.split("|", 2)
    return (int(ts), sha, assunto)


def expandir(repo: Path, padrao: str) -> list:
    """Expande um glob em caminhos existentes rastreados pelo git."""
    p = repo / padrao
    if p.exists():
        return [padrao]
    encontrados = [
        str(caminho.relative_to(repo))
        for caminho in repo.glob(padrao)
        if caminho.is_file()
    ]
    return encontrados or [padrao]


def formatar(ts: int) -> str:
    if not ts:
        return "sem histórico"
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def auditar(repo: Path, caminho_mapa: Path) -> list:
    mapa = json.loads(caminho_mapa.read_text(encoding="utf-8"))
    resultados = []

    for item in mapa.get("mapeamentos", []):
        doc = item["doc"]
        fontes = item.get("fontes", [])

        doc_ts, doc_sha, _ = ultimo_commit(repo, [doc])

        fontes_expandidas = []
        for padrao in fontes:
            fontes_expandidas.extend(expandir(repo, padrao))

        src_ts, src_sha, src_assunto = ultimo_commit(repo, fontes_expandidas)

        if not (repo / doc).exists():
            situacao = "AUSENTE"
        elif not doc_ts:
            situacao = "NAO_VERSIONADO"
        elif src_ts > doc_ts:
            situacao = "DEFASADO"
        else:
            situacao = "OK"

        dias = int((src_ts - doc_ts) / 86400) if situacao == "DEFASADO" else 0

        resultados.append({
            "doc": doc,
            "situacao": situacao,
            "doc_atualizado_em": formatar(doc_ts),
            "codigo_atualizado_em": formatar(src_ts),
            "dias_de_atraso": dias,
            "ultimo_commit_codigo": f"{src_sha} {src_assunto}".strip(),
            "fontes": fontes,
            "descricao": item.get("descricao", ""),
        })

    ordem = {"AUSENTE": 0, "DEFASADO": 1, "NAO_VERSIONADO": 2, "OK": 3}
    resultados.sort(key=lambda r: (ordem[r["situacao"]], -r["dias_de_atraso"]))
    return resultados


def imprimir(resultados: list, somente_defasados: bool) -> None:
    icones = {"OK": "ok  ", "DEFASADO": "!!  ", "AUSENTE": "XX  ", "NAO_VERSIONADO": "??  "}
    problemas = [r for r in resultados if r["situacao"] != "OK"]
    mostrar = problemas if somente_defasados else resultados

    if not mostrar:
        print("Documentação em dia com o código.")
        return

    print(f"{'':4}{'DOCUMENTO':<52} {'DOC':<13} {'CÓDIGO':<12} ATRASO")
    print("-" * 96)
    for r in mostrar:
        atraso = f"{r['dias_de_atraso']}d" if r["dias_de_atraso"] else "-"
        print(
            f"{icones[r['situacao']]}{r['doc']:<52} "
            f"{r['doc_atualizado_em']:<13} {r['codigo_atualizado_em']:<12} {atraso}"
        )
        if r["situacao"] == "DEFASADO" and r["ultimo_commit_codigo"]:
            print(f"{'':4}  └ código mudou em: {r['ultimo_commit_codigo']}")

    print("-" * 96)
    print(
        f"{len(resultados)} documentos mapeados · "
        f"{sum(1 for r in resultados if r['situacao'] == 'DEFASADO')} defasados · "
        f"{sum(1 for r in resultados if r['situacao'] == 'AUSENTE')} ausentes"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita defasagem entre docs e código.")
    parser.add_argument("--repo", default=".", help="raiz do repositório git")
    parser.add_argument("--mapa", default=None, help="caminho do .docmap.json")
    parser.add_argument("--somente-defasados", action="store_true")
    parser.add_argument("--json", action="store_true", help="saída em JSON")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    caminho_mapa = Path(args.mapa) if args.mapa else repo / "docs" / ".docmap.json"

    if not (repo / ".git").exists():
        print(f"erro: {repo} não parece ser um repositório git", file=sys.stderr)
        return 2
    if not caminho_mapa.exists():
        print(
            f"erro: {caminho_mapa} não encontrado.\n"
            "Crie-o a partir de assets/templates/docmap.json ao gerar a documentação.",
            file=sys.stderr,
        )
        return 2

    if git(repo, "rev-parse", "--is-shallow-repository") == "true":
        print(
            "aviso: clone raso (shallow). As datas de commit podem estar erradas; "
            "rode `git fetch --depth=1000` ou `git fetch --unshallow` antes de confiar no resultado.",
            file=sys.stderr,
        )

    resultados = auditar(repo, caminho_mapa)

    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        imprimir(resultados, args.somente_defasados)

    return 1 if any(r["situacao"] != "OK" for r in resultados) else 0


if __name__ == "__main__":
    sys.exit(main())
