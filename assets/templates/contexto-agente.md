<!-- Trecho para o arquivo de instruções do projeto (CLAUDE.md, AGENTS.md ou equivalente).
     Aponte para a documentação; não copie o conteúdo dela para cá. -->

## Documentação do sistema

A documentação fica em `docs/` (índice: `docs/README.md`). Antes de mudar o sistema, leia:

| Vou... | Leia antes |
|---|---|
| Implementar ou alterar funcionalidade | `docs/02-requisitos/requisitos.md` (RFs e critérios de aceitação) e a especificação do UC em `docs/03-visao-casos-de-uso/` |
| Mexer em regra de negócio | `docs/02-requisitos/regras-de-negocio.md` |
| Criar ou alterar entidade, tabela ou relacionamento | `docs/04-visao-logica/` e `docs/07-seguranca-privacidade/inventario-dados.md` |
| Criar ou alterar endpoint | `docs/05-outras-visoes/contrato-api.md` |
| Tomar decisão estrutural (biblioteca, banco, arquitetura) | `docs/06-decisoes/` (ADRs aceitos não são contrariados sem um ADR novo) |

**Identificadores:** RF001, RNF014, NR002 (sequência única), UC1, RN1, MSG01, ADR-0001.
Cite-os em nomes de teste, mensagens de commit e descrições de PR.

**Regra de atualização:** mudança estrutural (entidade, endpoint, integração, regra de
negócio, fluxo de autenticação) atualiza a documentação afetada no mesmo commit. Antes de
concluir, rode `python <skill>/scripts/check_ids.py docs/` e `python <skill>/scripts/check_mermaid.py docs/`.
