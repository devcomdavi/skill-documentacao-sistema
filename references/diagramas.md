# Diagramas — sintaxe de referência

Todos os blocos abaixo são modelos prontos para copiar e adaptar. Padrão da skill é
Mermaid embutido no Markdown; PlantUML aparece só onde Mermaid não cobre bem.

Conteúdo:
1. Casos de uso
2. Classes / modelo de domínio
3. Sequência
4. Estados
5. Atividades (fluxo)
6. Entidade-relacionamento
7. Componentes
8. Implantação
9. C4 (contexto e contêineres)
10. Diagrama de requisitos (rastreabilidade)
11. Erros comuns de sintaxe

---

## 1. Casos de uso

Mermaid **não tem** diagrama de casos de uso nativo. Duas saídas.

Antes da sintaxe, as convenções que valem para as duas: caso de uso começa com **verbo no
infinitivo**; um CRUD completo sobre a mesma entidade colapsa em `Manter <entidade>`;
identificadores `UC1`, `UC2`, sem zeros à esquerda; retângulo delimitando a fronteira do
sistema (ou de um módulo). O diagrama precisa ser compreensível pelo cliente — se depende
de explicação técnica para ser lido, simplifique.

### 1a. Emulação em Mermaid (renderiza em qualquer lugar — preferida)

```mermaid
flowchart LR
    usuario(["👤 Usuário"])
    cliente(["👤 Cliente"])
    admin(["👤 Administrador"])
    fabricante(["⚙️ Sistema do Fabricante"])

    subgraph sistema["Sistema de Controle de Garantias"]
        uc1("UC1<br>Manter produto")
        uc2("UC2<br>Manter garantia")
        uc3("UC3<br>Fazer login")
        uc4("UC4<br>Recuperar senha")
        uc5("UC5<br>Validar dados do produto")
        uc6("UC6<br>Consultar contato do fabricante")
    end

    cliente --- uc1
    cliente --- uc3
    admin --- uc3
    uc6 --- fabricante

    cliente -.->|"é um tipo de"| usuario
    admin -.->|"é um tipo de"| usuario

    uc1 -.->|"&laquo;include&raquo;"| uc5
    uc2 -.->|"&laquo;extend&raquo;"| uc1
    uc4 -.->|"&laquo;extend&raquo;"| uc3
```

Convenções de desenho: atores como `([texto])`, casos de uso como `("texto")`, fronteira
como `subgraph`, associação ator–UC com linha cheia `---`, relações entre UCs com linha
tracejada `-.->` rotulada. Use `<br>` para quebrar linha dentro do nó.

**Atenção ao sentido das setas**, que é a fonte nº 1 de erro nesse diagrama:

| Relação | Semântica | A seta sai de | e aponta para |
|---|---|---|---|
| `<<include>>` | obrigatória — o incluído **deve** ser executado | o UC incluidor | o UC incluído |
| `<<extend>>` | opcional — o extensor **pode** ser disparado | o UC extensor | o UC estendido |
| generalização | "é um tipo de" | o especializado | o genérico |

No exemplo: `Manter produto` **inclui** `Validar dados do produto` (não dá para cadastrar
sem validar), enquanto `Manter garantia` **estende** `Manter produto` (o cliente pode ou
não cuidar das garantias naquele momento). O mesmo vale para `Recuperar senha`, que estende
`Fazer login`.

Um ator pode ter associação direta com um UC que também estende outro. `Cadastrar-se`
estende `Fazer login` e, ao mesmo tempo, pode ser acessado direto da página principal —
nesse caso, desenhe as duas relações.

### 1b. PlantUML (UML formal, quando exigido por norma acadêmica ou corporativa)

```plantuml
@startuml
left to right direction

actor "Usuário" as usuario
actor "Cliente" as cliente
actor "Administrador" as admin
actor "Sistema do Fabricante" as fabricante

cliente --|> usuario
admin --|> usuario

rectangle "Sistema de Controle de Garantias" {
  usecase "UC1 Manter produto" as UC1
  usecase "UC2 Manter garantia" as UC2
  usecase "UC3 Fazer login" as UC3
  usecase "UC4 Recuperar senha" as UC4
  usecase "UC5 Validar dados do produto" as UC5
  usecase "UC6 Consultar contato do fabricante" as UC6
}

cliente --> UC1
cliente --> UC3
admin --> UC3
UC6 --> fabricante

UC1 ..> UC5 : <<include>>
UC2 ..> UC1 : <<extend>>
UC4 ..> UC3 : <<extend>>
@enduml
```

Em PlantUML, `--|>` é generalização e `..>` é a dependência usada para include/extend.

Salve como `.puml` ao lado do `.md` e referencie, ou use bloco ```plantuml no Markdown
(renderiza no GitLab; no GitHub precisa de extensão/CI que gere a imagem).

---

## 2. Classes / modelo de domínio

```mermaid
classDiagram
    class Pedido {
        +UUID id
        +Date criadoEm
        +StatusPedido status
        +Decimal valorTotal()
        +adicionarItem(Produto, int) void
        +enviarParaFaturamento() void
    }
    class ItemPedido {
        +int quantidade
        +Decimal precoUnitario
        +Decimal subtotal()
    }
    class Cliente {
        +String nome
        +String documento
        +boolean estaAdimplente()
    }
    class Produto {
        +String sku
        +String nome
        +Decimal preco
    }
    class StatusPedido {
        <<enumeration>>
        EM_EDICAO
        AGUARDANDO_APROVACAO
        FATURADO
        CANCELADO
    }
    class RepositorioPedido {
        <<interface>>
        +salvar(Pedido) void
        +buscarPorId(UUID) Pedido
    }

    Cliente "1" --> "0..*" Pedido : realiza
    Pedido "1" *-- "1..*" ItemPedido : contém
    ItemPedido "0..*" --> "1" Produto : referencia
    Pedido --> StatusPedido
```

Relações: `-->` associação, `*--` composição, `o--` agregação, `<|--` herança,
`<|..` implementação de interface, `..>` dependência. Multiplicidade entre aspas nas pontas.
Visibilidade: `+` público, `-` privado, `#` protegido.

Para modelo de domínio na visão lógica, prefira mostrar **um agregado por diagrama** com
suas entidades e objetos de valor; a visão geral de todos os agregados vira um diagrama
de pacotes separado.

---

## 3. Sequência

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant API as API de Pedidos
    participant SVC as ServicoPagamento
    participant GW as Gateway externo
    participant DB as Banco de dados

    C->>API: POST /pedidos/{id}/pagar
    API->>SVC: processarPagamento(pedidoId, cartao)
    SVC->>DB: registrar tentativa (status=PENDENTE)
    SVC->>GW: autorizar(valor, token)

    alt Autorizado
        GW-->>SVC: 200 aprovado
        SVC->>DB: status=PAGO
        SVC-->>API: PagamentoAprovado
        API-->>C: 200 OK
    else Recusado
        GW-->>SVC: 402 recusado
        SVC->>DB: status=RECUSADO
        API-->>C: 402 Pagamento recusado
    end

    Note over SVC,GW: Timeout de 8s. Após 3 falhas,<br>o circuit breaker abre (ver ADR-0005)
```

`->>` chamada síncrona, `-->>` retorno, `-)` mensagem assíncrona, `+`/`-` ativação (cada `+` precisa de exatamente um `-` em todos os caminhos de `alt`). Não use `;` em texto de mensagem ou nota: no diagrama de sequência ele separa instruções.
Blocos: `alt/else`, `opt`, `loop`, `par`, `critical`, `break`.

---

## 4. Estados

Ideal para documentar ciclo de vida de entidade — muitas regras de negócio moram aqui.

```mermaid
stateDiagram-v2
    [*] --> EmEdicao : criar pedido
    EmEdicao --> AguardandoAprovacao : enviar (valor > R$ 10.000) [RN7]
    EmEdicao --> Faturado : enviar (valor <= R$ 10.000)
    AguardandoAprovacao --> Faturado : gestor aprova
    AguardandoAprovacao --> EmEdicao : gestor rejeita
    EmEdicao --> Cancelado : cancelar
    AguardandoAprovacao --> Cancelado : cancelar
    Faturado --> [*]
    Cancelado --> [*]

    note right of AguardandoAprovacao
        Expira em 72h sem resposta
        e retorna para EmEdicao (RN11)
    end note
```

---

## 5. Atividades / fluxo de processo

```mermaid
flowchart TD
    inicio([Início]) --> receber[Receber pedido]
    receber --> valida{Cliente<br>adimplente?}
    valida -->|Não| recusa[Registrar recusa] --> notifica[Notificar cliente] --> fim([Fim])
    valida -->|Sim| estoque{Estoque<br>disponível?}
    estoque -->|Não| backorder[Gerar pendência de compra] --> notifica
    estoque -->|Sim| reserva[Reservar itens]
    reserva --> valor{Valor ><br>R$ 10.000?}
    valor -->|Sim| aprovacao[Aguardar aprovação do gestor]
    valor -->|Não| fatura[Faturar]
    aprovacao --> fatura
    fatura --> fim
```

Para raias (quem faz o quê), use `subgraph` por ator:

```mermaid
flowchart TD
    subgraph Vendedor
        a1[Registrar pedido] --> a2[Enviar para faturamento]
    end
    subgraph Gestor
        b1[Analisar pedido]
    end
    subgraph Sistema
        c1[Validar crédito] --> c2[Reservar estoque]
    end
    a2 --> c1
    c2 --> b1
```

---

## 6. Entidade-relacionamento

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ ITEM_PEDIDO : contem
    PRODUTO ||--o{ ITEM_PEDIDO : referenciado_em
    PEDIDO ||--o| PAGAMENTO : possui

    CLIENTE {
        uuid id PK
        varchar nome
        varchar documento UK "CPF ou CNPJ"
        boolean ativo
        timestamp criado_em
    }
    PEDIDO {
        uuid id PK
        uuid cliente_id FK
        varchar status "EM_EDICAO|AGUARDANDO_APROVACAO|FATURADO|CANCELADO"
        numeric valor_total
        timestamp criado_em
    }
    ITEM_PEDIDO {
        uuid id PK
        uuid pedido_id FK
        uuid produto_id FK
        int quantidade
        numeric preco_unitario "preço no momento da compra"
    }
```

Cardinalidade: `||` exatamente um, `o|` zero ou um, `}|` um ou muitos, `}o` zero ou muitos.
Lado esquerdo lê-se de fora para dentro: `||--o{` = um para zero-ou-muitos.

---

## 7. Componentes

```mermaid
flowchart TB
    subgraph frontend["Frontend"]
        spa["SPA React"]
    end
    subgraph backend["Backend"]
        api["API REST<br>(controllers)"]
        dominio["Núcleo de domínio<br>(entidades + regras)"]
        infra["Adaptadores<br>(repositórios, clientes HTTP)"]
    end
    subgraph externo["Externo"]
        pg[("PostgreSQL")]
        gw["Gateway de Pagamento"]
        smtp["Servidor SMTP"]
    end

    spa -->|"HTTPS/JSON"| api
    api --> dominio
    dominio -.->|"interfaces"| infra
    infra --> pg
    infra --> gw
    infra --> smtp
```

A seta tracejada de `dominio` para `infra` comunica inversão de dependência: o domínio
declara a interface, a infraestrutura implementa. Se a arquitetura do projeto for essa,
mostre isso explicitamente — é a informação mais útil do diagrama.

---

## 8. Implantação

```mermaid
flowchart TB
    subgraph usuario["Dispositivo do usuário"]
        browser["Navegador"]
    end
    subgraph cloud["Nuvem — região sa-east-1"]
        subgraph edge["Borda"]
            cdn["CDN + WAF"]
        end
        subgraph app["Cluster de aplicação"]
            c1["Container API<br>2 réplicas · 1 vCPU · 2 GB"]
            worker["Container Worker<br>1 réplica"]
        end
        subgraph dados["Camada de dados"]
            db[("PostgreSQL 16<br>Multi-AZ")]
            redis[("Redis<br>cache + fila")]
            s3[("Object storage<br>anexos")]
        end
    end
    terceiro["Gateway de Pagamento<br>(SaaS)"]

    browser --> cdn --> c1
    c1 --> db
    c1 --> redis
    worker --> redis
    worker --> db
    c1 --> s3
    c1 --> terceiro
```

Sempre anote no texto: ambientes existentes (dev/homolog/prod), como o deploy acontece,
onde ficam segredos, e política de backup. Um diagrama de implantação sem essas quatro
informações não ajuda ninguém em incidente.

---

## 9. C4 — contexto e contêineres

Mermaid tem suporte a C4 (ainda experimental, sintaxe pode variar entre versões). Se
falhar na renderização, caia para `flowchart` com subgraphs como nos exemplos 7 e 8.

```mermaid
C4Context
    title Diagrama de Contexto — Sistema de Vendas

    Person(cliente, "Cliente", "Compra produtos pelo site")
    Person(gestor, "Gestor comercial", "Aprova pedidos de alto valor")
    System(vendas, "Sistema de Vendas", "Registra, aprova e fatura pedidos")
    System_Ext(gateway, "Gateway de Pagamento", "Autoriza cobranças em cartão")
    System_Ext(erp, "ERP", "Faturamento fiscal e estoque")

    Rel(cliente, vendas, "Registra e paga pedidos", "HTTPS")
    Rel(gestor, vendas, "Aprova pedidos", "HTTPS")
    Rel(vendas, gateway, "Solicita autorização", "REST/JSON")
    Rel(vendas, erp, "Envia pedido faturado", "Fila AMQP")
```

Níveis do C4 e o que documentar em cada um:
- **Nível 1 — Contexto**: o sistema como caixa preta e quem interage com ele. Vai na visão geral.
- **Nível 2 — Contêineres**: aplicações, bancos, filas — unidades que rodam separadamente. Vai na visão de implantação/implementação.
- **Nível 3 — Componentes**: módulos dentro de um contêiner. Vai na visão lógica.
- **Nível 4 — Código**: diagrama de classes. Só para partes realmente complexas; envelhece rápido.

Regra prática: gere sempre os níveis 1 e 2. Nível 3 só para os contêineres não triviais.
Nível 4 apenas onde a lógica é sutil o bastante para justificar.

---

## 10. Diagrama de requisitos (rastreabilidade)

```mermaid
requirementDiagram
    functionalRequirement RF001 {
        id: RF001
        text: Como cliente eu gostaria de manter os produtos que compro
        risk: medium
        verifymethod: test
    }
    performanceRequirement RNF014 {
        id: RNF014
        text: Tempo de resposta de no maximo 5 segundos
        risk: high
        verifymethod: test
    }
    element UC1 {
        type: "caso de uso"
        docref: "docs/03-visao-casos-de-uso/uc1-manter-produto.md"
    }
    element ServicoPedido {
        type: "modulo"
        docref: "src/dominio/pedido/"
    }

    UC1 - satisfies -> RF001
    ServicoPedido - satisfies -> RF001
    ServicoPedido - satisfies -> RNF014
```

Valores com hífen, barra ou espaço (como `docref` e `text` longos) vão entre aspas.
Tipos aceitos: `requirement`, `functionalRequirement`, `performanceRequirement`,
`interfaceRequirement`, `physicalRequirement`, `designConstraint`.
Relações: `contains`, `copies`, `derives`, `satisfies`, `verifies`, `refines`, `traces`.

Use isso só quando a rastreabilidade for exigida formalmente. Para o dia a dia, a tabela
de rastreabilidade em Markdown é mais fácil de manter e de ler em diff.

---

## 11. Erros comuns de sintaxe

- Parênteses, colchetes, chaves ou aspas **dentro** do texto de um nó quebram o parser.
  Escape com aspas: `no["Pedido (rascunho)"]` funciona; `no[Pedido (rascunho)]` não.
- Acentos são aceitos, mas o **id** do nó deve ser ASCII sem espaço: `nao_aprovado["Não aprovado"]`.
- `end` como texto de nó em flowchart quebra o diagrama — use `Fim` ou `fim([Fim])`.
- Em `classDiagram`, `<<interface>>` e `<<enumeration>>` vão numa linha própria dentro da classe.
- Em `stateDiagram-v2`, nomes de estado não podem ter espaço; use `AguardandoAprovacao` ou
  `s1 : Aguardando aprovação`.
- Em `erDiagram`, o nome da relação não pode ter espaço — use `underscore`.
- Comentários em Mermaid: linha começando com `%%`.

Rode `python scripts/check_mermaid.py <arquivo.md>` antes de entregar; ele pega blocos não
fechados, ids inválidos e os erros acima mais comuns.

---

*As convenções de casos de uso (verbo no infinitivo, "Manter X", sentido das setas de
include/extend e generalização) seguem o material de Maxwell Anderson (IFPB), CC BY-SA 4.0:
<https://maxwellamaral.github.io/lessons/softeng/design/uml_usecase/>*
