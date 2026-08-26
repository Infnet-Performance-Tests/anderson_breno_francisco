# TP1

## Contexto do projeto

Olá! Você está começando o Projeto de Bloco: ao final deste bloco, você vai ter construído um sistema de atendimento ao cliente alimentado por inteligência artificial — e depois vai atacar o sistema de um colega para descobrir as falhas de segurança que ele deixou.

Mas antes de atacar, você precisa construir. E, antes de construir um sistema inteligente, você precisa entender os dados. Neste primeiro TP, o seu trabalho é escolher o dataset que vai ser a base de todo o projeto, explorar esses dados com rigor estatístico e montar a estrutura da API que vai servir o sistema ao longo do bloco.

Não se preocupe com o modelo de machine learning nem com o agente agora — isso vem depois. Foque em entender os dados e em fazer a API rodar de forma segura desde o início.

## Objetivo da entrega

Produzir a análise exploratória inicial do dataset de atendimento ao cliente e configurar a estrutura base da API FastAPI com autenticação JWT funcional. Este TP corresponde à competência integradora: Definir o domínio do sistema com EDA exploratória e API FastAPI autenticada como base.

## Dataset
O dataset para o trabalho é 'Customer Support Ticket Dataset' disponível no kaggle no link:
[https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data)

## Tarefas

### 1. Leia toda a documentação disponível para o 'Customer Support Ticket Dataset' e documente tecnicamente o seguinte:
* **a.** Fonte (origem do dataset)
* **b.** Principais características
* **c.** Motivode escolha do dataset.


### 2. Realize a EDA inicial no dataset. O EDA deve ser implementado como visto em aula e deve conter os seguintes passos:
* **a.** Compreensão do problemae do dataset
* **b.** Inspeção inicial
* **c.** Vericação da qualidade dos dados
* **d.** Limpeza e preparação dos dados
* **e.** Análise Univariada


### 3. A partir da Análise Univariada e o desenvolvimento de histogramas e grá^cos para visualização das distribuições das principais variáveis, escreva pelo menos 3 hipóteses sobre as "intenções" dos usuários a partir dos padrões observados


### 4. Configure um projeto FastAPI com estrutura modular e que seja executável com 'uvicorn main:app --reload'. O código-fonte deve conter pelo menos:
* **a.** Arquivo 'main': pontode entrada da aplicação FastAPI
* **b.** Diretório 'routes': contém a definição das rotas/endpoints da API
* **c.** Diretório 'models': contém os modelos Pydantic utilizados para validar os dados de entrada e saída da API.
* **d.** Diretório 'security': contém as funcionalidades relacionadas à segurança e autenticação, como geração e validação de tokens JWT e configuração do 'OAuth2PasswordBearer'.


### 5. Implemente pelo menos 3 rotas: 'GET /health', 'POST /auth/token' e 'POST /predict'. A seguir está o objetivo de cada rota:
* **a.**  'GET/health': verifica se a API está ativa e funcionando corretamente.
* **b.**  'POST /auth/token': autentica o usuário e retorna um token JWT para acesso às rotas protegidas.
* **c.**  'POST/predict': não implementa o modelo de ML ainda. Esta rota recebe um texto e retorna uma intenção pré-determinada que simula a saída de um modelo que será implementado posteriormente.


### 6. No código-fonte da API, implemente autenticação JWT utilizando 'OAuth2PasswordBearer'. Defina o login e senha no próprio código-fonte (in-code) de um usuário admin, o qual deve ser o único com acesso à API. A rota '/predict' deve ser protegida pelo token válido.


### 7. Elabore um DFD básico da API com as entradas, saídas e trust boundaries identificados. Aplique a tríade CIA para cada componente: o que é confidencial, o que precisa de integridade, o que deve estar disponível.


## Entrega

Sua entrega deve ser realizada em um repositório git. O repositório deve estar público ou acessível para o e-mail do professor tiago.xavier@prof.infnet.edu.br. A estrutura do repositório de conter os seguintes diretórios:
- Diretório Raiz: deve conter o 'README.md' com objetivo do projeto, instruções de instalação, instruções de execução e estrutura de pastas.
- Diretório 'data': deve possuir arquivo '.csv' contendo o dataset 'Customer Support Ticket Dataset'.
- Diretório 'eda': deve possuir exatamente um arquivo '.ipynb' com o EDA do projeto. O EDA deve conter todos os itens sobre o EDA que foram solicitados nos exercícios.
- Diretório 'fastapi': deve possuir todo o código-fonte para uma aplicação FastAPI atendendo todos os itens sobre a aplicação FastAPI que foram solicitados nos exercícios. Arquivos e subdiretórios adicionais podem ser criados dentro de 'fastapi' para manter a aplicação modular.
- Diretório 'others': deve conter o DFD no formato '.png'.

No moodle, deve ser anexado um arquivo PDF contendo as seguintes informações:
- Nome de cada aluno Link para o repositório
- No git, o nome do repositório deve ser **'nome1_nome2...'** onde nomeX representa o primeiro nome de cada aluno. No moodle, o nome do PDF enviado deve seguir o formato **'nome1_ultimosobrenome1_nome2_ultimosobrenome2..._PB_TP1.PDF'**.