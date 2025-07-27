const express = require('express');
const axios = require('axios');
const soap = require('soap');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
app.use(express.json());
const cors = require("cors");
app.use(cors());

// ===== Swagger Config =====
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'API Gateway - IFRN Notas',
      version: '1.0.0',
      description: 'Gateway que integra REST e SOAP para calcular notas e situação do aluno.'
    },
  },
  apis: ['./index.js'], // importante
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// ===== Endpoint principal =====
/**
 * @openapi
 * /notas:
 *   post:
 *     summary: Calcula média e verifica situação
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nota1:
 *                 type: number
 *               nota2:
 *                 type: number
 *     responses:
 *       200:
 *         description: Resultado da média e situação do aluno
 */
app.post('/notas', async (req, res) => {
  const { nota1, nota2 } = req.body;

  try {
    const mediaResp = await axios.post('http://localhost:5000/calcular-media', { nota1, nota2 });
    const media = mediaResp.data.media;

    soap.createClient('http://localhost:8001/?wsdl', (err, client) => {
      if (err) return res.status(500).send("Erro ao criar cliente SOAP: " + err.message);

      client.verificarSituacao({ media }, (err, result) => {
        if (err) return res.status(500).send("Erro ao chamar serviço SOAP: " + err.message);

        res.json({
          media,
          situacao: result.verificarSituacaoResult.situacao,
          nota_final: result.verificarSituacaoResult.nota_final,
          links: [
            { rel: 'self', href: '/notas' },
            { rel: 'refazer', href: '/notas' }
          ]
        });
      });
    });
  } catch (err) {
    res.status(500).send("Erro ao comunicar com o serviço REST: " + err.message);
  }
});

// ===== Start Server =====
app.listen(3000, () => console.log('API Gateway rodando na porta 3000'));