# tccpucrs

## Vita
Bot Telegram para TCC de ciência de dados e IA

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
  Crie uma pasta de nome .credentials e inclua o JSON de credenciais do seu google TTS

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
  <em>Seu assistente de dieta</em>
</p>



