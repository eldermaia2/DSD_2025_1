const amqp = require("amqplib");
const readline = require("readline");

async function sendMessage(nota1, nota2) {
  try {
    const connection = await amqp.connect("amqp://localhost");
    const channel = await connection.createChannel();

    const queue = "notas";
    await channel.assertQueue(queue, { durable: true });

    const msg = JSON.stringify({ nota1, nota2 });
    channel.sendToQueue(queue, Buffer.from(msg), { persistent: true });

    console.log("✅ Mensagem enviada:", msg);

    setTimeout(() => {
      connection.close();
      process.exit(0);
    }, 500);
  } catch (err) {
    console.error("Erro no produtor:", err);
  }
}

// Interface para ler do terminal
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question("Digite a primeira nota: ", (n1) => {
  rl.question("Digite a segunda nota: ", (n2) => {
    sendMessage(Number(n1), Number(n2));
    rl.close();
  });
});