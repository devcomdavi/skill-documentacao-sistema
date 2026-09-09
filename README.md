# Skill: documentacao-sistema

Elicitação de requisitos e documentação de sistemas para Claude Code, seguindo o
encadeamento clássico da Engenharia de Software em português:

```
Elicitação → DVP → Documento de Requisitos → Visão de Casos de Uso → Visão Lógica → Código
```

## Instalação

**Uso pessoal (todos os seus projetos):**
```bash
cp -r documentacao-sistema ~/.claude/skills/
```

**Uso em um projeto (versionada com o time):**
```bash
mkdir -p .claude/skills && cp -r documentacao-sistema .claude/skills/
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
| Auditoria | "Roda o doc_audit e me mostra o que está defasado" |

## Convenções adotadas

- **Identificadores** `RF001`, `RNF014`, `NR002` em sequência numérica única entre os três
  tipos; `UC1`, `RN1`, `MSG01`, `ADR-0001`.
- **Requisito funcional em forma de história de usuário**: "Como um \<papel\>, eu gostaria
  de \<ação\>, para que \<benefício\>".
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

## Estrutura

```
documentacao-sistema/
├── SKILL.md                          # fluxo principal, 3 modos de trabalho
├── references/
│   ├── elicitacao.md                 # entrevistas, armadilhas de pergunta, DVP
│   ├── extracao.md                   # heurísticas substantivo→classe, verbo→método
│   ├── diagramas.md                  # sintaxe Mermaid/PlantUML de cada diagrama
│   ├── visoes-arquiteturais.md       # visão de casos de uso, lógica e demais
│   └── engenharia-reversa.md         # extrair documentação de código existente
├── assets/templates/                 # DVP, requisitos, caso de uso, RN, mensagens, ADR…
└── scripts/
    ├── doc_audit.py                  # acha documentação defasada via git
    └── check_mermaid.py              # valida diagramas antes de entregar
```

## Ajustes recomendados

- Se seu time usa outra estrutura de pastas, edite "Estrutura de saída padrão" no `SKILL.md`.
- Se precisa de PlantUML em todos os diagramas (exigência acadêmica), inverta o padrão na
  seção "Diagramas" do `SKILL.md`.
- Adicione `check_mermaid.py` ao pre-commit para não subir diagrama quebrado.

## Créditos

A metodologia, as convenções de identificação e as heurísticas de extração seguem o
material de Engenharia de Software de **Maxwell Anderson** (IFPB), licenciado sob
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):
<https://maxwellamaral.github.io/lessons/softeng/>

Por ser derivada de material CC BY-SA, esta skill é distribuída sob a mesma licença.
