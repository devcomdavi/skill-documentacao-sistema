# Visões do sistema

Analisar por visões existe porque **públicos diferentes fazem perguntas diferentes** — e
porque o mesmo diagrama pode ter propósitos distintos dependendo da visão em que aparece.
O caso mais claro: o diagrama de atividades aparece tanto na visão de casos de uso quanto
na visão lógica. Na primeira, mostra o fluxo de eventos de um caso de uso, na perspectiva
de quem usa o sistema. Na segunda, mostra o fluxo interno de uma operação de classe, na
perspectiva do desenvolvedor. Mesmo diagrama, leitura diferente.

| Visão | Pergunta que responde | Público | Modelos |
|---|---|---|---|
| Casos de uso | **O que** o sistema faz e como isso é percebido por quem o usa | Clientes, designers, desenvolvedores, gerentes | Casos de uso, atividades, sequência, comunicação, protótipos |
| Lógica | **Como** as funcionalidades são projetadas e estruturadas | Designers, desenvolvedores | Classes, objetos, máquina de estados, atividades |
| Processos | O que roda concorrente e como as partes conversam em execução | Arquitetos, SRE | Sequência, atividades, estados |
| Implementação | Como o código está organizado no repositório | Desenvolvedores novos no time | Pacotes, dependências, estrutura de pastas |
| Implantação | Onde o sistema roda e como chega lá | Infra, SRE, segurança | Implantação, contêineres |

Nem todo sistema precisa das cinco. Faça somente o que for útil e registre em
`docs/README.md` o motivo de cada omissão — ausência justificada também é informação.

---

## Visão de casos de uso

Arquivo: `docs/03-visao-casos-de-uso/visao-de-casos-de-uso.md`

Exibe as funcionalidades do sistema e como elas são percebidas pelos usuários enquanto
atores que interagem com ele.

Uma orientação importante sobre o público: mesmo quando o cliente não vai ver o diagrama,
**projete-o como se ele fosse ver**. Isso força simplicidade e evita o diagrama denso de
include/extend que só o autor entende. Se o seu diagrama de casos de uso precisa de
explicação técnica para ser lido, ele falhou no propósito.

Conteúdo:
1. Lista de atores, com descrição de uma linha e as generalizações entre eles.
2. Diagrama geral de casos de uso, com o retângulo delimitando a fronteira do sistema
   (ou um retângulo por módulo, quando forem muitos UCs).
3. Tabela: UC, nome, ator primário, RFs atendidos, técnica de detalhamento usada, link.
4. Link para a especificação de cada caso de uso.

A derivação dos atores e dos casos de uso a partir dos requisitos funcionais está em
`extracao.md`, seções 1 a 3.

### Escolha da técnica de detalhamento

Para cada caso de uso, escolha **uma**:

| Técnica | Quando prefira | Observação |
|---|---|---|
| Especificação descritiva (tabela) | Fluxo com muitos passos, exceções e regras | Formato completo; template disponível |
| História de usuário | Times ágeis, quando as etapas vão virar casos de teste | Mais simples e direto; casa bem com TDD |
| Diagrama de atividades | Quando o desenho comunica melhor que o texto | Bom para decisões e paralelismo |

Nunca mantenha duas representações do mesmo caso de uso. Se você alterar uma e esquecer da
outra, criou uma inconsistência que alguém vai descobrir da pior maneira. Em algumas
empresas a história de usuário *é* o documento de requisitos, com valor contratual — nesses
casos, não duplique em especificação descritiva.

### Mensagens do sistema

Não escreva o texto das mensagens direto nos fluxos. Crie identificadores (`MSG01`,
`MSG02`) e mantenha um artefato único de mensagens, que também vira o arquivo de idioma no
código (`lang/pt-br`, `lang/en-us`). Assim, alterar uma mensagem usada em oito casos de uso
é uma edição, não oito; e a internacionalização já nasce pronta.

---

## Visão lógica

Arquivo: `docs/04-visao-logica/visao-logica.md`

Exibe a estrutura do sistema e como os componentes interagem entre si — **como** as
funcionalidades são projetadas.

Modelos:
- Estrutura estática: diagrama de classes, diagrama de objetos.
- Comportamento dinâmico: máquina de estados, diagrama de atividades (aqui aplicado ao
  fluxo de uma operação, não de um caso de uso).

Estrutura sugerida do documento:

1. **Tabelas de extração** — substantivo → classe/atributo/descartado, e verbo →
   operação/descartar/desnecessário/redundante. Mantenha-as no documento: são a
   justificativa rastreável de por que cada classe e cada método existem. Sem elas, meses
   depois ninguém sabe por que `Marca` virou classe e `local de compra` virou atributo.
2. **Diagrama de classes**, apresentado em versões (classes+atributos → relacionamentos →
   métodos).
3. **Estilo arquitetural adotado** e a regra de dependência entre camadas/módulos. Se não
   havia arquitetura definida, defina um padrão e registre em ADR.
4. **Máquinas de estado** das entidades com ciclo de vida (aquelas com campo `status`).
   Muita regra de negócio mora aqui.
5. **Padrões transversais**: autenticação, autorização, validação, tratamento de erro,
   transação, log, auditoria. É o que todo mundo pergunta no primeiro dia de projeto.
6. **Rastreabilidade**: quais UCs cada classe/módulo atende.

O erro típico é despejar todas as classes do sistema. Inclua o que tem significado de
domínio ou de arquitetura; DTOs, mappers e utilitários ficam de fora.

Os tipos de atributos e de parâmetros são definidos conforme o domínio, a linguagem e a
arquitetura adotada — não são universais, e o critério usado merece uma linha de
explicação.

---

## Visão de processos

Arquivo: `docs/05-outras-visoes/visao-de-processos.md`

Só faz sentido quando existe concorrência, assincronismo ou coordenação entre partes.
Documente: processos/serviços que rodam (API, workers, cron, consumidores de fila); fluxos
assíncronos (quem publica, quem consome, ordem, idempotência); sequência dos cenários
críticos; transações e consistência (o que é transacional, onde há consistência eventual e
qual a janela aceitável); tratamento de falha (timeout, retry, backoff, circuit breaker,
fila de mensagens mortas); e pontos de concorrência (lock, versionamento otimista, risco de
condição de corrida).

---

## Visão de implementação

Arquivo: `docs/05-outras-visoes/visao-de-implementacao.md`

O guia de sobrevivência de quem acabou de clonar o repositório: árvore de diretórios
anotada; convenções de organização (por camada? por feature? por contexto?); dependências
externas relevantes e o motivo de cada escolha não óbvia; como rodar local, testar, lintar
e buildar; onde ficam migrações, seeds e configuração por ambiente; e — a seção de maior
retorno prático e a mais esquecida — **como adicionar** um endpoint, uma entidade, um job.

---

## Visão de implantação

Arquivo: `docs/05-outras-visoes/visao-de-implantacao.md`

Diagrama de implantação com nós e recursos gerenciados; ambientes e o que difere entre
eles; pipeline de CI/CD; configuração e segredos (onde ficam, como são injetados, quem tem
acesso); observabilidade (logs, métricas, alertas); backup, retenção e recuperação, com
RPO/RTO se existirem; e segurança de rede.

Nunca coloque credencial, token, string de conexão real ou IP interno sensível na
documentação. Referencie o cofre de segredos, não o valor.

---

## Modelo de dados

Arquivo: `docs/04-visao-logica/modelo-de-dados.md`

Diagrama ER com as tabelas principais (agrupadas por módulo se forem muitas); dicionário
de dados das colunas não óbvias; índices relevantes e a consulta que cada um serve;
estratégia de migração; dados pessoais marcados com base legal e política de retenção
(LGPD); volumes esperados e política de expurgo.

O modelo de dados costuma ser derivável do diagrama de classes da visão lógica, mas não é
idêntico a ele: decisões de normalização, índices e tipos físicos pertencem aqui.

---

## Checagem cruzada final

Ao terminar, pegue os casos de uso mais críticos e percorra-os nas outras visões. Cada
passo deve corresponder a uma classe da visão lógica, a um processo da visão de processos e
a um nó da visão de implantação. Onde o caminho não fecha, ou falta documentação ou falta
arquitetura — e nos dois casos você achou algo que vale reportar ao usuário.

---

*As definições das visões de casos de uso e lógica seguem o material de Maxwell Anderson
(IFPB), CC BY-SA 4.0: <https://maxwellamaral.github.io/lessons/softeng/design/>*
