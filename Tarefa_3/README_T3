# Serviço de Cálculo de Notas IFRN com gRPC

![gRPC](https://img.shields.io/badge/gRPC-1.2.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)

Este projeto implementa um sistema distribuído para cálculo de notas de alunos do IFRN usando gRPC para comunicação entre serviços em Python (servidor) e Node.js (cliente).

## 📋 Funcionalidades

- Calcula a média ponderada de duas notas (pesos 2 e 3)
- Determina se o aluno está aprovado ou precisa de prova final
- Calcula a nota mínima necessária na prova final para aprovação
- Comunicação entre serviços usando gRPC

## 🛠️ Tecnologias

- **gRPC** - Framework para comunicação entre serviços
- **Protocol Buffers** - Definição do contrato de serviço
- **Python** - Implementação do servidor
- **Node.js** - Implementação do cliente

## 📂 Estrutura do Projeto
```
grpc-notas/
├── proto/
│ └── notas.proto # Definição do serviço gRPC
├── server/
│ ├── server.py # Servidor em Python
│ ├── notas_pb2.py # Gerado pelo protoc
│ └── notas_pb2_grpc.py # Gerado pelo protoc
├── client/
│ └── client.js # Cliente em Node.js
└── README.md
```


## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Node.js 18+
- gRPC (instalado via dependências)

### Configuração do Servidor (Python)

```bash
cd server
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/notas.proto
```

### Configuração do Cliente (Node.js)

```bash
cd client
npm install @grpc/grpc-js @grpc/proto-loader
```

## 🚀 Como Executar

1\. Inicie o servidor (em um terminal):

```bash
cd server
python server.py
```

2\. Execute o cliente (em outro terminal):

```bash
cd client
node client.js
```

## 💻 Exemplo de Saída

```bash
Média: 4.80
Situação: Prova final
Nota necessária na final: 7.20
```

## 📊 Regras de Cálculo

### Fórmulas de Cálculo

| Descrição | Fórmula | Exemplo |
|-----------|---------|---------|
| **Média Parcial** | `(nota1 × 2 + nota2 × 3) / 5` | (5.0×2 + 6.0×3)/5 = 5.6 |
| **Situação do Aluno** | `Média ≥ 6.0 → Aprovado`<br>`Média < 6.0 → Prova Final` | 5.6 → Prova Final |
| **Nota Necessária na Final** | `max(0, 12 - Média Parcial)` | 12 - 5.6 = 6.4 |