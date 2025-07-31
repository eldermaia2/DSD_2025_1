# Integração de APIs REST e SOAP com API Gateway
<!--
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Vue.js](https://img.shields.io/badge/Vue-3-green)
![Arquitetura](https://img.shields.io/badge/REST%2FSOAP-Gateway-blue)-->

Este projeto demonstra a integração de serviços REST e SOAP utilizando um **API Gateway** desenvolvido com Node.js, além de um cliente web feito em Vue.js.

## 🎯 Objetivo

Construir uma arquitetura distribuída que integra diferentes estilos de API (REST e SOAP), oferecendo uma única interface por meio de um API Gateway. A aplicação simula um sistema de cálculo de médias semestrais de alunos.

## 📂 Estrutura do Projeto

```
grpc-ifrn-integrado/
├── api-gateway/          # Gateway (Node.js)
│   ├── index.html
│   ├── index.js
│   ├── package-lock.json
│   ├── package.json
├── cliente-web/          # Cliente Web simples (HTML + JS)
│   ├── index.html
├── frontend-ifrn/        # Frontend moderno (Vue.js)
│   ├── .gitignore
│   ├── README.md
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── vite.config.js
│   ├── .vscode/
│   │   ├── extensions.json
│   ├── public/
│   │   ├── vite.svg
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── style.css
│   │   ├── assets/
│   │   │   ├── vue.svg
│   │   ├── components/
│   │   │   ├── HelloWorld.vue
├── rest-media/           # API REST (Python Flask)
│   ├── app.py
├── soap-final/           # Servidor SOAP (Python + Spyne)
│   ├── servidor.py
```
## 🛠️ Tecnologias Utilizadas

- **Node.js** – API Gateway
- **Vue.js** – Cliente Web (frontend-ifrn)
- **Python Flask** – REST API (cálculo de médias)
- **Python Spyne** – SOAP Server
- **HTML/CSS/JS** – Cliente Web básico
- **Vite** – Build do Vue.js

## 🔄 Fluxo da Arquitetura

1. O **cliente web** acessa o **API Gateway**.
2. O **Gateway** se comunica com:
   - A **API REST** para cálculo de médias.
   - O **Servidor SOAP** para regras adicionais ou armazenamento.
3. O Gateway também implementa **HATEOAS**, oferecendo links navegáveis nos retornos JSON.

## 🔧 Como Executar

### 1. Servidor SOAP

```bash
cd soap-final
pip install spyne
pip install lxml
python servidor.py
```

### 2. API REST

```bash
cd rest-media
pip install flask
python app.py
```

### 3. API Gateway

```bash
cd api-gateway
npm install
node index.js
```

### 4. Frontend Vue.js

```bash
cd frontend-ifrn
npm install
npm run dev
```

### 5. Cliente Web (HTML simples)

Abra o arquivo `cliente-web/index.html` diretamente no navegador.

## 📄 WSDL

O servidor SOAP gera automaticamente o WSDL ao ser iniciado. As principais tags observadas são:

- `<wsdl:definitions>`
- `<wsdl:message>`
- `<wsdl:portType>`
- `<wsdl:binding>`
- `<wsdl:service>`

## 🌐 HATEOAS no Gateway

O Gateway responde com objetos JSON que incluem links navegáveis para outras ações, seguindo o estilo REST HATEOAS.

Exemplo de resposta:
```json
{
  "media": 7.0,
  "situacao": "Aprovado",
  "links": [
    { "rel": "self", "href": "/media" },
    { "rel": "prova-final", "href": "/prova-final" }
  ]
}
```

## 🧪 Testes e Clientes em Linguagens Diferentes

O servidor SOAP foi testado com clientes em Python e Node.js utilizando bibliotecas como `zeep` e `soap`.

## ✅ Requisitos Atendidos

- [x] API Gateway implementado
- [x] Integração REST + SOAP
- [x] HATEOAS
- [x] Cliente Web
- [x] Documentação (este README)
- [x] Servidor SOAP com WSDL gerado
- [x] Cliente e servidor em linguagens diferentes
- [x] Projeto funcional para apresentação

## 📌 Observações

- Linguagens: Python 3.10+ e Node.js 18+
- O projeto pode ser executado em ambientes separados ou em containers Docker (opcional)



---

Desenvolvido para a disciplina de Sistemas Distribuídos.
