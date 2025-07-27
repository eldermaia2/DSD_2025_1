<template>
  <div class="container">
    <h1>Calculadora de Notas IFRN</h1>
    <form @submit.prevent="enviarNotas">
      <label>Nota 1:</label>
      <input v-model="nota1" type="number" min="10" max="100" required />

      <label>Nota 2:</label>
      <input v-model="nota2" type="number" min="10" max="100" required />

      <button type="submit">Calcular</button>
    </form>

    <div
      v-if="resultado"
      class="resultado"
      :class="{ final: resultado.situacao === 'Final', aprovado: resultado.situacao === 'Aprovado' }"
    >
      <h2>Resultado</h2>
      <p>Média: {{ resultado.media }}</p>
      <p>Situação: {{ resultado.situacao }}</p>
      <p v-if="resultado.situacao === 'Final'">
        Nota necessária na final: {{ resultado.nota_final }}
      </p>
    </div>

    <div v-if="erro" class="erro">{{ erro }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const nota1 = ref('')
const nota2 = ref('')
const resultado = ref(null)
const erro = ref(null)

const enviarNotas = async () => {
  try {
    const response = await axios.post('http://localhost:3000/notas', {
      nota1: parseFloat(nota1.value),
      nota2: parseFloat(nota2.value),
    })
    resultado.value = response.data
    erro.value = null
  } catch {
    erro.value = 'Erro ao comunicar com o servidor.'
  }
}
</script>

<style>
.container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  text-align: center;
  font-family: Arial, sans-serif;
}

input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
}

button {
  background: #42b983;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.resultado {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
  color: white;
}

.resultado.aprovado {
  background: #038312b8; /* verde */
}

.resultado.final {
  background: #d9534f; /* vermelho */
}

.erro {
  color: rgba(255, 0, 0, 0.761);
  margin-top: 10px;
}
</style>