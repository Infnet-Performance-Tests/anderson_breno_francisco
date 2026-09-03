# Projeto de Bloco — TP1

**Grupo:** Anderson, Breno e Francisco

Análise exploratória do *Customer Support Ticket Dataset* e estrutura base de uma API
FastAPI com autenticação JWT, servindo de fundação para o sistema de atendimento ao cliente
com IA que será construído ao longo do bloco.

---

## Objetivo do projeto

Definir o domínio do sistema a partir de duas frentes:

1. **EDA exploratória** — entender o dataset de tickets de atendimento, avaliar sua qualidade
   e levantar hipóteses verificáveis sobre as intenções dos usuários.
2. **API FastAPI autenticada** — estruturar de forma modular a API que servirá o futuro
   modelo de classificação de intenção, já com autenticação JWT funcional e as fronteiras de
   confiança mapeadas.

O modelo de machine learning **não** faz parte desta entrega: a rota `POST /predict` devolve
uma intenção pré-determinada que simula a saída do modelo futuro, mantendo o contrato HTTP
estável para a troca posterior.

---

## Estrutura de pastas

```text
.
├── README.md                    # este arquivo
├── requirements.txt             # dependências de execução
├── pyproject.toml               # configuração de pytest e ruff
├── Makefile                     # atalhos (install, run, test, notebook, dfd)
├── .env.example                 # modelo da variável JWT_SECRET_KEY
│
├── data/
│   └── customer_support_tickets.csv    # dataset original do Kaggle, sem alterações
│
├── eda/
│   ├── eda.ipynb                # EDA completa, com as saídas já executadas
│   └── hipoteses.md             # hipóteses sobre as intenções dos usuários
│
├── fastapi/                     # código-fonte da aplicação
│   ├── main.py                  # ponto de entrada (uvicorn main:app)
│   ├── config.py                # credencial do admin e parâmetros do JWT
│   ├── routes/                  # definição dos endpoints
│   │   ├── health.py            #   GET  /health
│   │   ├── auth.py              #   POST /auth/token
│   │   └── predict.py           #   POST /predict  (protegida)
│   ├── models/                  # modelos Pydantic de entrada e saída
│   │   ├── health.py
│   │   ├── auth.py
│   │   └── prediction.py
│   ├── security/                # segurança e autenticação
│   │   ├── jwt.py               #   geração e validação do token JWT
│   │   └── dependencies.py      #   OAuth2PasswordBearer + dependência de admin
│   ├── application/             # casos de uso (fronteira entre rotas e domínio)
│   ├── domain/                  # conceitos de negócio, sem FastAPI nem Pydantic
│   └── tests/                   # testes automatizados das três rotas
│
└── others/
    ├── dfd.png                  # DFD da API com entradas, saídas e trust boundaries
    ├── dfd-and-cia.md           # análise CIA por componente e ameaças priorizadas
    └── generate_dfd.py          # script que gera o dfd.png
```

### Por que a aplicação está organizada assim

O fluxo é sempre o mesmo, em uma direção só:

```text
routes (HTTP)  ->  application (caso de uso)  ->  domain / security
```

- `routes` conhece HTTP e delega; não contém regra de negócio.
- `application` é a fronteira pública da aplicação.
- `domain` guarda conceitos de negócio puros, sem dependência de framework.
- `models` contém os contratos HTTP em Pydantic.
- `security` concentra OAuth2 e JWT.

Não há repositório, banco de dados nem *event bus* porque esta entrega não precisa deles.

---

## Instalação

Requisito: **Python 3.12 ou superior**.

```bash
# 1. clonar e entrar no repositório
git clone <url-do-repositorio>
cd anderson_breno_francisco

# 2. criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. instalar as dependências
python -m pip install -r requirements.txt

# 4. definir a chave de assinatura do JWT
cp .env.example .env             # e substituir o valor por um segredo aleatório
```

O `requirements.txt` cobre as três frentes: API, EDA e testes.

---

## Execução

### API

O comando exigido pelo enunciado é executado **de dentro do diretório `fastapi/`**, onde
está o `main.py`:

```bash
cd fastapi
uvicorn main:app --reload
```

A API sobe em `http://127.0.0.1:8000` e a documentação interativa fica em
`http://127.0.0.1:8000/docs`.

> Defina `JWT_SECRET_KEY` no ambiente antes de subir. Sem ela, a aplicação usa um valor
> padrão explicitamente marcado como de desenvolvimento.

### Notebook da EDA

```bash
jupyter lab eda/eda.ipynb
```

O notebook já está **executado e com todas as saídas salvas** — gráficos e tabelas são
visíveis sem precisar rodar nada. Ele baixa o dataset via `kagglehub` na primeira execução.
As hipóteses derivadas da análise estão em `eda/hipoteses.md`.

### Testes

```bash
pytest            # 6 testes cobrindo as três rotas e a proteção do /predict
ruff check .      # análise estática
```

### Regerar o DFD

```bash
python others/generate_dfd.py
```

---

## Endpoints

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| `GET` | `/health` | Não | Verifica se a API está ativa. |
| `POST` | `/auth/token` | Não | Autentica o admin e devolve um JWT válido por 30 minutos. |
| `POST` | `/predict` | **Sim (Bearer)** | Recebe um texto e devolve uma intenção simulada. |

### Credencial

| Campo | Valor |
| --- | --- |
| usuário | `admin` |
| senha | `admin123` |

A credencial fica no código (`fastapi/config.py`) porque o enunciado exige. É uma exposição
conhecida e documentada: em produção ela migraria para um provedor de identidade com senha
em *hash*. A chave de assinatura do JWT, essa sim, já é injetada por variável de ambiente.

### Exemplos

```bash
# 1. saúde da API
curl http://127.0.0.1:8000/health
# {"status":"ok"}

# 2. obter o token
curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
# {"access_token":"eyJhbGciOiJIUzI1NiIs...","token_type":"bearer"}

# 3. usar o token na rota protegida
curl -X POST http://127.0.0.1:8000/predict \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"I need help with a refund"}'
# {"intent":"general_inquiry","confidence":1.0,"model_version":"stub-v0"}

# 4. sem token, a rota protegida recusa
curl -i -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" -d '{"text":"teste"}'
# HTTP/1.1 401 Unauthorized
```

---

## Dataset

**Customer Support Ticket Dataset** — publicado por `suraj520` no Kaggle
([link](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data)),
licença CC0 (domínio público). São **8.469 tickets × 17 colunas**, cobrindo o texto livre do
cliente, a categorização do atendimento e métricas operacionais.

A cópia original está em `data/customer_support_tickets.csv` e é preservada sem alterações.
A documentação técnica completa — fonte, características e motivo da escolha — está na
**seção 0 do notebook**.

### Principais achados da EDA

1. **A ausência de dados é estrutural, não aleatória.** `Resolution`, `Time to Resolution` e
   `Customer Satisfaction Rating` estão preenchidas em exatamente os 2.769 tickets `Closed`;
   `First Response Time` falta exatamente nos 2.819 tickets `Open`. Por isso nada foi
   imputado — imputar inventaria uma nota de satisfação para um ticket ainda aberto.
2. **Não há desbalanceamento de classes.** Todas as categóricas são praticamente uniformes
   (desbalanceamento ≤ 1,20x), o que é irrealista para uma operação real de suporte.
3. **O texto não prediz o rótulo.** O qui-quadrado não rejeita a independência em nenhum par
   testado (texto × assunto: p=0,911; assunto × tipo: p=0,981; canal × tipo: p=0,458), com
   V de Cramér sempre abaixo de 0,04. Textos idênticos aparecem sob rótulos diferentes.
4. **Um único template de abertura cobre 69,3% dos tickets**, e 100% das descrições continham
   o placeholder `{product_purchased}` não renderizado.
5. **O conjunto é sintético.** As evidências acima, somadas à incoerência temporal (em 49,3%
   dos tickets encerrados a resolução ocorre *antes* da primeira resposta), sustentam essa
   conclusão.

O notebook registra **5 hipóteses verificáveis** sobre as intenções dos usuários, cada uma
com o padrão observado, o método de teste e ao menos uma explicação alternativa.

---

## Segurança

O DFD da API está em **[`others/dfd.png`](others/dfd.png)** e a análise da tríade CIA por
componente, junto com as ameaças priorizadas, em
**[`others/dfd-and-cia.md`](others/dfd-and-cia.md)**.

Controles já implementados nesta entrega:

- `/predict` protegida por `OAuth2PasswordBearer` e JWT válido.
- Token com `sub`, `iat` e `exp` (30 minutos), aceitando apenas o algoritmo configurado.
- Comparação de credenciais em tempo constante (`hmac.compare_digest`).
- Resposta `401` genérica, que não revela qual campo falhou.
- Validação estrita de entrada e saída com Pydantic, com limite de 5.000 caracteres no texto.
- A API não ecoa nem registra o texto do ticket, que pode conter dados pessoais.
- Chave de assinatura fora do código, via `JWT_SECRET_KEY`.

---

## Referências

- [Customer Support Ticket Dataset (Kaggle)](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data)
- [FastAPI — OAuth2 com JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
