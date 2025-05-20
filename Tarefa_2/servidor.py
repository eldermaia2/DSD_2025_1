import asyncio
import json

class CurrencyServer:
    def __init__(self):
        self.rates = {
            'USD': 1.0,    # Dólar Americano (base)
            'BRL': 5.04,   # Real Brasileiro
            'EUR': 0.92,   # Euro
            'GBP': 0.79,   # Libra Esterlina
            'JPY': 151.50  # Iene Japonês
        }
        self.tcp_port = 12345
        self.udp_port = 12346

    async def handle_tcp(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Conexão TCP estabelecida com {addr}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                try:
                    request = json.loads(data.decode())
                    response = self.convert_currency(request)
                    writer.write(json.dumps(response).encode())
                    await writer.drain()
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    writer.write(json.dumps({'error': str(e)}).encode())
                    await writer.drain()
        except ConnectionError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"Conexão TCP com {addr} encerrada")

    def connection_made(self, transport):
        self.udp_transport = transport

    def datagram_received(self, data, addr):
        try:
            request = json.loads(data.decode())
            response = self.convert_currency(request)
            self.udp_transport.sendto(json.dumps(response).encode(), addr)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.udp_transport.sendto(json.dumps({'error': str(e)}).encode(), addr)

    def convert_currency(self, request):
        """Realiza a conversão de moeda"""
        from_curr = request['from'].upper()
        to_curr = request['to'].upper()
        amount = float(request['amount'])
        
        if from_curr not in self.rates or to_curr not in self.rates:
            raise ValueError('Moeda não suportada')
        
        converted = amount * self.rates[to_curr] / self.rates[from_curr]
        return {
            'from': from_curr,
            'to': to_curr,
            'amount': amount,
            'converted': round(converted, 2),
            'rate': round(self.rates[to_curr] / self.rates[from_curr], 6)
        }

    async def run(self):
        # Inicia servidor TCP
        tcp_server = await asyncio.start_server(
            self.handle_tcp, '0.0.0.0', self.tcp_port)
        
        # Inicia servidor UDP
        loop = asyncio.get_running_loop()
        udp_server = await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=('0.0.0.0', self.udp_port))
        
        print(f"Servidor de conversão iniciado. TCP: {self.tcp_port}, UDP: {self.udp_port}")
        print(f"Cotações: {self.rates}")
        
        async with tcp_server:
            await tcp_server.serve_forever()

async def main():
    server = CurrencyServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor encerrado")