# Secure Support Agent Lab

Base enxuta para o Projeto de Bloco de análise e segurança de agentes de IA. O repositório
entrega uma API FastAPI autenticada e deixa a EDA preparada para ser preenchida após o download
do dataset.

## Decisões de arquitetura

O desenho aplica Clean Architecture apenas onde ela reduz acoplamento:

```text
HTTP route -> application facade -> domain/security
```

- `routes` conhece HTTP e delega os casos de uso.
- `application` é a fronteira pública da aplicação.
- `domain` contém apenas conceitos de negócio, sem FastAPI ou Pydantic.
- `models` contém os contratos HTTP em Pydantic.
- `security` concentra OAuth2 e JWT.
- Não há repository, banco, event bus ou interfaces ornamentais porque o TP ainda não precisa
  deles.

## Estrutura

```text
.
├── main.py
├── app
│   ├── application       # Facades/casos de uso
│   ├── domain            # Conceitos de negócio puros
│   ├── models            # DTOs Pydantic de entrada e saída
│   ├── routes            # Endpoints FastAPI
│   ├── security          # OAuth2PasswordBearer e JWT
│   └── config.py
├── analysis
│   └── 01_initial_eda.ipynb
├── data
│   ├── raw               # CSV original, não versionado
│   └── processed         # Dados derivados, não versionados
├── docs
│   ├── dataset.md
│   ├── dfd-and-cia.md
│   └── hypotheses.md
└── tests
```

## Como executar

Requisito: Python 3.12 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev,eda]"
cp .env.example .env
```

Exporte a chave do `.env` no seu shell ou defina `JWT_SECRET_KEY` diretamente. Em seguida:

```bash
uvicorn main:app --reload
```

A documentação interativa ficará em `http://127.0.0.1:8000/docs`.

### Credencial acadêmica

- usuário: `admin`
- senha: `admin123`

A credencial em código existe apenas porque o enunciado exige. Em produção, ela deve migrar
para um provedor de identidade ou armazenamento de credenciais com hash. A chave JWT já pode ser
injetada por variável de ambiente.

## Endpoints

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

curl -X POST http://127.0.0.1:8000/predict \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"I need help with a refund"}'
```

## Dataset e EDA

O arquivo `customer_support_tickets.csv` já está incluído em `data/raw/`, preservado sem
alterações. A fonte é o
[Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data).

1. Execute `jupyter lab analysis/01_initial_eda.ipynb`.
2. Preencha as interpretações e as três hipóteses somente depois de observar os resultados.

## Qualidade

```bash
pytest
ruff check .
ruff format --check .
```

## Referências

- [Dataset no Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data)
- [FastAPI: OAuth2 Password Bearer com JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
