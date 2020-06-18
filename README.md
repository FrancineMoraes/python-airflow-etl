# python-airflow-etl

### Repositório da implementação de um teste de etl aplicado pela empresa melhor envio

Neste teste, são fornecidas através de arquivos uma série de dados no padrão:

<code> 
{

    "request": {

        "method": "GET",

        "uri": "/get",

        "url": "http://httpbin.org:8000/get",

        "size": "75",

        "querystring": {},

        "headers": {

            "accept": "*/*",

            "host": "httpbin.org",

            "user-agent": "curl/7.37.1"

        },

    },

    "upstream_uri": "/",

    "response": {

        "status": 200,

        "size": "434",

        "headers": {

            "Content-Length": "197",

            "via": "kong/0.3.0",

            "Connection": "close",

            "access-control-allow-credentials": "true",

            "Content-Type": "application/json",

            "server": "nginx",

            "access-control-allow-origin": "*"

        }

    },

    "authenticated_entity": {

        "consumer_id": "80f74eef-31b8-45d5-c525-ae532297ea8e"

    },

    "route": {

        "created_at": 1521555129,

        "hosts": null,

        "id": "75818c5f-202d-4b82-a553-6a46e7c9a19e",

        "methods": ["GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD"],

        "paths": [

            "/example-path"

        ],

        "preserve_host": false,

        "protocols": [

            "http",

            "https"

        ],

        "regex_priority": 0,

        "service": {

            "id": "0590139e-7481-466c-bcdf-929adcaaf804"

        },

        "strip_path": true,

        "updated_at": 1521555129

    },

    "service": {

        "connect_timeout": 60000,

        "created_at": 1521554518,

        "host": "example.com",

        "id": "0590139e-7481-466c-bcdf-929adcaaf804",

        "name": "myservice",

        "path": "/",

        "port": 80,

        "protocol": "http",

        "read_timeout": 60000,

        "retries": 5,

        "updated_at": 1521554518,

        "write_timeout": 60000

    },

    "latencies": {

        "proxy": 1430,

        "kong": 9,

        "request": 1921

    },

    "client_ip": "127.0.0.1",

    "started_at": 1433209822425

}
</code>

Como requisito é necessário extrair as informações fornecidas dos arquivos, transformar as mesmas e salva-las em um banco de dados relacional.

## Ferramentas
Para a implementação deste teste, as seguintes bibliotecas, bancos e frameworks foram escolhidos:

Apache Airflow - https://airflow.apache.org/
Mysql - https://www.mysql.com/
Docker compose - https://docs.docker.com/compose/

## Como começar

### Clone o projeto 
<code> git clone https://github.com/FrancineMoraes/python-airflow-etl.git </code>

### Ambiente

Após clonar o projeto, para configurar o ambiente você deve rodar o comando dentro da pasta do projeto
<code> docker-compose up -d </code>

Apos a criação dos containers, entre no container do mysql e execute o tables.sql que está situado em dags/database/
<code> source tables.sql</code>

Ou se preferir, copie o sql do tables.sql, entre no container e cole o script lá!

### Url de acesso
Após estes passos, a url de acesso para o projeto é localhost:8080
