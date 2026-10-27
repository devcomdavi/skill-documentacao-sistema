---
name: skill-documentacao-sistema
description: Elicitação de requisitos e documentação de sistemas pela metodologia clássica de Engenharia de Software, em português — Documento de Visão do Produto (DVP), Documento de Requisitos com RF/RNF/NR, critérios de aceitação e matriz de rastreabilidade, Visão de Casos de Uso (diagrama UML + especificação descritiva de UCs), Visão Lógica (extração de classes e métodos), diagramas UML, ADRs e contrato de API. Use sempre que o usuário falar em elicitação/levantamento de requisitos, documento de visão, DVP, requisitos funcionais e não funcionais, casos de uso, diagrama de casos de uso, UML, visão lógica, visão de casos de uso, modelo de domínio, diagrama de classes, glossário, "pré-projeto", "meu projeto não tem documentação", ou quando pedir para atualizar a documentação após uma implementação. Use também de forma proativa ao final de mudanças estruturais no código (nova entidade, novo endpoint, nova integração, mudança de arquitetura).
---

# Documentação de Sistema

Skill para conduzir elicitação de requisitos e produzir/manter a documentação de um sistema
seguindo o encadeamento clássico da Engenharia de Software:

```
Elicitação → DVP → Documento de Requisitos → Visão de Casos de Uso → Visão Lógica → Código
```

Cada etapa é **derivada** da anterior por heurísticas explícitas (substantivos viram atores
e classes; verbos viram casos de uso e métodos). Isso não é burocracia: é o que garante
que nenhum requisito se perca no caminho e que cada classe tenha uma justificativa
rastreável até uma necessidade do cliente.

## Princípios

**Faça somente o que for útil.** Não gere um artefato por simetria. Se uma história de
usuário já descreve as etapas de um caso de uso, não faça também um diagrama de atividades
para o mesmo caso — duas representações da mesma coisa criam inconsistência assim que uma
das duas for alterada e a outra não. Escolha uma.

**Nunca invente.** O que foi confirmado pelo usuário ou lido do código é fato; o resto é
marcado com `⚠️ A CONFIRMAR`. Se você precisou assumir mais de três coisas relevantes,
pare e pergunte.

**Tudo rastreável por identificador.** RF001, UC1, RN1, MSG01, ADR-0001. Identificador é o
que permite citar o artefato em outro documento, em teste e em mensagem de commit.

**Documentação junto do código.** Markdown com diagramas em Mermaid embutidos, versionado
em git. O `docs/.docmap.json` registra qual documento nasceu de qual parte do código, para
auditoria posterior.

**Documentação também é contexto para agentes.** Num projeto construído com agentes de
código, `docs/` é o que o próximo agente (ou a próxima sessão) lê para não reinventar regra
de negócio nem contradizer um requisito. Por isso ela precisa ser enxuta, navegável a partir
de um índice e citada no arquivo de instruções do projeto (veja "Contexto para agentes").

## Integração com as outras skills da sequência

Esta skill faz parte de uma sequência para construir sistemas **legais, documentados e
funcionais**. Elas compartilham a mesma pasta `docs/` e os mesmos identificadores:

| Skill | Responsabilidade | Ponto de contato com esta |
|---|---|---|
| `skill-seguranca-lgpd` | Segurança e conformidade com a LGPD | É dona de `docs/07-seguranca-privacidade/` (inventário de dados, modelo de ameaças, relatórios de auditoria, plano de incidentes). Os RNFs de privacidade e segurança e a restrição regulatória do DVP apontam para lá; o modelo de dados marca colunas pessoais e remete ao inventário em vez de repetir base legal e retenção. Decisões de segurança relevantes viram ADR aqui. |

Se uma dessas skills estiver instalada, delegue a ela o que é dela em vez de produzir uma
versão própria do mesmo artefato. Se não estiver, siga os templates desta skill e registre a
lacuna no `docs/README.md`.

## Passo 0 — Identificar o modo de trabalho

| Modo | Situação | Vá para |
|---|---|---|
| **A — Pré-projeto** | Sistema ainda não existe. O usuário tem uma ideia/necessidade. | [Modo A](#modo-a--pré-projeto) |
| **B — Engenharia reversa** | Código existe, documentação não (ou está morta). | [Modo B](#modo-b--documentar-sistema-existente) |
| **C — Manutenção** | Documentação existe e o código mudou. | [Modo C](#modo-c--manter-a-documentação-viva) |

Se não estiver óbvio, olhe o repositório (existe código? existe `docs/`?) e confirme com o
usuário em uma frase. Modos se combinam: é comum entrar em B e seguir em C.

## Estrutura de saída padrão

```
docs/
├── README.md                          # índice navegável
├── .docmap.json                       # rastreabilidade doc → código
├── 01-visao-produto/
│   └── dvp.md                         # Documento de Visão do Produto
├── 02-requisitos/
│   ├── requisitos.md                  # Documento de Requisitos (RF, RNF, NR, matriz)
│   ├── glossario.md                   # definições, acrônimos e abreviações
│   ├── regras-de-negocio.md           # RN1, RN2...
│   └── mensagens.md                   # MSG01, MSG02...
├── 03-visao-casos-de-uso/
│   ├── visao-de-casos-de-uso.md       # diagrama geral + lista de atores e UCs
│   └── uc1-<nome>.md                  # especificação descritiva, um arquivo por UC
├── 04-visao-logica/
│   ├── visao-logica.md                # extração de classes/métodos + diagrama de classes
│   └── modelo-de-dados.md             # ER e dicionário de dados
├── 05-outras-visoes/
│   ├── visao-de-processos.md
│   ├── visao-de-implementacao.md
│   ├── visao-de-implantacao.md
│   └── contrato-api.md                # quando há API HTTP: aponta para a especificação OpenAPI
├── 06-decisoes/
│   └── adr-0001-<titulo>.md
└── 07-seguranca-privacidade/          # mantida pela skill skill-seguranca-lgpd
    ├── inventario-dados.md            # registro das operações de tratamento (LGPD, art. 37)
    ├── modelo-de-ameacas.md
    ├── plano-resposta-incidentes.md
    └── auditorias/AAAA-MM-DD.md
```

Se o projeto já tiver convenção própria de documentação, respeite-a em vez de impor esta.
Seções sem conteúdo não devem existir — registre a omissão e o motivo no `docs/README.md`.

---

## Modo A — Pré-projeto

### A.1 Elicitação

Entreviste em rodadas curtas (no máximo 5 perguntas por vez) e devolva um rascunho a cada
rodada. Corrigir é mais fácil que criar: o usuário aponta um erro no seu resumo muito mais
rápido do que articula um requisito do zero.

Leia `references/elicitacao.md` antes da primeira rodada. Ele traz as perguntas livres de
contexto, as armadilhas de pergunta (indutivas, longas, que começam com "por quê"), e a
postura correta — você não é o especialista no domínio, o entrevistado é.

### A.2 Documento de Visão do Produto (DVP)

O DVP vem **antes** da elicitação detalhada dos requisitos, não depois. Ele dá a visão
geral do problema e das necessidades, e serve de norteador para as perguntas seguintes:
sem ele, você não sabe nem quais perguntas fazer. Suas categorias de necessidade
costumam virar os módulos do sistema.

Ele descreve o produto de forma abrangente — problema, oportunidades, benefícios,
stakeholders, funcionalidades principais e restrições — sem o detalhe da lista de
requisitos. Pode ser anexado a contrato, então cuidado com o que se escreve nele. É
artefato vivo: atualize sempre que surgir informação nova.

Template: `assets/templates/dvp.md`.

### A.3 Documento de Requisitos

A partir do DVP e das entrevistas, escreva o Documento de Requisitos.
Template: `assets/templates/requisitos.md`. Convenções obrigatórias:

**Identificação.** `RF` requisito funcional, `RNF` requisito não-funcional, `NR`
não-requisito (o que foi decidido que o sistema *não* fará). O número é uma sequência
única para todo o conjunto de tipos: se existe RF012, o próximo identificador criado —
seja RF, RNF ou NR — é 013. Formato de três ou quatro dígitos: `RF001`, `RNF014`, `NR002`.
Referencie sempre entre colchetes: `[RF001]`.

**Requisito funcional em forma de história de usuário:**

> `[RF001]` — Como um `<papel>`, eu gostaria de `<ação/capacidade>`, para que `<benefício>`.
> `<Detalhamento: dados obrigatórios, formatos, condições.>`

Essa forma amarra o requisito a um ator e a um propósito, e alimenta diretamente o
diagrama de casos de uso e os testes.

**Critérios de aceitação.** Todo RF Essencial ou Importante ganha de 2 a 5 critérios no
formato *Dado / Quando / Então*, cobrindo o caminho feliz e pelo menos uma recusa
(dado inválido, permissão negada, limite atingido). São eles que viram testes de aceitação
e que respondem, sem discussão, "a funcionalidade está pronta?". Critério que não dá para
verificar com um teste ou uma observação objetiva está mal escrito.

**Atributos de cada requisito:** requisitos vinculados (rastreabilidade), prioridade
(Essencial, Importante, Desejável), complexidade (Complexa, Alta, Média, Baixa) e risco
(Alto, Médio, Baixo).

**Requisitos não-funcionais agrupados por categoria:** Disponibilidade · Privacidade e
segurança · Usabilidade · Suportabilidade · Interoperabilidade · Manutenibilidade ·
Desempenho · Implementação · Implantação. Percorra todas as categorias na entrevista,
mesmo que algumas fiquem vazias — é assim que se descobre a exigência que ninguém
mencionou.

Em **Privacidade e segurança**, se o sistema trata dados pessoais (quase todo sistema
trata), os RNFs incluem no mínimo: controle de acesso por recurso, proteção dos dados
pessoais em trânsito e em repouso, atendimento aos direitos do titular (exportar, corrigir,
excluir) e retenção definida. O detalhamento técnico e legal fica com a skill
`skill-seguranca-lgpd`; aqui o RNF registra a exigência e como será verificada.

**Matriz de rastreabilidade RF × RNF** ao final: linhas RNF, colunas RF, `X` onde o
requisito não-funcional incide sobre o funcional. Ela revela RNF que não afeta nada
(provavelmente mal escrito) e RF crítico sem nenhuma exigência de qualidade.

O documento tem capa, histórico de revisões (data, versão, descrição, autor), sumário e
uma seção de definições, acrônimos e abreviações. Valide com o cliente antes de seguir.

### A.4 Visão de Casos de Uso

Exibe **o que** o sistema faz, do ponto de vista de quem o usa. Público: cliente,
designer, desenvolvedor e gerente de projeto — projete o diagrama para ser entendido pelo
cliente, mesmo que ele nunca venha a vê-lo. Se o diagrama só faz sentido para
desenvolvedores, ele falhou.

Derive os casos de uso dos requisitos funcionais usando as heurísticas de
`references/extracao.md` (leia antes de começar):

1. **Substantivos → atores.** Liste os substantivos de cada RF e separe quem *interage*
   com o sistema (ator) de quem é apenas *dado informado* (atributo).
2. **Verbos → casos de uso.** Liste os verbos e, para cada um, pergunte: é uma
   funcionalidade, uma etapa de uma funcionalidade maior, ou só uma condição/verbo de
   ligação? Só o primeiro caso vira caso de uso.
3. **Relacionamentos** entre atores, entre ator e UC, e entre UCs.

Convenções: caso de uso começa com **verbo no infinitivo**; um CRUD completo sobre a mesma
entidade colapsa em um único `Manter <entidade>`; identificadores `UC1`, `UC2`, sem zeros
à esquerda. Regras de negócio referenciadas nos fluxos como `[RN1]`, mensagens do sistema
como `MSG01`.

Depois do diagrama geral, detalhe cada UC. Escolha **uma** técnica por caso de uso:
especificação descritiva (tabela), história de usuário, ou diagrama de atividades — nunca
duas para o mesmo UC. A especificação descritiva usa a tabela de
`assets/templates/caso-de-uso.md`, com fluxos alternativos rotulados `A1`, `A2`, `A3` e
fluxos de exceção apontando para as regras de negócio.

Escreva os passos usando a palavra "o ator", não o nome do papel: se o ator for renomeado,
você não precisa reescrever a especificação inteira.

### A.5 Visão Lógica

Exibe **como** as funcionalidades são projetadas. Público: designers e desenvolvedores.
Modelos: diagrama de classes e de objetos para a estrutura estática; máquina de estados e
diagrama de atividades para o comportamento dinâmico. Aqui o diagrama de atividades tem
propósito diferente do que teve na visão de casos de uso: lá ele mostrava o fluxo de
eventos de um caso de uso, aqui mostra o fluxo interno de uma operação.

As classes saem das especificações de caso de uso, pela heurística de cinco passos
detalhada em `references/extracao.md`: descrição → extrair substantivos → tentativa de
classes → eliminar classes estranhas → classes identificadas. Cada substantivo é
classificado como classe, atributo de alguma classe, ou descartado.

Os métodos saem dos verbos das mesmas especificações, classificados como operação,
descartar, desnecessário ou redundante, e então nomeados.

Construa o diagrama de classes em versões: primeiro só classes e atributos, depois
relacionamentos, depois métodos. Mostre cada versão ao usuário — é mais fácil corrigir o
recorte de classes antes de os métodos estarem todos escritos.

### A.6 Demais visões e decisões

Visão de processos, de implementação e de implantação: veja
`references/visoes-arquiteturais.md`. Gere apenas as que o sistema justifica.

Toda escolha estrutural relevante (estilo arquitetural, banco, framework, estratégia de
autenticação) vira um ADR em `06-decisoes/`, template em `assets/templates/adr.md`.

**Contrato de API.** Se o sistema expõe API HTTP, a especificação OpenAPI (ou o schema
GraphQL) é a documentação dos endpoints — de preferência **gerada a partir do código**
(decoradores, schemas zod/pydantic), para não divergir. `05-outras-visoes/contrato-api.md`
só aponta para ela e registra o que a especificação não diz: autenticação exigida por grupo
de rotas, versionamento, limites de uso e a ligação endpoint → UC. Não reescreva os
endpoints à mão em Markdown: duas fontes para o mesmo contrato é a redundância que o
princípio "faça somente o que for útil" proíbe.

---

## Modo B — Documentar sistema existente

O código é a fonte da verdade; o usuário é a fonte da intenção. Você extrai a estrutura do
código e valida a intenção com ele.

Se o produto for grande, não tente cobrir tudo: atue no escopo do módulo em que o usuário
trabalha e peça ajuda a quem já conhece o sistema. Ordem de ataque recomendada:

1. **DVP** — mesmo em sistema existente, ele é o artefato norteador. Se não existir, crie;
   se existir desatualizado, atualize; se estiver mal escrito, reescreva.
2. **Glossário** do domínio — destrava a leitura de todo o resto.
3. **Documento de Requisitos** reconstruído a partir de rotas, testes e regras no código.
4. **Visão de casos de uso** do módulo mais crítico (pergunte ao usuário qual é).
5. **Visão lógica** e modelo de dados.
6. **Visão de implantação**.
7. Demais módulos, por ordem de dor.

`references/engenharia-reversa.md` traz a ordem de leitura eficiente do repositório, os
comandos úteis e a tabela de "o que no código vira qual artefato". Marque com
`⚠️ A CONFIRMAR` tudo que foi inferido e reúna as dúvidas numa lista curta e priorizada
(5 a 10 perguntas, não 40) ao final.

RNFs quase nunca estão no código. Não invente número: escreva
`⚠️ NÃO DOCUMENTADO — definir com o negócio`.

Entregue e valide cada bloco antes de seguir. Se o usuário corrigir seu entendimento do
domínio no passo 2, tudo depois disso já sai certo.

---

## Modo C — Manter a documentação viva

**Reativo:** o usuário pede. **Proativo:** você acabou de implementar algo que muda a
estrutura do sistema (nova entidade, novo endpoint, mudança de contrato, nova dependência
externa, mudança no fluxo de autenticação, alteração de esquema). Nesses casos, ao
terminar a implementação, diga o que precisa ser atualizado e ofereça atualizar — não
altere silenciosamente arquivos que o usuário não pediu para tocar.

Fluxo:

1. Descubra o delta: `git diff` desde o último commit que tocou `docs/`, ou o diff da
   branch contra a base. Com `.docmap.json` presente, rode
   `python scripts/doc_audit.py --repo <raiz>` (em clone raso, busque histórico antes:
   as datas ficam erradas sem ele).
2. Atualize **apenas** os artefatos afetados. Documentação boa tem diff pequeno.
3. Propague na direção do encadeamento: requisito novo → caso de uso → classes. Requisito
   alterado sem o UC correspondente atualizado é o começo da documentação morta.
4. Preserve identificadores. Requisito removido vira
   `[RF012] (DEPRECADO em 2026-03-01, ver RF030)`. Nunca recicle número.
5. Registre no histórico de revisões do documento (data, versão, descrição, autor).
6. Decisão estrutural nova → ADR novo. ADR aceito não é editado: crie outro com status
   "Substitui ADR-0004" e marque o antigo como "Substituído por ADR-0009".
7. Atualize o `.docmap.json`.
8. Rode `python scripts/check_ids.py docs/` e `python scripts/check_mermaid.py docs/`
   antes de entregar: referência quebrada e diagrama inválido são os dois defeitos que
   mais aparecem depois de uma atualização.

Se a deriva for grande demais (meses de atraso), pare de remendar e proponha uma passada
de Modo B no módulo afetado.

---

## Diagramas

Padrão: **Mermaid** embutido no Markdown. Use PlantUML quando o usuário pedir ou quando o
diagrama for de casos de uso — Mermaid não tem sintaxe nativa para esse tipo.
`references/diagramas.md` tem a sintaxe pronta de cada diagrama, incluindo as duas
alternativas para casos de uso.

Regras que evitam diagrama inútil:
- Um diagrama responde **uma** pergunta. Se precisa de duas, faça dois.
- Máximo ~12 elementos; acima disso, quebre por módulo ou subsistema.
- Todo diagrama acompanhado de um parágrafo dizendo o que mostra e o que omite.
- Valide a sintaxe antes de entregar: `python scripts/check_mermaid.py <arquivo ou pasta>`.
  Um bloco Mermaid inválido derruba a renderização do arquivo inteiro. Se o Mermaid CLI
  (`mmdc`) estiver instalado, use `--estrito`: ele renderiza cada bloco com o parser
  oficial e pega o que as heurísticas não pegam (como `;` dentro de nota em diagrama de
  sequência).

## Rastreabilidade

```
Necessidade no DVP → RF001 → UC1 → Classe/Método → Teste
                   ↘ RNF001 → decisão registrada em ADR-0001
```

Ligações a manter explícitas: cada UC cita os RFs que realiza e as RNs que aplica; cada RF
cita os UCs que o realizam; cada classe importante cita os UCs de que participa; cada ADR
cita os RNFs que o motivaram; a matriz RF × RNF fecha o quadro.

Os identificadores também vão para fora de `docs/`: nome ou descrição dos testes
(`test_RF001_cadastro_rejeita_preco_negativo`), mensagens de commit e descrição de PR
(`feat(UC3): ... [RF012]`). É isso que permite responder "qual teste cobre este requisito?"
e "por que este código existe?" com uma busca.

## Contexto para agentes

Ao criar ou reorganizar a documentação, garanta que o arquivo de instruções do projeto
(`CLAUDE.md`, `AGENTS.md` ou equivalente) tenha um trecho curto apontando para ela. Modelo
em `assets/templates/contexto-agente.md`. Ele diz onde está o índice, quais documentos ler
antes de cada tipo de mudança, as convenções de identificadores e a regra de atualizar a
documentação no mesmo commit da mudança estrutural. Não copie a documentação para dentro
desse arquivo: aponte para ela, senão são duas fontes para manter.

## Checklist antes de entregar

- [ ] Numeração sequencial única respeitada entre RF, RNF e NR; nenhum número reciclado
- [ ] Todo RF em forma de história de usuário, com prioridade, complexidade e risco
- [ ] RFs Essenciais e Importantes com critérios de aceitação Dado/Quando/Então
- [ ] Todo RNF dentro de uma das nove categorias e com forma de verificação
- [ ] Matriz de rastreabilidade RF × RNF preenchida
- [ ] Casos de uso com verbo no infinitivo; CRUD colapsado em "Manter X"
- [ ] Uma única técnica de detalhamento por caso de uso (sem redundância)
- [ ] Especificações escritas com "o ator", não com o nome do papel
- [ ] Mensagens do sistema centralizadas como MSG0x, não escritas soltas nos fluxos
- [ ] Diagramas com sintaxe válida e parágrafo de contexto
- [ ] Inferências marcadas com `⚠️ A CONFIRMAR` e reunidas numa lista de pendências
- [ ] Histórico de revisões e `.docmap.json` atualizados
- [ ] `check_ids.py` sem erros (nenhuma referência a identificador inexistente)
- [ ] Arquivo de instruções do projeto aponta para `docs/README.md`

## Arquivos de apoio

| Arquivo | Quando ler |
|---|---|
| `references/elicitacao.md` | Antes de entrevistar (Modo A) ou validar inferências (Modo B) |
| `references/extracao.md` | Ao derivar atores/UCs dos requisitos e classes/métodos dos UCs |
| `references/diagramas.md` | Sempre que for gerar qualquer diagrama |
| `references/visoes-arquiteturais.md` | Ao montar as visões de processos, implementação e implantação |
| `references/engenharia-reversa.md` | No Modo B, antes de explorar o repositório |
| `assets/templates/` | Ao criar cada artefato — copie e preencha |
| `scripts/doc_audit.py` | No Modo C, para achar documentação defasada |
| `scripts/check_mermaid.py` | Antes de entregar arquivos com diagramas (`--estrito` com mmdc) |
| `scripts/check_ids.py` | Antes de entregar: sequência RF/RNF/NR, duplicatas, referências quebradas, RF sem UC |

## Fontes

As convenções de identificação de requisitos, a forma de história de usuário, a
especificação descritiva de casos de uso, as heurísticas de extração de atores, casos de
uso, classes e métodos, e a definição das visões seguem o material de Engenharia de
Software de Maxwell Anderson (IFPB), licenciado sob CC BY-SA 4.0:
<https://maxwellamaral.github.io/lessons/softeng/>.
