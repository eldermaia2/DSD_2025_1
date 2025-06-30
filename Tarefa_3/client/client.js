const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const packageDefinition = protoLoader.loadSync('../proto/notas.proto', {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const grpcObject = grpc.loadPackageDefinition(packageDefinition);
const NotaService = grpcObject.NotaService;
const cliente = new NotaService('localhost:50051', grpc.credentials.createInsecure());

async function obterNotas() {
    return new Promise((resolve) => {
        rl.question('Digite a primeira nota (peso 2): ', (nota1) => {
            rl.question('Digite a segunda nota (peso 3): ', (nota2) => {
                resolve({
                    nota1: parseFloat(nota1),
                    nota2: parseFloat(nota2)
                });
            });
        });
    });
}

async function main() {
    console.log('=== Calculadora de Notas IFRN ===');
    
    const { nota1, nota2 } = await obterNotas();
    
    if (isNaN(nota1) || isNaN(nota2)) {
        console.log('Por favor, informe valores numéricos válidos');
        rl.close();
        return;
    }

    console.log('\nProcessando...\n');
    
    cliente.CalcularNota({ nota1, nota2 }, (err, response) => {
        rl.close();
        
        if (err) {
            console.error("Erro:", err);
            return;
        }
        
        console.log("Resultado:");
        console.log("Nota 1:", nota1);
        console.log("Nota 2:", nota2);
        console.log("Média:", response.media.toFixed(2));
        
        const notaFinal = response.nota_final_necessaria ?? response.notaFinalNecessaria ?? 0;
        
        if (response.reprovado) {
            console.log("Situação: ❌ Reprovado direto");
            console.log("Motivo: Precisaria de", notaFinal.toFixed(2), "na final");
        } else if (response.aprovado) {
            console.log("Situação: ✅ Aprovado");
        } else {
            console.log("Situação: ⚠ Prova final");
            console.log("Nota necessária na final:", notaFinal.toFixed(2));
        }
    });
}

main();