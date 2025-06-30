from concurrent import futures
import grpc
import notas_pb2
import notas_pb2_grpc

class NotaService(notas_pb2_grpc.NotaServiceServicer):
    def CalcularNota(self, request, context):
        nota1 = request.nota1
        nota2 = request.nota2
        
        media = (nota1 * 2 + nota2 * 3) / 5
        aprovado = media >= 6
        nota_final_necessaria = max(0.0, 12 - media)
        reprovado = not aprovado and nota_final_necessaria > 10.0
        
        return notas_pb2.NotaResponse(
            media=media,
            aprovado=aprovado,
            reprovado=reprovado,
            nota_final_necessaria=nota_final_necessaria
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notas_pb2_grpc.add_NotaServiceServicer_to_server(NotaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor rodando na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()