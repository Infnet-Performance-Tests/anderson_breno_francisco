# Dataset: Customer Support Ticket Dataset

## 1. Fonte

- Publicação: **Customer Support Ticket Dataset**.
- Autor/publicador no Kaggle: `suraj520`.
- Arquivo: `customer_support_tickets.csv` (3.945.533 bytes).
- Origem de acesso: [Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset/data).
- Licença indicada na publicação: **CC0: Public Domain**.
- Data de acesso: **26 de agosto de 2026**.

## 2. Principais características

A publicação descreve tickets de suporte relacionados a produtos tecnológicos. A versão de
referência possui 8.469 registros e 17 colunas:

| Grupo | Variáveis |
| --- | --- |
| Identificação do ticket | `Ticket ID` |
| Dados do cliente | `Customer Name`, `Customer Email`, `Customer Age`, `Customer Gender` |
| Produto e compra | `Product Purchased`, `Date of Purchase` |
| Conteúdo/intenção | `Ticket Type`, `Ticket Subject`, `Ticket Description` |
| Operação do atendimento | `Ticket Status`, `Resolution`, `Ticket Priority`, `Ticket Channel` |
| Tempos e avaliação | `First Response Time`, `Time to Resolution`, `Customer Satisfaction Rating` |

Campos ligados ao encerramento do atendimento, como resolução, tempo de resolução e satisfação,
podem estar ausentes em tickets ainda não encerrados. Isso deve ser validado na EDA, e não tratado
automaticamente como erro.

O dataset também contém nome e e-mail. Mesmo sendo um conjunto público, essas colunas devem ser
tratadas como dados pessoais: não devem aparecer em logs, gráficos, respostas da API ou exemplos
de documentação.

## 3. Motivo da escolha

O conjunto é adequado ao projeto porque combina:

- texto livre do cliente, necessário para uma futura classificação de intenção;
- categorias de atendimento que podem servir como referência inicial de intenção;
- variáveis operacionais para análise estatística e formulação de hipóteses;
- cenários de segurança realistas, como dados pessoais, entrada textual não confiável e acesso
  autenticado a uma futura inferência de IA.

> TODO da entrega: ajustar esta justificativa aos objetivos discutidos em aula e às descobertas
> efetivamente observadas no notebook.

## Limites que devem ser verificados

- Confirmar a proveniência dos dados além da publicação no Kaggle.
- Verificar a licença e as condições de redistribuição antes de compartilhar o CSV.
- Investigar se textos ou categorias apresentam padrões artificiais, repetição ou vazamento de
  rótulo.
- Não inferir que valores ausentes são aleatórios sem analisar sua relação com `Ticket Status`.
