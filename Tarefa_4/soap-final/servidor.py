from spyne import Application, rpc, ServiceBase, Float, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class SituacaoResponse(ComplexModel):
    situacao = str
    nota_final = float

class FinalService(ServiceBase):
    @rpc(Float, _returns=SituacaoResponse)
    def verificarSituacao(ctx, media):
        if media >= 60:  # aprovado direto
            return SituacaoResponse(situacao='Aprovado', nota_final=0.0)
        else:
            # cálculo da nota necessária na prova final (escala 0–100)
            nota_final = (60 * 2) - media
            nota_final = round(nota_final, 2)

            if nota_final > 100:
                return SituacaoResponse(situacao='Reprovado', nota_final=0.0)
            else:
                return SituacaoResponse(situacao='Final', nota_final=nota_final)

app = Application([FinalService], 'ifrn.soap.final',
                  in_protocol=Soap11(), out_protocol=Soap11())
wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("🚀 Servidor SOAP rodando em http://localhost:8001")
    server = make_server('0.0.0.0', 8001, wsgi_app)
    server.serve_forever()