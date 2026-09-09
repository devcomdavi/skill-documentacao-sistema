# Documentação — \<Nome do Sistema\> (\<SIGLA\>)

\<Uma frase sobre o que o sistema faz.\>

**Status:** atualizada em AAAA-MM-DD, referente ao commit `\<hash curto\>`.

## Por onde começar
- Sou novo no projeto → [DVP](01-visao-produto/dvp.md), depois [Visão de implementação](05-outras-visoes/visao-de-implementacao.md)
- Vou implementar uma feature → [Requisitos](02-requisitos/requisitos.md) e [Visão de casos de uso](03-visao-casos-de-uso/visao-de-casos-de-uso.md)
- Vou mexer na estrutura → [Visão lógica](04-visao-logica/visao-logica.md) e [Decisões](06-decisoes/)
- Estou de plantão → [Visão de implantação](05-outras-visoes/visao-de-implantacao.md)

## Índice

### 1. Visão do produto
- [Documento de Visão do Produto (DVP)](01-visao-produto/dvp.md)

### 2. Requisitos
- [Documento de Requisitos](02-requisitos/requisitos.md)
- [Glossário](02-requisitos/glossario.md)
- [Regras de negócio](02-requisitos/regras-de-negocio.md)
- [Mensagens do sistema](02-requisitos/mensagens.md)

### 3. Visão de casos de uso
- [Visão de casos de uso](03-visao-casos-de-uso/visao-de-casos-de-uso.md)
- [UC1 — ...](03-visao-casos-de-uso/uc1-....md)

### 4. Visão lógica
- [Visão lógica](04-visao-logica/visao-logica.md)
- [Modelo de dados](04-visao-logica/modelo-de-dados.md)

### 5. Outras visões
- [Visão de processos](05-outras-visoes/visao-de-processos.md)
- [Visão de implementação](05-outras-visoes/visao-de-implementacao.md)
- [Visão de implantação](05-outras-visoes/visao-de-implantacao.md)

### 6. Decisões
- [ADR-0001 — ...](06-decisoes/adr-0001-....md)

## Convenções de identificação

| Prefixo | Significado | Exemplo |
|---|---|---|
| RF | Requisito funcional | RF001 |
| RNF | Requisito não-funcional | RNF014 |
| NR | Não-requisito | NR002 |
| UC | Caso de uso | UC1 |
| RN | Regra de negócio | RN1 |
| MSG | Mensagem do sistema | MSG01 |
| ADR | Decisão de arquitetura | ADR-0001 |

RF, RNF e NR compartilham uma **sequência numérica única**. Identificadores nunca são
reciclados: requisito removido é marcado como deprecado, não apagado.

## Seções deliberadamente omitidas

| Seção | Motivo |
|---|---|
| Visão de processos | Sistema sem processamento assíncrono ou concorrência relevante |

## Como manter

A documentação é mantida junto com o código. Ao alterar estrutura do sistema (entidade,
endpoint, integração, arquitetura), atualize os artefatos afetados no mesmo PR e propague
na direção do encadeamento: requisito → caso de uso → classes.

Para verificar defasagem: `python scripts/doc_audit.py --repo .`
