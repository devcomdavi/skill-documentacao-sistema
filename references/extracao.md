# Heurísticas de extração

Como derivar, de forma disciplinada, cada artefato do anterior. Este é o núcleo da
metodologia: sem essas heurísticas, a passagem de requisitos para casos de uso e de casos
de uso para classes vira adivinhação.

Conteúdo:
1. Requisito funcional → atores
2. Requisito funcional → casos de uso
3. Relacionamentos do diagrama de casos de uso
4. Especificação de caso de uso → classes e atributos
5. Especificação de caso de uso → métodos
6. Aplicando em escala

---

## 1. Requisito funcional → atores

Leia o requisito e **extraia todos os substantivos**. Depois separe: quem *interage* com o
sistema é ator; o que é *informado ao* sistema é atributo.

Exemplo, a partir de um RF sobre um cliente que cadastra produtos com nome, data de
compra, marca, modelo, local de compra e valor pago:

| Substantivo | Classificação |
|---|---|
| cliente | **ator** — usa a funcionalidade |
| produto | dado (candidato a classe, ver seção 4) |
| nome do produto | dado informado |
| data de compra | dado informado |
| marca, modelo | dado informado |
| local de compra | dado informado |
| valor pago | dado informado |

Só `cliente` vai para o diagrama de casos de uso. Os demais substantivos não desaparecem —
eles reaparecem na visão lógica como classes e atributos.

Ator pode ser pessoa em um papel, sistema externo ou dispositivo externo. Ator é papel,
não indivíduo: a mesma pessoa pode ser Atendente e Gestor.

**Generalização entre atores.** Quando um ator é *um tipo de* outro, desenhe a seta de
generalização do especializado para o genérico. É comum e útil: `Cliente` é um tipo de
`Usuário comum`; `Usuário comum` e `Administrador` são tipos de `Usuário`. Isso evita
repetir a mesma associação para vários papéis e antecipa a hierarquia de permissões.

---

## 2. Requisito funcional → casos de uso

Agora **extraia todos os verbos** do mesmo requisito. Para cada um, faça a pergunta
decisiva:

> Este verbo é uma **funcionalidade** do sistema, uma **etapa** de uma funcionalidade
> maior, ou apenas uma **condição / verbo de ligação**?

Só o primeiro caso vira caso de uso. No exemplo acima, dos verbos *manter, controlar,
saber, ser, estar, dever*, apenas `manter` e `controlar` são candidatos. `saber` descreve
o benefício; `ser`, `estar` e `dever` são de ligação.

O que for **etapa** não some — vai para o fluxo principal, alternativo ou de exceção da
especificação do caso de uso. Guarde essa lista, ela é usada na seção 5.

### Convenções de nome

- Caso de uso começa com **verbo no infinitivo**: `Cadastrar cliente`, `Buscar produto`.
- Um CRUD completo sobre a mesma entidade colapsa em **um** caso de uso: em vez de
  `Cadastrar cliente` + `Alterar cliente` + `Excluir cliente` + `Buscar cliente`, escreva
  `Manter cliente`. As quatro operações aparecem como fluxos alternativos na especificação.
- Identificadores `UC1`, `UC2`… sem zeros à esquerda, citados assim em qualquer outro
  documento, teste ou mensagem de commit.

### Perguntas que ajudam a encontrar casos de uso

- Quais serviços ou funcionalidades os atores querem do sistema?
- O sistema armazena informações? Quais atores criam, leem, atualizam ou excluem essas informações?
- Qual ator **inicia** o caso de uso?
- Qual ator **informa** os dados? (pode ser sistema ou dispositivo externo)
- O sistema precisa **informar** algo a algum ator?
- Existe processamento externo que o sistema precisa conhecer?

---

## 3. Relacionamentos do diagrama de casos de uso

Três grupos, em ordem lógica e incremental:

**Ator ↔ ator** — um ator *é um tipo de* outro (generalização/especialização).

**Ator ↔ caso de uso** — o ator utiliza, inicia ou informa dados ao caso de uso, ou o caso
de uso informa algo ao ator. Linha cheia. Um retângulo em volta dos casos de uso delimita
a fronteira do sistema (ou de um módulo).

**Caso de uso ↔ caso de uso** — três tipos:

| Relação | Semântica | Direção da seta |
|---|---|---|
| `<<include>>` | **Obrigatória.** O UC incluído *deve* ser executado como parte do incluidor. | Do incluidor **para** o incluído |
| `<<extend>>` | **Opcional.** O UC estendido *pode* disparar o UC extensor, se o ator quiser. | Do extensor **para** o estendido (sentido inverso ao include) |
| Generalização | Um UC é um tipo especializado de outro. O especializado herda o fluxo do genérico. | Do especializado para o genérico |

Exemplo de `<<extend>>` que aparece em quase todo sistema: `Esqueci minha senha` e
`Cadastrar-se` estendem `Fazer login` — ações opcionais que o usuário pode ou não
disparar a partir da tela de login. Repare que `Cadastrar-se` também pode ter associação
direta com o ator, se for acessível pela página principal.

Exemplo de generalização: `Abrir conta comum` especializa-se em `Abrir conta poupança` e
`Abrir conta corrente`. Na especificação, o UC especializado não repete o fluxo do
genérico — ele diz "o ator segue o fluxo principal de UC1" e descreve só o que difere. Na
implementação, isso costuma virar herança de classes ou métodos.

Cuidado com o vício mais comum: encher o diagrama de include e extend. Se estiver na
dúvida, não use nenhum dos dois. O diagrama precisa ser compreensível pelo cliente.

---

## 4. Especificação de caso de uso → classes e atributos

Cinco passos:

```
descrição → extrair substantivos → tentativa de classes → eliminar classes estranhas → classes identificadas
```

Analise o **fluxo principal, os fluxos alternativos e as regras de negócio** da
especificação do UC. Extraia os substantivos e monte uma tabela classificando cada um como
**classe**, **atributo de \<classe\>** ou **descartado**.

O critério para ser classe: você consegue realizar ações sobre ela (cadastrar, alterar,
excluir, consultar) e ela se relaciona com outras entidades. O critério para ser atributo:
é característica de outra coisa.

| Substantivo | Tipo |
|---|---|
| cliente | classe |
| produto | classe |
| nome do produto | atributo de Produto |
| data de compra | atributo de Produto |
| segmento de produto | classe |
| marca | classe |
| modelo | classe |
| local de compra | atributo de Produto |
| modo de compra | classe |

**A decisão classe-vs-atributo é frequentemente ambígua e isso é normal.** `segmento de
produto` pode ser um simples campo texto em Produto, ou uma classe própria — se o negócio
precisa cadastrar, listar e manter segmentos, é classe. O mesmo vale para `marca`,
`modelo` e `modo de compra` (que tem valores fixos: online, físico — candidato natural a
enumeração ou a classe pequena). Explicite o critério que você usou, para o usuário poder
discordar.

Faça isso para **todos** os casos de uso, sem repetir atributos já listados. Classes que
aparecem cedo (como Cliente) só ganham atributos quando os UCs delas forem analisados —
não force atributos antes da hora, mas ao final o analista pode acrescentar os que
claramente fazem falta (Cliente sem nome e e-mail seria estranho).

Os tipos dos atributos são definidos conforme o domínio, a linguagem e a arquitetura
adotada. Se não houver arquitetura definida, defina e registre um padrão — isso é ADR.

Construa o diagrama de classes em versões: (v1) classes + atributos, (v2) relacionamentos
e atributos complementares, (v3) métodos. Mostre cada versão.

---

## 5. Especificação de caso de uso → métodos

Releia a especificação buscando **verbos simples e compostos**, agora para identificar
comportamento. Depois elimine redundância, generalidade, vaguidade, comportamentos que são
apenas instâncias de outros, e o que for desnecessário. Por fim, distribua o que sobrou
entre as classes identificadas.

Monte uma tabela com três colunas — verbo, tipo, nome da operação:

| Verbo extraído | Tipo | Operação |
|---|---|---|
| preencher os campos com os dados do produto | descartar | |
| cadastrar o produto | operação de Produto | `incluir_produto` |
| verificar se o produto foi cadastrado | operação de Produto | `validar_produto` |
| exibir mensagem de sucesso | operação de Produto | `exibir_mensagem` |
| selecionar listagem de produtos | desnecessário | |
| exibir lista de produtos | operação de Produto | `listar_produto` |
| buscar produtos na lista | operação de Produto | `buscar_produto` |
| selecionar campo de busca | desnecessário | |
| exibir lista de produtos encontrados | redundante | |
| editar dados do produto | operação de Produto | `alterar_produto` |
| exibir detalhes do produto | operação de Produto | `exibir_produto` |
| salvar dados alterados | descartar | |
| excluir produto | operação de Produto | `excluir_produto` |
| confirmar exclusão | redundante | |

Os quatro tipos de descarte têm significados distintos e vale usá-los com precisão:
**descartar** (é ação do usuário na interface, não do sistema), **desnecessário** (não
agrega comportamento novo), **redundante** (já coberto por outra operação já nomeada) e
**operação de \<Classe\>** (fica).

Verbos de alto nível como "manter" viram um conjunto de operações, não uma só:
`manter produto` → `incluir_produto`, `alterar_produto`, `excluir_produto`,
`buscar_produto`.

Para as classes cujos UCs ainda não foram analisados, é aceitável atribuir o conjunto
padrão de operações CRUD e refinar depois.

---

## 6. Aplicando em escala

Fazer isso à mão para 28 requisitos é inviável em uma conversa. Na prática:

- Processe os requisitos **em lotes** (5 a 8 por vez), mostrando a tabela de substantivos
  e verbos de cada lote antes de desenhar qualquer diagrama.
- Consolide a lista de atores e de casos de uso e valide com o usuário **antes** de
  escrever qualquer especificação detalhada. Reescrever 12 especificações porque o recorte
  estava errado é desperdício puro.
- Mantenha a tabela de classificação (substantivo → tipo, verbo → operação) **dentro do
  documento** da visão lógica. Ela não é rascunho: é a justificativa rastreável de por que
  cada classe e cada método existem, e é o que permite auditar a decisão meses depois.
- Quando o sistema for grande, aplique tudo isso módulo a módulo, não de uma vez.

---

*Heurísticas baseadas no material de Projeto de Software de Maxwell Anderson (IFPB),
CC BY-SA 4.0: <https://maxwellamaral.github.io/lessons/softeng/design/views_usecase/> e
<https://maxwellamaral.github.io/lessons/softeng/design/views_logic/>*
