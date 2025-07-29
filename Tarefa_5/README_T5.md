# Sistema de Cálculo de Notas com RabbitMQ (Fila de Mensagens)

Este projeto implementa uma arquitetura simples utilizando **RabbitMQ** como *Message Broker*.  
Ele simula o envio e processamento de notas de alunos, seguindo as regras do **IFRN**.

---

## 📌 Funcionalidades

- **Produtor (Node.js)**: envia mensagens para uma fila (`notas`).
- **Consumidor (Python)**: recebe as mensagens, calcula a média e determina a situação do aluno:
  - Aprovado
  - Prova Final
  - Reprovado
- **RabbitMQ**: faz a intermediação entre produtor e consumidor.
- **Docker**: utilizado para subir o servidor RabbitMQ rapidamente.

---

## 📁 Estrutura de Pastas

```
projeto-rabbitmq/
├── producer-node/
│   ├── producer.js
│   └── package.json
├── consumer-python/
│   └── consumer.py
└── README_T4.md
```

---

## 🐇 1. Subindo o RabbitMQ com Docker

Antes de executar o produtor e o consumidor, inicie o RabbitMQ com o seguinte comando:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

- Painel de administração: [http://localhost:15672](http://localhost:15672)
- Usuário: `guest`
- Senha: `guest`

---

## 🚀 2. Executando o Produtor (Node.js)

1. Abra um terminal e vá até a pasta `producer-node`:

```bash
cd producer-node
```

2. Instale as dependências:

```bash
npm install amqplib
```

3. Execute o produtor e insira as notas via terminal:

```bash
node producer.js
```

Você poderá digitar valores de **0 a 100** diretamente no terminal.

---

## 🐍 3. Executando o Consumidor (Python)

1. Abra outro terminal e vá até a pasta `consumer-python`:

```bash
cd consumer-python
```

2. Instale a biblioteca `pika`:

```bash
pip install pika
```

3. Execute o consumidor:

```bash
python consumer.py
```

4. O consumidor ficará aguardando as mensagens:

```
Aguardando mensagens. CTRL+C para sair
```

---

## 🧮 Lógica de Cálculo

- **Média** = (nota1 × 2 + nota2 × 3) / 5

### Situações:
- **Média ≥ 60**: Aprovado ✅
- **40 ≤ Média < 60**: Prova Final (é calculada a nota mínima necessária para aprovação) 📘
- **Nota necessária > 100**: Reprovado diretamente ❌

---

## 🔄 Fluxo do Sistema

```
[Node.js Producer] → [RabbitMQ Queue] → [Python Consumer]
```

---

## 📝 Licença

Este projeto é de uso acadêmico, feito como tarefa prática utilizando integração entre Node.js, Python e RabbitMQ.
