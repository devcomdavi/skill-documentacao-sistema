# Elicitação de requisitos

Conteúdo:
1. Postura do entrevistador
2. Objetivos da atividade
3. Técnicas de elicitação
4. Entrevistas livres de contexto
5. Perguntas baseadas em contexto (e suas armadilhas)
6. Considerações ao formular perguntas
7. Condução da entrevista
8. Do resultado da entrevista para o DVP
9. Anti-padrões na escrita de requisitos

---

## 1. Postura do entrevistador

Duas coisas definem o resultado antes de qualquer técnica.

**Você não é o especialista no problema — o entrevistado é.** Se um escritório de
advocacia pede um sistema de gestão de processos judiciais, você provavelmente não entende
de Direito. Isso não é problema a esconder: é o ponto de partida. Pergunte como ele
organiza os processos hoje, como guarda os documentos, como controla prazos, como registra
os dados dos clientes. Humildade aqui é técnica, não etiqueta.

**Ser bom ouvinte vale mais que ser bom perguntador.** Muitos stakeholders executam suas
atividades manualmente, com papel e caneta, e têm dificuldade genuína de explicar o que
fazem. O objetivo do software é agilizar e automatizar essas atividades — então você
precisa entender o trabalho real, não a versão idealizada que a pessoa consegue verbalizar
sob pressão.

---

## 2. Objetivos da atividade

- Identificar os principais stakeholders do projeto.
- Levantar informações sobre o problema e as necessidades desses stakeholders.
- Analisar os dados coletados.
- Escrever os requisitos do produto.

---

## 3. Técnicas de elicitação

| Técnica | Quando usar | Cuidado |
|---|---|---|
| Entrevista | Principal técnica; serve em quase todo contexto | Conduzir a resposta invalida o dado |
| Brainstorming | Muitos stakeholders com visões divergentes | Precisa de mediação e critério de fechamento |
| Análise de documentos | Existe planilha, contrato, manual, legislação | A planilha em uso revela as regras não ditas |
| Prototipação de baixa fidelidade | Requisito de interface ambíguo | Protótipo bonito demais parece pronto |
| Observação do processo | Processo manual complexo | O que fazem ≠ o que dizem que fazem |
| Encenação / interpretação de papéis | Fluxo com muitos atores e passagens de bastão | Consome tempo; use nos fluxos críticos |
| Análise de sistema legado | Substituição de sistema existente | Nem tudo que existe precisa ser recriado |

Em ambiente de código, a análise de documentos e a análise do legado são as mais
produtivas: leia README, issues, testes e migrações antes de perguntar. Chegue à entrevista
com hipóteses, não com folha em branco — mas apresente-as como hipóteses, não como fatos.

---

## 4. Entrevistas livres de contexto

São as do começo, quando você ainda não tem conhecimento prévio do domínio. Três blocos:

**Para encontrar os atores**
- Quem são os clientes que solicitam o desenvolvimento do sistema?
- Quem são os usuários que vão utilizá-lo?
- As necessidades deles são diferentes entre si?
- Quais são suas habilidades e conhecimentos técnicos?
- Quais são suas formações e seus ambientes de trabalho?

**Para compreender os processos e as atividades**
- Qual problema vocês estão enfrentando?
- Por que desejam resolver este problema? Existem outras razões?
- Como esse problema é resolvido hoje?
- Existe em outro lugar uma solução para esse problema?
- Por que uma solução é tão importante?

**Para entender os principais requisitos do produto**
- Que problemas o sistema deve resolver?
- Poderão existir riscos para o usuário?
- Em que ambiente o produto será executado?
- O que você espera do produto quanto a qualidade, desempenho, segurança, usabilidade…?

Esse último bloco alimenta os requisitos não-funcionais. Percorra as nove categorias do
Documento de Requisitos (disponibilidade, privacidade e segurança, usabilidade,
suportabilidade, interoperabilidade, manutenibilidade, desempenho, implementação,
implantação), mesmo que algumas fiquem vazias.

---

## 5. Perguntas baseadas em contexto (e suas armadilhas)

Quando já se tem contexto, o risco muda: em vez de não saber o que perguntar, você começa
a **plantar a resposta**. Reconheça estes formatos:

- **Perguntas que induzem à resposta**: "Você precisa de uma tela touch screen?" /
  "Você necessita que rode em desktop?" O entrevistado tende a concordar por educação.
- **Perguntas com a resposta embutida**: "São necessários 10 usuários?" /
  "É necessário acesso via web?" Você acabou de definir o requisito sozinho.
- **Orientações controladas**: "Podemos esclarecer minhas dúvidas?" / "Pode me explicar
  melhor o problema?" — úteis para retomar o rumo sem induzir.
- **Perguntas longas e complexas**: "Tenho uma pergunta que se divide em três partes."
  A pessoa responde só à última parte. Quebre em três perguntas.

Nem todas são proibidas — as duas primeiras têm lugar na *validação* de algo já dito
("então confirmo: acesso via web, certo?"), nunca na *descoberta*.

---

## 6. Considerações ao formular perguntas

- **Não pergunte o que você já sabe.** Consome o tempo e a paciência do entrevistado.
- **Não peça que descreva algo que ele normalmente não descreve.** Evite aspectos técnicos
  com quem não é técnico.
- **Não pressuponha que ele consegue descrever atividades complexas.** Em vez de "como
  você descreveria o processo de integração de dados entre os sistemas?", pergunte "como
  os diferentes sistemas se comunicam hoje?".
- **Aceite que muita gente executa bem o que não sabe explicar.** Alguém pode usar um
  software complexo todo dia sem conseguir descrever seu funcionamento. Nesses casos,
  observe em vez de perguntar.
- **Prefira perguntas sem resposta definitiva.** Em vez de "qual é a solução ideal?",
  pergunte "como vocês lidam com isso atualmente?".
- **Evite perguntas que começam com "por que…?"** Elas soam como cobrança e geram postura
  defensiva. Em vez de "por que vocês fizeram assim?", pergunte "vocês chegaram a
  considerar outras opções?".

---

## 7. Condução da entrevista

- Seja gentil, educado, paciente e atencioso.
- Não espere que o entrevistado responda a todas as suas perguntas.
- Não espere respostas curtas e simples.
- Não apresse quem está respondendo. Silêncio depois de uma pergunta costuma ser
  pensamento, não incompreensão.
- Lembre-se de que há partes interessadas que não são usuárias de sistemas de informação e
  que os níveis de conhecimento e formação variam muito entre elas.
- **Sempre ouça.**

Ritmo em conversa por chat: no máximo 5 perguntas por rodada, agrupadas por tema, e um
rascunho devolvido ao fim de cada rodada. Se o usuário responder "tanto faz", ofereça duas
opções concretas com o trade-off explícito; se ainda assim não houver preferência, registre
como premissa no DVP.

---

## 8. Do resultado da entrevista para o DVP

O Documento de Visão do Produto é escrito logo após as primeiras entrevistas e **antes** da
elicitação detalhada — ele é o norteador que permite formular as perguntas seguintes e
dividir as necessidades em categorias que virarão módulos do sistema.

Conteúdo: descrição do problema, oportunidades de negócio, benefícios (com os problemas
que cada um resolve e quem é afetado), stakeholders e usuários, funcionalidades principais
em alto nível, arquitetura ambiental e restrições.

**Restrições** merecem atenção porque são o que limita as decisões técnicas depois.
Percorra os seis tipos: hardware, software, segurança, regulatórias, tempo e custo, e
usabilidade. As regulatórias e as de prazo são as que mais costumam aparecer tarde demais.

O DVP pode ser anexado a um contrato entre as partes. Tudo que se escreve nele é
reaproveitado nas etapas seguintes — tenha cuidado com o que escreve, e mantenha-o
atualizado sempre que surgir informação nova.

---

## 9. Anti-padrões na escrita de requisitos

- **Requisito-solução**: descreve implementação em vez de necessidade ("usar Redis para
  cache"). Isso é decisão de arquitetura, vai para ADR.
- **Requisito duplo**: dois verbos numa frase, impossível de testar parcialmente. Separe.
- **Adjetivo sem verificação**: rápido, intuitivo, robusto, escalável. Sempre pergunte
  "verificado como?".
- **Requisito órfão**: ninguém sabe quem pediu nem por quê. Registre sempre a origem.
- **Elicitação por adivinhação**: gerar o documento inteiro sem perguntar nada.
- **Redundância de representação**: especificar o mesmo caso de uso como história de
  usuário *e* como diagrama de atividades. Quando um mudar, o outro vira mentira.

---

*Baseado no material de Engenharia de Requisitos de Maxwell Anderson (IFPB), CC BY-SA 4.0:
<https://maxwellamaral.github.io/lessons/softeng/requirements/>*
