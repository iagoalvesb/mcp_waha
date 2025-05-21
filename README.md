# Projeto para disciplina TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES E APLICAÇÕES 1

Implemataçãod do protocolo MCP com Whatsapp utilizando Waha. PS: Sistema operacional Linux.

### Links de suporte:
> https://modelcontextprotocol.io/quickstart/server

### 1) Instalações
> curl -LsSf https://astral.sh/uv/install.sh | sh
> docker pull devlikeapro/waha

### 2) Execução
> Inicializar o container com docker run -it --rm -p 3000:3000/tcp --name waha devlikeapro/waha
> Entrar no dashboard http://localhost:3000/dashboard
> Logar no Whatsapp. A imagem abaixo exemplifica como fazer isso (clicar em Start e, em seguida, escanear o QR Code
![image](https://github.com/user-attachments/assets/b4d1d1b1-6f08-43e6-8631-3ac95091e1fe)

Rodar no terminal:
```
#Create a new directory for our project
uv init weather
cd weather
#Create virtual environment and activate it
uv venv
source .venv/bin/activate
#Install dependencies
uv add "mcp[cli]" httpx
#Create our server file
touch weather.py
```

Então, substitua o arquivo "weather.py" pelo presente neste repositório

Rode o MCP por meio de ```python weather.py```

### 3) Resultados:
Temos duas ferramentas: 
send_message: Envia uma mensagem para uma pessoa com base no número dela (necessita do código internacional).
send_message_by_name: Envia mensagem para um uma pessoa com nome cadastrado.
Aqui está o resultado final da aplicação
![image](https://github.com/user-attachments/assets/453bafe2-2492-47f8-baf4-936032f02a45)
