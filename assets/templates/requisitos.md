# Requisitos de Software

## \<Nome do Sistema\> (\<SIGLA\>)

Versão 1.0

---

## Histórico de revisões

| Data | Versão | Descrição | Autor |
|---|---|---|---|
| DD/MM/AAAA | 1.0 | Criação do documento | \<nome\> |
| DD/MM/AAAA | 1.1 | Adição de novas informações | \<nome\> |

---

## Sumário

- [Introdução](#introdução)
  - [Definições, acrônimos e abreviações](#definições-acrônimos-e-abreviações)
- [Usuários identificados](#usuários-identificados)
- [Requisitos funcionais](#requisitos-funcionais)
- [Requisitos não-funcionais](#requisitos-não-funcionais)
- [Não-requisitos](#não-requisitos)
- [Matriz de rastreabilidade](#matriz-de-rastreabilidade)

---

## Introdução

O objetivo deste documento é apresentar os requisitos de software do produto
**\<Nome do Sistema\> (\<SIGLA\>)**.

### Definições, acrônimos e abreviações

Esta subseção fornece as definições dos termos, acrônimos e abreviações necessários à
adequada interpretação deste documento.

**Identificação dos requisitos.** A referência a um requisito é feita pelo seu
identificador, no formato `[TIPOnnn]`:

- `RF` — Requisito Funcional
- `RNF` — Requisito Não-Funcional
- `NR` — Não-Requisito (o que foi decidido que o sistema **não** fará)

O número é uma **sequência única para todo o conjunto de tipos**: se o último identificador
criado foi RF012, o próximo é 013, seja ele RF, RNF ou NR. Exemplos: `RF001`, `RF1234`,
`RNF014`, `NR002`.

**Atributos dos requisitos:**

- **Requisitos vinculados**: lista dos requisitos com os quais mantém rastreabilidade.
- **Prioridade**: Essencial, Importante, Desejável.
- **Complexidade**: Complexa, Alta, Média, Baixa.
- **Risco**: Alto, Médio, Baixo.

**Outros identificadores usados neste projeto:** `UC1` (caso de uso), `RN1` (regra de
negócio), `MSG01` (mensagem do sistema), `ADR-0001` (decisão de arquitetura).

\<Acrescente aqui os termos do domínio, ou remeta ao glossário.\>

## Usuários identificados

Os seguintes usuários foram identificados para o sistema:

- Usuário do sistema
  - Usuários comuns
    - \<papel\>
    - \<papel\>
  - Administrador do sistema

## Requisitos funcionais

Escritos em forma de história de usuário: **Como um \<papel\>, eu gostaria de \<ação\>,
para que \<benefício\>**, seguido do detalhamento (dados obrigatórios, formatos, condições).

- **[RF001]** — Como um \<papel\>, eu gostaria de \<ação\>, para que \<benefício\>.
  \<Detalhamento: campos obrigatórios, formatos aceitos, condições, limites.\>

  **Critérios de aceitação**
  1. **Dado** \<contexto\>, **quando** \<ação\>, **então** \<resultado observável\>.
  2. **Dado** \<contexto de recusa: dado inválido, sem permissão, limite atingido\>, **quando** \<ação\>, **então** \<recusa e mensagem MSG0x\>.

  | Atributo | Valor |
  |---|---|
  | Requisitos vinculados | RF002, RNF014 |
  | Prioridade | Essencial |
  | Complexidade | Média |
  | Risco | Baixo |
  | Casos de uso | UC1 |
  | Origem | \<quem solicitou / documento / código `arquivo:linha`\> |
  | Status | Proposto / Aprovado / Implementado / Deprecado |

- **[RF002]** — …

> Quando o volume de requisitos for grande, mantenha a lista enxuta (identificador +
> história de usuário + detalhamento) e leve a tabela de atributos para uma tabela única
> ao final da seção, com uma linha por requisito.

## Requisitos não-funcionais

Agrupados por categoria. Percorra todas as nove, mesmo que algumas fiquem vazias — é assim
que aparece a exigência que ninguém mencionou. Todo RNF precisa dizer **como será
verificado**.

### Disponibilidade
- **[RNF00x]** — \<requisito\> · *Verificação:* \<como medir\>

### Privacidade e segurança

Se o sistema trata dados pessoais, cubra no mínimo: controle de acesso por recurso,
proteção dos dados em trânsito e em repouso, direitos do titular (exportar, corrigir,
excluir) e retenção. Detalhes técnicos e legais em `../07-seguranca-privacidade/`.

- **[RNF00x]** — \<requisito\> · *Verificação:* \<como medir\>

### Usabilidade
- **[RNF00x]** — …

### Suportabilidade
- **[RNF00x]** — …

### Interoperabilidade
- **[RNF00x]** — …

### Manutenibilidade
- **[RNF00x]** — …

### Desempenho
- **[RNF00x]** — …

### Implementação
- **[RNF00x]** — …

### Implantação
- **[RNF00x]** — …

## Não-requisitos

O que foi explicitamente decidido que o sistema não fará. Registrar evita que a discussão
volte a cada reunião e protege o escopo contratual.

- **[NR001]** — \<o que não será feito\> · *Motivo:* \<razão\> · *Reavaliar se:* \<condição\>

## Matriz de rastreabilidade

### Rastreabilidade entre RFs e RNFs

Marque `X` onde o requisito não-funcional incide sobre o funcional. Linha inteira vazia
indica RNF que não afeta nada — provavelmente mal escrito ou fora de escopo. Coluna vazia
em requisito crítico indica RF sem nenhuma exigência de qualidade associada.

| RNF \ RF | RF001 | RF002 | RF003 | RF004 |
|---|---|---|---|---|
| RNF00x | | X | X | |
| RNF00y | X | | | X |

### Rastreabilidade entre RFs e casos de uso

| RF | Casos de uso | Regras de negócio |
|---|---|---|
| RF001 | UC1, UC2 | RN1 |

## Requisitos deprecados

| ID | Descrição resumida | Deprecado em | Substituído por | Motivo |
|---|---|---|---|---|

---
*Última revisão: AAAA-MM-DD | Responsável: \<nome\> | Fontes: \<DVP, entrevistas, código\>*
