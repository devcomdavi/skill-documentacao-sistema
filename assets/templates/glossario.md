# Glossário — definições, acrônimos e abreviações

> Corresponde à subseção "Definições, acrônimos e abreviações" do Documento de Requisitos.
> Pode viver aqui como arquivo separado e ser referenciado a partir dele.

> Um termo, uma definição, usada igual no negócio, no código e na documentação.
> Quando o negócio e o código usam nomes diferentes para a mesma coisa, registre os dois
> e escolha um como oficial — ambiguidade de nome é fonte silenciosa de bug.

| Termo | Definição | Sinônimos usados no negócio | Representação no código |
|---|---|---|---|
| Pedido | Intenção de compra registrada por um Cliente, contendo um ou mais itens | Ordem, OS | `Pedido` (`src/dominio/pedido/`), tabela `pedidos` |
| Cliente adimplente | Cliente sem títulos vencidos há mais de 5 dias úteis | Cliente OK, cliente liberado | `Cliente.estaAdimplente()` |
| Pedido de alto valor | Pedido com valor total acima de R$ 10.000 (RN-007) | Pedido especial | constante `LIMITE_APROVACAO` |

## Termos ambíguos identificados
| Termo | Problema | Definição adotada |
|---|---|---|
| "Ativo" | Usado para cliente ativo (não inativado) e para contrato vigente | Separar em `cliente.ativo` e `contrato.vigente` |

---
*Última revisão: AAAA-MM-DD | Responsável: <nome>*
