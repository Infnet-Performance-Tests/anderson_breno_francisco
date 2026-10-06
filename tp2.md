# TP2

## Contexto do projeto

Olá! No TP1, você escolheu o dataset, fez a EDA inicial e montou a estrutura da API com autenticação básica. Agora o projeto entra em profundidade.

Neste TP, você vai completar a análise exploratória do dataset — incluindo correlações, testes de hipótese e visualizações sofisticadas — e vai transformar a API FastAPI em uma API de verdade: com todos os controles de segurança do OWASP Top 10 aplicados e auditada por uma ferramenta real (OWASP ZAP). Lembre-se de que, em alguns meses, um colega vai tentar invadir essa API. Quanto mais robusta ela estiver agora, mais interessante vai ser o pentest depois.

## Objetivo da entrega

Produzir a análise exploratória completa do dataset e entregar a API FastAPI com controles OWASP Top 10 implementados e auditada por scan passivo ZAP. Este TP corresponde à competência integradora: Implementar análise estatística completa e controles OWASP Top 10 na API FastAPI auditada por ZAP.

## Tarefas

### 1. Implemente o EDA completo sobre o conjunto de dados Customer Support Ticket Dataset considerando as variáveis numéricas, categóricas textuais. Formule pelo menos duas hipóteses e realize um teste de hipótese formal (t-test ou Mann-Whitney) para cada hipótese formulada. O EDA completo deve conter as seguintes etapas:
- 1.1 Compreensão do problema e do dataset
- 1.2 Inspeção inicial
- 1.3 Verificação da qualidade dos dados
- 1.4 Limpeza e preparação dos dados
- 1.5 Análise Univariada
- 1.6 Análise Multivariada
- 1.7 Identificação de Outliers e Anomalias
- 1.8 Documentação do EDA e conclusões

### 2. Crie o arquivo fastapi/database.db utilizando SQLite, contendo as tabelas necessárias para usuários e predictions. Cada prediction deve possuir um owner_id que identifique seu proprietário. Crie também o arquivo fastapi/sqlite_database.py utilizando sqlite3 para criação e população inicial do banco. Devem existir pelo menos dois usuários e predictions pertencentes a usuários diferentes. As consultas realizadas pela API devem utilizar SQLModel, sem SQL raw.

### 3. Configure os modelos Pydantic utilizados para receber dados das requisições com extra='forbid', de forma que a API rejeite campos extras que não estejam definidos no modelo esperado.

### 4. Implemente controle de acesso por ownership para evitar vulnerabilidades do tipo BOLA. Nas rotas que retornam recursos por ID, verifique se o usuário autenticado é o proprietário do recurso antes de permitir o acesso. Caso o recurso pertença a outro usuário, a API não deverá retorná-lo.


### 5. Configure os headers de segurança HTTP: HSTS, X-Frame-Options, X-Content-Type-Options e Content-Security-Policy via middleware FastAPI. Configure também CORS com allowlist explícita de origens via middleware FastAPI.

### 6. Implemente rate limiting no endpoint de autenticação /auth/token utilizando a biblioteca SlowAPI, com o objetivo de reduzir tentativas de brute force. Configure o endpoint para permitir no máximo 10 requisições por minuto por cliente.

### 7. Execute um scan passivo com OWASP ZAP na API rodando localmente. Exporte o relatório de findings. Para cada finding com severidade Medium ou High, documente:
- 7.1. Finding
- 7.2. Severidade
- 7.3. Confiança
- 7.4. URL afetada
- 7.5. O que foi detectado
- 7.6. Por que é um problema
- 7.7. Correção realizada
- 7.8. Validação
- 7.9. Risco aceito, se não corrigido

### 8. Escreva 3 testes pytest cobrindo:
- (a) tentativa de acesso sem token
- (b) tentativa de acesso a recurso de outro usuário
- (c) envio de campo extra no body da request.

## Entrega

Sua entrega deve ser realizada em um repositório git. O repositório deve estar público ou acessível para o e-mail do professor tiago.xavier@prof.infnet.edu.br. A estrutura do repositório deve conter os seguintes diretórios e arquivos:

### Diretório Raiz:
Deve conter o arquivo README.md com o objetivo do projeto, instruções de instalação, instruções de execução da API, instruções para criação/população do banco de dados, instruções para execução dos testes e estrutura de pastas do projeto.

### Diretório data:
Deve conter o arquivo .csv contendo o Customer Support Ticket Dataset utilizado no projeto.

### Diretório eda:
Deve conter exatamente um arquivo .ipynb com o EDA completo do projeto. O notebook deve conter todas as etapas solicitadas do EDA completo no TP2.

### Diretório fastapi:
Deve conter todo o código-fonte da aplicação FastAPI. A aplicação deve incluir:
- estrutura modular da API;
- autenticação JWT;
- modelos Pydantic com extra='forbid';
- modelos e consultas com SQLModel;
- controle de acesso por ownership;
- headers HTTP de segurança;
- configuração de CORS com allowlist explícita;
- rate limiting com SlowAPI no endpoint /auth/token;
- rotas necessárias para demonstrar os controles implementados.

### Arquivo fastapi/database.db:
Deve conter o banco de dados SQLite utilizado pela aplicação, com usuários e recursos de exemplo pertencentes a usuários diferentes.

### Arquivo fastapi/sqlite_database.py:
Deve conter o código necessário para criação e população inicial do banco de dados.

### Diretório tests:
Deve conter os testes automatizados implementados com pytest. Devem existir, no mínimo, testes para:

- tentativa de acesso sem token;
- tentativa de acesso a recurso pertencente a outro usuário;
- envio de campo extra no body da requisição.

### Diretório zap:
Deve conter o relatório exportado pelo OWASP ZAP após a execução do scan passivo da API.

### Diretório zap/scan_passivo_zap.md:
Deve conter um documento com a análise dos findings Medium e High encontrados pelo OWASP ZAP. Caso não existam findings Medium ou High, essa informação deve ser explicitamente documentada.

### No Moodle, deve ser anexado um arquivo PDF contendo as seguintes informações:
- Nome de cada aluno;
- Link para o repositório.

No Git, o nome do repositório deve ser nome1_nome2..._tp2 onde nomeX representa o primeiro nome de cada aluno. No Moodle, o nome do PDF enviado deve seguir o formato nome1_ultimosobrenome1_nome2_ultimosobrenome2..._PB_TP2.PDF.

## Rubricas

### 2. Implementar análise estatística completa e controles OWASP Top 10 na API FastAPI auditada por ZAP
- O aluno apresentou notebook contendo heatmap de correlação produzido com seaborn?
- O aluno executou pelo menos um teste de hipótese formal com SciPy e interpretou o p-valor?
- O aluno narrou os resultados em linguagem acessível, conectando as estatísticas às hipóteses do TP1?
- O aluno implementou API que rejeita campos extras no body com status 422? (Pydantic extra='forbid' em funcionamento)
- O aluno implementou rotas que retornam recursos por ID e verificam se o recurso pertence ao usuário autenticado? (proteção BOLA)
- O aluno apresentou headers HSTS, X-Frame-Options e X-Content-Type-Options presentes nas respostas da API?
- O aluno implementou endpoint POST /auth/token que retorna 429 após exceder o limite de requisições configurado?
- O aluno documentou o limite escolhido e a justificativa técnica no README ou nos comentários do código?
- O aluno entregou o relatório ZAP exportado presente no repositório ou entregue como anexo?
- O aluno apresentou, para cada finding Medium ou High, um documento com: o que é, por que é um problema e o que foi feito? (corrigido ou aceito com justificativa)
- O aluno apresentou relatório de EDA que possui as seções: problema, dados, análise, insights e próximos passos?
- O aluno entregou relatório que conecte os insights da análise estatística à pergunta de classificação que vem no TP3?
