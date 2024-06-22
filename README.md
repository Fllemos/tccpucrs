# tccpucrs

## Vita
Boot Telegram para TCC de ciência de dados e IA

## TODO 

- [x] estruturar o protótipo para conversa via telegram
- [x] fazer a conexão com a api da opeanai
- [x] ajustar instruções para obter em quase 100% as respostas desejadas 
- [x] adicionar parser do json recebido
- [x] escolher o banco de dados não relacional para uso local -> mongoDB via docker
- [x] Criar collection users e controlar o fluxo de usuários utilizando o bot
- [x] controlar as conversas por usuário do telegram
- [x] manter o histórico de conversas no banco de dados  -> manter o historico no mongoDB
- [x] manter os registros de dieta no banco de dados
- [x] fluir a conversa de acordo com o histórico de dietas e atualizar de acordo com a conversa
- [x] Ajustar atualizacao de dieta já cadastrada
- [x] adicionar input/output de áudio ao bot 
- [x] adicionar input de imagem ao bot 
- [x] adicionar comando de download de histórico de dieta 
- [x] testar resumos, calcular calorias e informar os dados
- [x] deploy da aplicação em servidor próprio
- [x] alterar prints por uma lib de logs, com ativacao ou nao de debug 
- [ ] refactor e testes após deploy e ajuste contínuo até o momento da entrega


## Pré-requisitos
Antes de iniciar, você precisará:
- Docker e Docker Compose instalados
- Uma conta no Telegram para criar um bot através do @BotFather
- Uma conta na OpenAI para obter as credenciais de API

## Configuração
1. **Clonar o repositório:**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd [NOME_DO_DIRETORIO]
   ```

2. **Configurar variáveis de ambiente:**
Copie o arquivo .env_example para .env e substitua os valores pelas suas chaves de API e outras configurações necessárias:
  ```bash
    cp .env_example .env
    # Edite o arquivo .env com suas próprias credenciais
  ```
  Lembre-se de que a variável BOT_SECRET deve conter uma palavra-passe para que usuários possam cadastrar-se pelo comando /cadastrar BOT_SECRET

3. **Construir e executar containers:**
Use o Docker Compose para construir e iniciar os serviços necessários:
  ```bash
    docker compose build
    docker compose up -d
  ```

## Verificar instalação
Após iniciar os serviços com Docker Compose, verifique se os containers estão rodando corretamente:
  ```bash
    docker compose ps
  ```
Para visualizar os logs do bot em tempo real:
  ```bash
    docker compose logs -f bot
  ```

## Troubleshooting
Se encontrar problemas com ffmpeg e pydub, assegure-se de que o ffmpeg está corretamente instalado no Dockerfile.<br>
Para problemas de conexão com MongoDB, verifique se a string de conexão no .env está correta e corresponde ao serviço configurado no docker-compose.yml.<br>
Este projeto rodou docker em:<br>
  ```bash
        Distributor ID:	ManjaroLinux
        Description:	Manjaro Linux
        Release:	23.1.4
        Codename:	Vulcan
  ```

Em caso de problemas para executar via docker, pode ser realizada a instalação local das bibliotecas python e do mongodb.


<br>


<p align="center">
  <img src="assets/vita_avatar.png" alt="Em construção..." width="400" height="400"><br>
  <em>Em construção...</em>
</p>



