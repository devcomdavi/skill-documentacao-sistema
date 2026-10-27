# Skill: documentacao-sistema

Elicitação de requisitos e documentação de sistemas para Claude Code e outros agentes de
código, seguindo o encadeamento clássico da Engenharia de Software em português:

```
Elicitação → DVP → Documento de Requisitos → Visão de Casos de Uso → Visão Lógica → Código
```

Faz parte de uma sequência de skills para construir sistemas **legais, documentados e
funcionais**:

| Skill | Foco |
|---|---|
| [seguranca-lgpd-vibecode](https://github.com/devcomdavi/seguranca-lgpd-vibecode) | Segurança da informação e LGPD |
| **documentacao-sistema** (esta) | Requisitos, casos de uso, visões e decisões |

As skills compartilham a mesma pasta `docs/` e os mesmos identificadores (a de segurança
mantém `docs/07-seguranca-privacidade/`).

## Instalação

**Uso pessoal (todos os seus projetos):**
```bash
git clone https://github.com/devcomdavi/claude-skill-documentacao-sistema ~/.claude/skills/documentacao-sistema
```

**Uso em um projeto (versionada com o time):**
```bash
git clone https://github.com/devcomdavi/claude-skill-documentacao-sistema .claude/skills/documentacao-sistema
rm -rf .claude/skills/documentacao-sistema/.git
git add .claude/skills && git commit -m "chore: skill de documentação"
```

Verifique com `/skills` dentro do Claude Code. A skill é *model-invoked*: o Claude decide
usá-la sozinho quando o pedido combina com a `description`. Também dá para forçar com
`/documentacao-sistema`.

## Como usar

| Situação | O que dizer |
|---|---|
| Projeto novo | "Vamos fazer o pré-projeto de um sistema de controle de garantias — me ajuda na elicitação" |
| Projeto sem documentação | "Este repositório não tem documentação. Documenta ele: DVP, requisitos, casos de uso e visão lógica" |
| Após implementar | "Atualiza a documentação com o que mudou nesta branch" |
| Auditoria | "Roda o doc_audit e o check_ids e me mostra o que está defasado ou quebrado" |

## Convenções adotadas

- **Identificadores** `RF001`, `RNF014`, `NR002` em sequência numérica única entre os três
  tipos; `UC1`, `RN1`, `MSG01`, `ADR-0001`. Citados também em testes, commits e PRs.
- **Requisito funcional em forma de história de usuário**: "Como um \<papel\>, eu gostaria
  de \<ação\>, para que \<benefício\>", com **critérios de aceitação** Dado/Quando/Então.
- **Atributos**: prioridade (Essencial/Importante/Desejável), complexidade, risco,
  requisitos vinculados.
- **RNF em nove categorias**: disponibilidade, privacidade e segurança, usabilidade,
  suportabilidade, interoperabilidade, manutenibilidade, desempenho, implementação,
  implantação.
- **Casos de uso** com verbo no infinitivo; CRUD colapsado em "Manter X"; especificação
  descritiva com fluxos alternativos `A1`, `A2` e exceções apontando para `RN`.
- **Uma técnica de detalhamento por caso de uso** — nunca especificação e diagrama de
  atividades para o mesmo UC.
- **Heurísticas de extração**: substantivos → atores e classes; verbos → casos de uso e
  métodos.
- **Contrato de API** gerado do código (OpenAPI), nunca reescrito à mão.
- **Documentação como contexto para agentes**: o `CLAUDE.md`/`AGENTS.md` do projeto aponta
  para `docs/`.

## Estrutura

```
SKILL.md                              # fluxo principal, 3 modos de trabalho
references/
├── elicitacao.md                     # entrevistas, armadilhas de pergunta, DVP
├── extracao.md                       # heurísticas substantivo→classe, verbo→método
├── diagramas.md                      # sintaxe Mermaid/PlantUML de cada diagrama
├── visoes-arquiteturais.md           # visão de casos de uso, lógica e demais
└── engenharia-reversa.md             # extrair documentação de código existente
assets/templates/                     # DVP, requisitos, caso de uso, RN, mensagens, ADR,
                                      # índice, docmap e trecho para CLAUDE.md/AGENTS.md
scripts/
├── doc_audit.py                      # acha documentação defasada via git
├── check_ids.py                      # identificadores: sequência, duplicatas, referências quebradas
└── check_mermaid.py                  # valida diagramas (--estrito usa o Mermaid CLI)
```

Os scripts usam só a biblioteca padrão do Python 3 e o git. O modo `--estrito` do
`check_mermaid.py` precisa do Mermaid CLI (`npm install -g @mermaid-js/mermaid-cli`).

## Ajustes recomendados

- Se seu time usa outra estrutura de pastas, edite "Estrutura de saída padrão" no `SKILL.md`.
- Se precisa de PlantUML em todos os diagramas (exigência acadêmica), inverta o padrão na
  seção "Diagramas" do `SKILL.md`.
- Adicione `check_mermaid.py` e `check_ids.py` ao pre-commit ou ao CI para não subir
  diagrama quebrado nem referência a requisito inexistente.

## Créditos e licença

A metodologia, as convenções de identificação e as heurísticas de extração seguem o
material de Engenharia de Software de **Maxwell Anderson** (IFPB), licenciado sob
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):
<https://maxwellamaral.github.io/lessons/softeng/>

Por ser derivada de material CC BY-SA, esta skill é distribuída sob a mesma licença
([LICENSE](LICENSE)).
