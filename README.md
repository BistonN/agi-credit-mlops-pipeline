# AGI Credit MLOps Pipeline

Pipeline completo de MLOps para treinamento, versionamento e disponibilização de um modelo de crédito via API, com automação CI/CD.

## Configurações

1. Este projeto utiliza variáveis de ambiente centralizadas em um arquivo .`env` no diretório raiz do projeto, seguindo o modelo .env.example.:

```BASH
DATA_PATH=/app/data/application_train.csv
MODEL_OUTPUT_PATH=/app/artifacts

MODEL_PATH=/app/artifacts/model_v1.rds
ENV=dev

JWT_SECRET=agisecretkey
FEATURE_METADATA_PATH=
```

2. O dataset de treinamento deve estar disponível no diretório:

```BASH
training/data/application_train.csv
```

Download

```BASH
wget -O training/data/application_train.csv "https://www.dropbox.com/scl/fi/hmhnf33bbapvpsq6becmo/application_train.csv?rlkey=t9i95h11b1uyc6dsh6s40z3x4&st=xzu9ijx2&dl=0"
```

3. Execução local para subir todos os servições:

```BASH
docker compose up --build
```

Execução separada:

```BASH
docker compose run training
docker compose run api
```

4. O gatilho da pipeline esta configurada para *push* na *branch* `main`

## Arquitetura

O versionamento do projeto foi criado em 3 *branchs* de desenvolvimento: **`feature/training-container`**, **`feature/api`** e **`feature/pipelineCICD`**. Conforme as funcionalidades foram desenvolvidas nessas *branchs* e chegando a versões estáveis, *pull requests* foram criados para
uma *branch*  **`develop`** que armazenava versões completas e estáveis. E após os testes e validações, foi subido para o que seria a *branch* de produção **`main`** que ativa o gatilho de execução do pipeline no `Github Actions`.

### feature/training-container

Para o ambiente de treinamento foi implementado um processo de versionamento automático via script shell (`versioning.sh`), executado imediatamente após o treinamento.

Esse script é responsável por:

- Criar e organizar a estrutura de armazenamento dos modelos;
- Versionar automaticamente cada novo modelo treinado;
- Atualizar um único arquivo `metadata.json` com histórico e versão ativa (que em produção obviamente deveria ser salva em um banco de dados garantindo a segurança das informações).

O script `train.R` permanece inalterado e sempre gera `model_v1.rds`. A responsabilidade de versionamento não fica com o time de Data Science, mas sim com o pipeline de engenharia.

Essa decisão procura simular um ambiente real de produção, onde:

- O time de cientistas entrega apenas o código do modelo;
- O pipeline gerencia versionamento, organização e governança;
- Novas versões podem ser promovidas sem modificar a lógica da API.

Com isso, reduz-se o acoplamento entre times e aumenta-se a confiabilidade do processo de deploy.

### feature/api

A API de inferência foi desenvolvida em **Flask**, integrando Python com R para execução dos modelos treinados.

Embora o pipeline de treinamento utilize R (o que permitiria uma API nativa em Plumber), foi adotada uma arquitetura híbrida para refletir cenários reais de produção, onde diferentes times e linguagens convivem no mesmo ecossistema.

No container da API:

- O R é instalado para carregar e executar os modelos (`.rds`);
- O Flask é responsável pela orquestração das rotas e validações;
- A comunicação entre Python e R é feita via `rpy2`.

Além disso, a API implementa:

- Autenticação via JWT;
- Validação automática de schema de features por versão de modelo;
- Suporte a múltiplas versões de modelos por parâmetro opicionais de rota;
- Logging estruturado e tratamento de erros.

Essa abordagem garante flexibilidade tecnológica sem comprometer governança, versionamento e segurança, aproximando o projeto de um ambiente real de produção.

Para ver todos os detalhes da  documentação e exemplos de requisições acesse a documentação da api em **[agi-api](https://documenter.getpostman.com/view/5769454/2sBXcEkLtG)**

#### Rotas:

- **/health**
  Retorna o status da API

```BASH
curl --location '{{url}}/health'
```

Response example:

```JSON
{
"status":  "ok"
}
```

- **/login**
  Gera o JWToken para autenticar rotas não públicas

```BASH
curl --location '{{jwt}}/login' \
--header 'Content-Type: application/json' \
--data '{ 
    "username": "admin", 
    "password": "123456" 
}'
```

Response example:

```JSON
{
    "token": "{{jwt}}"
}
```

- **/model_info**
  Gera o JWToken para autenticar rotas não públicas

```BASH
curl --location '{{url}}/model-info' \
--header 'Authorization: Bearer {{jwt}}
```

Response example:

```JSON
{
    "current_version": "v2",
    "models": [
        {
            "created_at": "2026-02-22 01:34:15",
            "features": [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "DAYS_BIRTH",
                "AMT_GOODS_PRICE"
            ],
            "version": "v1"
        },
        {
            "created_at": "2026-02-22 02:05:17",
            "features": [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "DAYS_BIRTH",
                "AMT_GOODS_PRICE"
            ],
            "version": "v2"
        }
    ]
}
```

- **/predict**
  Disponibiliza a previsão do modelo selecionado (ultiliza a ultima versão caso não seja especificado qual o modelo)

```BASH
curl --location '{{url}}/predict' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {{jwt}}' \
--data '{
    "AMT_INCOME_TOTAL":5000,
    "AMT_CREDIT":200000,
    "DAYS_BIRTH":-12000,
    "AMT_GOODS_PRICE":180000
}'
```

Response example:

```JSON
{
    "model_version": "v2",
    "prediction": 0,
    "prob_default": 0.10734710579372096
}
```

### feature/pipelineCICD

O workflow automatizado executa:

- Lint do código Python
- Build das imagens Docker
- Execução do treinamento do modelo
- Validação dos artefatos gerados
- Build da API
- Teste de integração via endpoint /health
- Geração automática de tags de imagem
- Cache de dependências para acelerar builds
- Usa variaveis de ambiente configuradas no Github Secrets
- A pipeline é acionada em push para:
  - main
  - test/**

O processo simula um fluxo real de produção sem necessidade de push para registry.
