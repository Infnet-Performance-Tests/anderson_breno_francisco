# DFD e análise CIA da API (Tarefa 7)

Documento de apoio ao diagrama **[`dfd.png`](dfd.png)**, gerado por
[`generate_dfd.py`](generate_dfd.py) (`python others/generate_dfd.py`).

O escopo é o estado atual da API do TP1: três rotas, um único usuário admin definido em
código e uma predição simulada. O modelo de ML e o agente ainda não existem — aparecem no
diagrama como fluxos tracejados, para que a fronteira já esteja mapeada quando forem
implementados.

---

## 1. Componentes do diagrama

### Entidade externa

| ID | Componente | Descrição |
| --- | --- | --- |
| — | **Administrador** | Único usuário autorizado. Vive fora de qualquer fronteira de confiança da aplicação. |

### Processos

| ID | Processo | Responsabilidade |
| --- | --- | --- |
| P1 | `GET /health` | Informa se a API está no ar. Rota pública, sem autenticação. |
| P2 | `POST /auth/token` | Valida usuário e senha (`OAuth2PasswordRequestForm`) e solicita a emissão do JWT. |
| P3 | `POST /predict` | Recebe o texto do ticket, exige token válido e devolve a intenção. |
| P4 | **Segurança** | `OAuth2PasswordBearer`, assinatura e validação do JWT (`sub`, `iat`, `exp`). |
| P5 | **Predição** | Stub determinístico que simula a saída do futuro modelo. |

### Depósitos de dados

| ID | Depósito | Onde vive hoje |
| --- | --- | --- |
| D1 | Credencial do admin | `fastapi/config.py` — login e senha em código, como exige o enunciado. |
| D2 | Chave de assinatura JWT | Variável de ambiente `JWT_SECRET_KEY`, com valor padrão apenas para desenvolvimento. |
| D3 | Dataset de tickets | `data/customer_support_tickets.csv` — contém nome e e-mail (dados pessoais). |
| D4 | Modelo de ML | Ainda não existe. Fluxo tracejado no diagrama. |

---

## 2. Entradas e saídas

### Entradas (tudo o que atravessa uma fronteira em direção à aplicação)

| # | Entrada | Origem | Destino | Confiabilidade |
| --- | --- | --- | --- | --- |
| 1 | `username` + `password` (form-urlencoded) | Administrador | P2 | **Não confiável** |
| 3 | Texto do ticket (JSON) + `Authorization: Bearer` | Administrador | P3 | **Não confiável** |
| 5 | Requisição `GET /health` | Administrador | P1 | **Não confiável** |
| 7 | Leitura da credencial do admin | D1 | P2 | Confiável (mas é segredo) |
| 11 | Leitura da chave de assinatura | D2 | P4 | Confiável (mas é segredo) |
| 13 | Carregamento do modelo *(futuro)* | D4 | P5 | A verificar por *hash* |

### Saídas (tudo o que a aplicação devolve)

| # | Saída | Origem | Destino | Observação |
| --- | --- | --- | --- | --- |
| 2 | JWT assinado (HS256, expiração de 30 min) | P2 | Administrador | **Credencial temporária — é um segredo** |
| 4 | `{intent, confidence, model_version}` | P3 | Administrador | Não ecoa o texto de entrada |
| 6 | `{"status":"ok"}` | P1 | Administrador | Deliberadamente sem detalhes de versão ou infraestrutura |
| 10 | Identidade `admin` validada, ou `401` | P4 | P3 | Mensagem de erro genérica |

---

## 3. Trust boundaries

### TB1 — Internet ↔ API

Separa o administrador (e qualquer outro agente na rede) dos processos da aplicação.

- **Tudo que a atravessa é não confiável**: usuário, senha, texto do ticket e token.
- Controles já implementados: validação de esquema com Pydantic, limite de 5.000 caracteres
  no texto, autenticação obrigatória em `/predict`, comparação de credenciais em tempo
  constante (`hmac.compare_digest`) e resposta `401` genérica que não revela qual campo falhou.
- Controles pendentes para um ambiente publicado: **TLS obrigatório**, *rate limiting* em
  `/auth/token` e `/predict`, limite de tamanho de corpo no servidor e política de log que
  proíba registrar corpo de requisição, senha e token.

### TB2 — Aplicação ↔ segredos e artefatos locais

Separa o processo da aplicação dos segredos (D1, D2) e dos artefatos de dados (D3, D4).

- Um arquivo pode ser adulterado, substituído ou lido por outro processo da máquina.
- Controles já implementados: a chave de assinatura sai do código por variável de ambiente;
  o `.env` está no `.gitignore`; a API nunca lê o dataset em tempo de requisição.
- Controles pendentes: permissões restritivas de sistema de arquivos, `checksum`/versionamento
  do dataset e do futuro modelo, e rotação da chave JWT.

> **Risco aceito e declarado.** A credencial do admin em código (D1) e o valor padrão da
> chave JWT são exigências didáticas do enunciado. Em produção, D1 migraria para um provedor
> de identidade com senha em *hash* (bcrypt/argon2) e D2 para um cofre de segredos.

---

## 4. Tríade CIA por componente

**C** = Confidencialidade (quem pode ver) · **I** = Integridade (não pode ser alterado sem
detecção) · **A** = Disponibilidade (precisa estar acessível quando necessário).

| Componente | Confidencialidade | Integridade | Disponibilidade |
| --- | --- | --- | --- |
| **Administrador** (entidade externa) | Senha e token não podem ser expostos no cliente, no histórico do shell nem em capturas de tela. | Requisição não pode ser alterada em trânsito (exige TLS). | Precisa conseguir autenticar e consultar a API quando necessário. |
| **P1 `GET /health`** | Baixa — a resposta é pública e por isso deve ser mínima: não revelar versão, stack, caminho de arquivo ou estado interno. | Não pode reportar "ok" com a aplicação degradada, ou o monitoramento fica cego. | **Criticidade máxima**: é a sonda usada pelo monitoramento e pelo orquestrador. |
| **P2 `POST /auth/token`** | A senha nunca pode ser registrada em log nem devolvida em mensagem de erro. | Só emite token para credencial correta; as *claims* (`sub`, `exp`) precisam ser fiéis. | Se cair, ninguém obtém token e `/predict` fica inacessível. É o alvo natural de força bruta — precisa de *rate limiting*. |
| **P3 `POST /predict`** | Não pode registrar nem ecoar o texto do ticket, que pode conter dados pessoais do cliente. | Deve validar esquema **e** identidade antes de processar; a resposta deve refletir o modelo declarado em `model_version`. | Rota de negócio principal: exige limite de payload e de taxa para não ser derrubada por abuso. |
| **P4 Segurança (JWT)** | **A chave de assinatura é o segredo mais crítico do sistema** — quem a obtém forja qualquer token. | Algoritmo fixo (`HS256`), assinatura e `exp` verificados a cada requisição; nunca aceitar `alg: none` nem algoritmo vindo do token. | A validação precisa funcionar sempre: se falhar aberto, a API fica exposta; se falhar fechado, a API fica indisponível. **Falhar fechado é a escolha correta.** |
| **P5 Predição (stub)** | Hoje não há segredo; com o modelo real, parâmetros e regras podem ser sensíveis (risco de extração de modelo). | Precisa ser previsível e versionada — a resposta deve corresponder ao artefato aprovado. | Falha na predição não pode derrubar a API: exige *timeout* e resposta de erro controlada. |
| **D1 Credencial admin** | **Confidencial.** Hoje em código, o que é uma exposição conhecida e aceita para fins didáticos. | Só pode ser alterada por mudança de código revisada. | Precisa estar carregada na inicialização, senão nenhum login funciona. |
| **D2 Chave JWT** | **Confidencial — o ativo de maior valor.** Fora do versionamento (`.env` no `.gitignore`). | Trocar a chave invalida todos os tokens emitidos: mudança é uma operação controlada. | Precisa estar disponível na inicialização; sem ela, nem emissão nem validação funcionam. |
| **D3 Dataset de tickets** | Contém **nome e e-mail** (dados pessoais). Não pode aparecer em log, gráfico, resposta da API ou exemplo de documentação. A EDA isola essas colunas e não as grava no arquivo processado. | O CSV original é preservado sem alteração; toda transformação é gravada em `data/processed/`, nunca sobrescrevendo a fonte. | Necessário para a EDA e para o treino futuro; não é lido em tempo de requisição. |
| **D4 Modelo de ML** *(futuro)* | Pesos e hiperparâmetros podem ser propriedade intelectual. | **Precisa de verificação de procedência (hash/assinatura)**: carregar um artefato adulterado é execução de código não confiável. | Necessário para `/predict` responder; exige *fallback* explícito caso o carregamento falhe. |

---

## 5. Ameaças priorizadas e mitigação

| # | Ameaça | Componente | Impacto | Estado |
| --- | --- | --- | --- | --- |
| A1 | Vazamento da chave JWT permite forjar tokens de admin | D2 / P4 | Crítico — comprometimento total | Parcial: chave por variável de ambiente; falta cofre e rotação |
| A2 | Força bruta na credencial fixa do admin | P2 / D1 | Alto | Parcial: comparação em tempo constante e erro genérico; **falta *rate limiting*** |
| A3 | Credencial trafegando em texto claro | TB1 | Alto | **Pendente**: exige TLS no ambiente publicado |
| A4 | Texto malicioso no corpo de `/predict` (payload gigante, injeção no futuro LLM) | P3 | Médio hoje, alto com o modelo | Parcial: limite de 5.000 caracteres e validação Pydantic |
| A5 | Dados pessoais do dataset em log ou em resposta | D3 / P3 | Alto (privacidade) | Mitigado: colunas isoladas na EDA; a API não devolve o texto de entrada |
| A6 | Substituição do artefato de modelo por um adulterado | D4 | Alto | **Pendente**: definir *checksum* antes de integrar o modelo |
| A7 | Indisponibilidade por excesso de requisições | P1–P3 | Médio | **Pendente**: limites de taxa e de tamanho no servidor |

---

## 6. Revisão futura

Este modelo deve ser revisto quando o projeto ganhar: o modelo de ML real (D4 passa a ser
carregado em tempo de execução), um agente ou LLM (surge a fronteira de *prompt injection*),
um banco de dados (novo depósito com dados pessoais em escala) ou qualquer serviço externo
(nova trust boundary de saída).
