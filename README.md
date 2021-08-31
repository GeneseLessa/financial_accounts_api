# Budget and Message APIs

Este repositório contem a base para execução de duas APIs Rest desenvolvidas usando Django Rest Framework.

A primeira delas se chama **Budget API** e basicamente detêm o trabalho de gerir o cadastro de usuários no sistema e administrar que os mesmos possam visualizar os dados de suas respectivas contas e movimentar o saldo através de operações específicas.

A segunda API se chama **Message API** e basicamente possui a função de notificação de eventos, pois, uma das regras do desafio era executar o envio de e-mail para o cliente a cada instância de movimento (débito ou crédito) na conta do usuário.


### Requisitos

Este projeto foi pensado para executar sobre o Docker, embora esteja numa versão inicial e itens relacionados à segurança do ambiente podem ser incrementados. Serão necessários:

» Docker

» Docker Compose

» Git

## Instruções para execução

Após realizar o clone deste repositório, você deverá navegar até ele e digitar o seguinte comando (ambiente Linux ou Mac):

$ docker-compose up --build

O docker irá baixar as imagens e gerar os contêineres necessários ao processo.

## APIs e Endpoints

### Budget API
O acesso base a esta API se dará por meio da porta 8000 no localhost. Basicamente o acesso deverá ser feito em:

http://localhost:8000



#### Autenticação, cadastro, listagem e detalhamento individual de usuários (endpoints públicos)

* **[POST] /authenticate**: JSON Body: (username, password)
* **[POST] /api/users/create_user**: JSON Body: (username, password, name, email)
* **[GET] /api/users**: Listagem de todos os usuários cadastrados
* **[GET] /api/users/:id**: Detalhes do usuário com ID informado na rota

#### Criação de conta, visualização de conta e movimentos na conta (endpoints protegidos por token)


Os seguintes endpoints necessitam de um token válido que identifique o usuário autenticado. Este token é adquirido no endpoint acima. O token deverá estar no header Authorization da seguinte maneira:

Authorization: "Token XXXXXXXXXXX"

Onde XXXXX é o token obtido em /authenticate via POST

* **[POST] /api/accounts**: (owner: id do dono da conta, kind: 'pf ou pj'): cria uma aconta caso o usuário no possua uma ainda
* **[GET] /api/accounts**: retorna detalhes da conta cadastrada
* **[POST] /api/accounts/movement**: (operation: debit ou credit, value): cadastra um movimento de crédito ou débito na API e realiza a notificação por meio da **API Messages**
