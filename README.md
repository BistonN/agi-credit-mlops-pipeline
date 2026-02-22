
# AGI Credit MLOps Pipeline
Pipeline completo de MLOps para treinamento, versionamento e disponibilização de um modelo de crédito via API, com automação CI/CD.

## Arquitetura
O versionamento do projeto foi criado em 3 *branchs* de desenvolvimento: **`feature/training-container`**, **`feature/api`** e **`feature/pipelineCICD`**. Conforme as funcionalidades foram desenvolvidas nessas *branchs* e chegando a versões estáveis, *pull requests* foram criados para
uma *branch*  **`develop`** que armazenava versões completas e estáveis. E após os testes e validações, foi subido para o que seria a *branch* de produção **`main`**.
### feature/training-container
Para o ambiente de treinamento foi implementado um processo de versionamento automático via script shell (`versioning.sh`), executado imediatamente após o treinamento.

Esse script é responsável por:

- Criar e organizar a estrutura de armazenamento dos modelos;
- Versionar automaticamente cada novo modelo treinado;
- Atualizar um único arquivo `metadata.json` com histórico e versão ativa (que em produção obviamente deveria ser salva em um banco de dados garantindo a segurança das informações).
  
O script `train.R` permanece inalterado e sempre gera `model_v1.rds`. A responsabilidade de versionamento não fica com o time de Data Science, mas sim com o pipeline de engenharia.

Essa decisão simula um ambiente real de produção, onde:
  
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
- Suporte a múltiplas versões de modelos por parâmetro de rota;
- Logging estruturado e tratamento de erros.

Essa abordagem garante flexibilidade tecnológica sem comprometer governança, versionamento e segurança, aproximando o projeto de um ambiente real de produção.

Algumas rotas tem parâmetros opicionais. Para ver toda documentação e exemplos de requisições acesse: **[agi-api](https://documenter.getpostman.com/view/5769454/2sBXcEkLtG)**
#### Rotas:
-  **/health**
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
-  **/login**
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
"status":  "ok"
}
```
-  **/model_info**
Gera o JWToken para autenticar rotas não públicas
```BASH
curl --location '{{url}}/model-info' \
--header 'Authorization: Bearer {{jwt}}
```
Response example:
```JSON

```