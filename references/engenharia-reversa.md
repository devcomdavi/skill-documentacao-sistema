# Engenharia reversa — documentar um sistema existente

Objetivo: extrair a estrutura real do sistema a partir do código, com o mínimo de leitura
possível, separando claramente o que é fato do que é inferência.

---

## Ordem de exploração

Siga esta sequência. Ela é desenhada para dar o máximo de entendimento por token lido.

**1. Superfície do repositório**
`README`, `CONTRIBUTING`, `docs/` existente, `Makefile`, `docker-compose.yml`, `.env.example`,
arquivos de manifesto (`package.json`, `pom.xml`, `requirements.txt`, `pyproject.toml`,
`go.mod`, `composer.json`, `*.csproj`, `Gemfile`). Daqui saem stack, dependências,
comandos de execução e uma primeira noção de integrações.

**2. Mapa estrutural sem ler conteúdo**
```bash
git ls-files | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40
```
Mostra onde o código está concentrado. Complemente com contagem de linhas por diretório
para achar o núcleo do sistema. Pastas grandes e recentes são o coração; pastas grandes e
paradas costumam ser legado congelado.

**3. Pontos de entrada**
Onde o processo começa: `main`, `app.py`, `index.ts`, `Application.java`, `Program.cs`,
definição de rotas, handlers de fila, cron/scheduler, comandos de CLI. Cada entrypoint é
candidato a caso de uso.

**4. Rotas e contratos**
Liste todos os endpoints com verbo, caminho, autenticação exigida e handler. Se houver
OpenAPI/Swagger, ele é a fonte mais rápida. Sem ele, procure os decoradores/anotações de
rota. Essa lista é o esqueleto da visão de casos de uso.

**5. Modelo de dados**
Migrações (fonte mais confiável, porque contam a história), entidades/models do ORM, ou
DDL. Daqui saem o ER e boa parte do glossário. Preste atenção em: colunas com nome
estranho, campos `status`/`tipo` com valores fixos (máquinas de estado escondidas),
`_legacy`, `_old`, colunas nullable que deveriam ser obrigatórias.

**6. Regras de negócio**
Serviços de domínio, validações, `if` sobre valores de negócio, jobs. É a parte mais cara
de extrair e a mais valiosa. Grep por termos do domínio descobertos no passo 5.

**7. Testes**
Testes de aceitação/integração descrevem comportamento esperado melhor que qualquer
comentário — são requisitos executáveis. Nomes de teste viram critérios de aceitação
quase diretamente.

**8. Integrações e infraestrutura**
Clientes HTTP, SDKs, filas, webhooks, variáveis de ambiente, Dockerfile, IaC, workflows
de CI. Daqui saem visão de implantação e o diagrama de contexto (C4 nível 1).

---

## Comandos úteis

```bash
# tamanho relativo do código por diretório (ignora vendor/build)
git ls-files | grep -vE 'node_modules|vendor|dist|build|\.lock' \
  | xargs wc -l 2>/dev/null | sort -rn | head -30

# arquivos mais alterados no último ano = núcleo ativo do sistema
git log --since="1 year ago" --name-only --pretty=format: \
  | sort | uniq -c | sort -rn | head -30

# quem mexe em quê (útil para saber a quem perguntar)
git shortlog -sn --since="1 year ago"

# endpoints (adapte o padrão à stack)
grep -rnE "@(Get|Post|Put|Delete|Patch)Mapping|@app\.(get|post|put|delete)|router\.(get|post|put|delete)|Route::" src/ 2>/dev/null

# variáveis de ambiente = integrações e configuração
grep -rhoE "(process\.env|os\.getenv|System\.getenv|ENV\[)[^)]*" . 2>/dev/null | sort -u

# última alteração de cada documento (defasagem)
git log -1 --format="%ad %an" -- docs/
```

---

## De código para artefato

| Fonte no código | Artefato gerado |
|---|---|
| Rotas + controllers + permissões | Casos de uso (UC1…), atores e sua generalização |
| Testes de integração/aceitação | Fluxos principal, alternativos (A1, A2…) e de exceção dos UCs |
| Entidades / migrações | Classes da visão lógica, ER, glossário |
| Enums e campos `status` | Diagramas de estado, regras de transição |
| Validações e serviços de domínio | Regras de negócio (RN1…) |
| Middlewares, guards, políticas | RNFs de privacidade e segurança, matriz de permissões |
| Estrutura de pastas + imports | Visão lógica e de implementação |
| Docker, IaC, CI | Visão de implantação, C4 nível 2 |
| Clientes HTTP, SDKs, filas | Diagrama de contexto, integrações |
| Índices, cache, timeouts, paginação | Pistas de RNF de desempenho |
| Arquivos de idioma (`lang/`, i18n) | Artefato de mensagens (MSG01…) |
| Issues, TODOs, código morto | Seção "Pontos de atenção" e débito técnico |

---

## Fato x inferência

Classifique cada afirmação da documentação:

- **Fato**: está no código, com evidência. Cite `caminho/arquivo.ext:linha`.
- **Inferência forte**: padrão claro e consistente no código, mas sem confirmação explícita.
  Escreva normalmente e marque a origem como "inferido do código".
- **Inferência fraca**: você deduziu intenção. Marque `⚠️ A CONFIRMAR` e leve à lista de
  pendências.
- **Desconhecido**: RNFs quase sempre caem aqui — o código não diz qual disponibilidade o
  negócio exige. Não invente número; escreva `⚠️ NÃO DOCUMENTADO — definir com o negócio`.

Ao final, apresente ao usuário uma lista curta e priorizada de perguntas (5 a 10, não 40),
focada no que muda a documentação de forma relevante.

---

## Escopo e ordem de ataque

Documentar legado inteiro de uma vez raramente compensa. Ordem recomendada:

1. **DVP** — mesmo em sistema existente é o artefato norteador. Se não existir, crie; se estiver desatualizado, atualize; se estiver mal escrito, reescreva.
2. Glossário do domínio — destrava todo o resto e resolve ambiguidade de nomes.
3. Modelo de dados — é o esqueleto mais estável do sistema.
4. Documento de Requisitos reconstruído (RF em forma de história de usuário) e casos de uso do módulo mais crítico — pergunte ao usuário qual é.
5. Visão lógica (classes e métodos) e de implementação.
6. Visão de implantação.
7. Demais módulos, por ordem de dor.

Entregue e valide cada bloco antes de seguir. Se o usuário corrigir seu entendimento do
domínio no bloco 2, tudo depois disso já sai certo.

---

## Sinais de que a documentação existente está morta

Ao encontrar `docs/` já existente, verifique antes de confiar: data do último commit,
endpoints citados que não existem mais, tecnologias mencionadas que sumiram das
dependências, diagramas com componentes inexistentes. Documentação errada é pior que
ausente — se estiver morta, diga isso claramente ao usuário e proponha reescrever em vez
de remendar.

---

*Complementa o material de Maxwell Anderson (IFPB), CC BY-SA 4.0, aplicando as mesmas
convenções de identificação e derivação a sistemas já existentes.*
