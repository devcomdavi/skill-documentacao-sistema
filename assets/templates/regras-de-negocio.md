# Regras de negócio

Regras existem independentemente do software — são do domínio, não do sistema. Ficam
separadas dos requisitos porque mudam por decisão de negócio, não por mudança de escopo.

## RN1 — \<Nome da regra\>

**Enunciado:** \<a regra, de forma inequívoca\>

| Atributo | Valor |
|---|---|
| Aplicada em | UC1 (passo 3), UC4 (passo 2) |
| Requisitos | RF001 |
| Origem | \<lei, contrato, política interna, decisão de quem\> |
| Frequência de mudança | \<estável / muda por decisão comercial / muda por lei\> |

**Detalhamento:** \<tabela de decisão, fórmula ou máquina de estados, conforme o caso\>

---

## RN2 — \<Nome da regra\>

…

## Formatos úteis

- **Tabela de decisão** quando há muitas combinações de condição.
- **Fórmula explícita** quando há cálculo (documente arredondamento e unidade).
- **Máquina de estados** quando há ciclo de vida — use `stateDiagram-v2`.

---
*Última revisão: AAAA-MM-DD | Responsável: \<nome\>*
