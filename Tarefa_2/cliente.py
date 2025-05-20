import asyncio
import json
import argparse

class UDPClientProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.response = None
        self.response_event = asyncio.Event()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.response = json.loads(data.decode())
        self.response_event.set()

    def error_received(self, exc):
        print(f"Erro na comunicação: {exc}")

    def connection_lost(self, exc):
        print("Conexão UDP encerrada")

class CurrencyClient:
    async def tcp_convert(self, host, port):
        reader, writer = await asyncio.open_connection(host, port)
        print("\nConversor de Moedas (TCP)")
        print("Moedas disponíveis: USD, BRL, EUR, GBP, JPY")
        print("Digite 'sair' para encerrar\n")
        
        try:
            while True:
                from_curr = input("De (ex: BRL): ").upper()
                if from_curr.lower() == 'sair':
                    break
                
                to_curr = input("Para (ex: USD): ").upper()
                if to_curr.lower() == 'sair':
                    break
                
                amount = input("Valor: ")
                if amount.lower() == 'sair':
                    break
                
                try:
                    request = {
                        'from': from_curr,
                        'to': to_curr,
                        'amount': float(amount)
                    }
                    
                    writer.write(json.dumps(request).encode())
                    await writer.drain()
                    
                    data = await reader.read(1024)
                    response = json.loads(data.decode())
                    
                    if 'error' in response:
                        print(f"\nErro: {response['error']}\n")
                    else:
                        print(f"\n{amount} {from_curr} = {response['converted']:.2f} {to_curr}")
                        print(f"Taxa: 1 {from_curr} = {response['rate']:.6f} {to_curr}\n")
                except ValueError:
                    print("\nValor inválido. Use números (ex: 100.50)\n")
        finally:
            writer.close()
            await writer.wait_closed()

    async def udp_convert(self, host, port):
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPClientProtocol(),
            remote_addr=(host, port))
        
        print("\nConversor de Moedas (UDP)")
        print("Moedas disponíveis: USD, BRL, EUR, GBP, JPY")
        print("Digite 'sair' para encerrar\n")
        
        try:
            while True:
                from_curr = input("De (ex: BRL): ").upper()
                if from_curr.lower() == 'sair':
                    break
                
                to_curr = input("Para (ex: USD): ").upper()
                if to_curr.lower() == 'sair':
                    break
                
                amount = input("Valor: ")
                if amount.lower() == 'sair':
                    break
                
                try:
                    request = {
                        'from': from_curr,
                        'to': to_curr,
                        'amount': float(amount)
                    }
                    
                    protocol.response_event.clear()
                    transport.sendto(json.dumps(request).encode())
                    
                    try:
                        await asyncio.wait_for(protocol.response_event.wait(), timeout=5.0)
                        response = protocol.response
                        
                        if 'error' in response:
                            print(f"\nErro: {response['error']}\n")
                        else:
                            print(f"\n{amount} {from_curr} = {response['converted']:.2f} {to_curr}")
                            print(f"Taxa: 1 {from_curr} = {response['rate']:.6f} {to_curr}\n")
                    except asyncio.TimeoutError:
                        print("\nTempo de espera esgotado. Nenhuma resposta recebida.\n")
                except ValueError:
                    print("\nValor inválido. Use números (ex: 100.50)\n")
        finally:
            transport.close()

async def main():
    parser = argparse.ArgumentParser(description="Cliente de Conversão de Moedas")
    parser.add_argument('--host', default='localhost', help="Endereço do servidor")
    parser.add_argument('--tcp', type=int, default=12345, help="Porta TCP do servidor")
    parser.add_argument('--udp', type=int, default=12346, help="Porta UDP do servidor")
    parser.add_argument('--protocol', choices=['tcp', 'udp'], required=True, help="Protocolo a ser usado")
    
    args = parser.parse_args()
    
    client = CurrencyClient()
    
    if args.protocol == 'tcp':
        await client.tcp_convert(args.host, args.tcp)
    else:
        await client.udp_convert(args.host, args.udp)

if __name__ == "__main__":
    asyncio.run(main())