import socket
import json
import argparse

class CurrencyClient:
    def tcp_convert(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
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
                        
                        s.sendall(json.dumps(request).encode())
                        data = s.recv(1024)
                        response = json.loads(data.decode())
                        
                        if 'error' in response:
                            print(f"\nErro: {response['error']}\n")
                        else:
                            print(f"\n{amount} {from_curr} = {response['converted']:.2f} {to_curr}")
                            print(f"Taxa: 1 {from_curr} = {response['rate']:.6f} {to_curr}\n")
                    except ValueError:
                        print("\nValor inválido. Use números (ex: 100.50)\n")
            except ConnectionError:
                print("\nConexão com o servidor perdida")

    def udp_convert(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
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
                        
                        s.sendto(json.dumps(request).encode(), (host, port))
                        s.settimeout(5.0)  # Timeout de 5 segundos
                        data, addr = s.recvfrom(1024)
                        response = json.loads(data.decode())
                        
                        if 'error' in response:
                            print(f"\nErro: {response['error']}\n")
                        else:
                            print(f"\n{amount} {from_curr} = {response['converted']:.2f} {to_curr}")
                            print(f"Taxa: 1 {from_curr} = {response['rate']:.6f} {to_curr}\n")
                    except socket.timeout:
                        print("\nTempo de espera esgotado. Nenhuma resposta recebida.\n")
                    except ValueError:
                        print("\nValor inválido. Use números (ex: 100.50)\n")
            except ConnectionError:
                print("\nErro na comunicação com o servidor")

def main():
    parser = argparse.ArgumentParser(description="Cliente de Conversão de Moedas")
    parser.add_argument('--host', default='localhost', help="Endereço do servidor")
    parser.add_argument('--tcp', type=int, default=12345, help="Porta TCP do servidor")
    parser.add_argument('--udp', type=int, default=12346, help="Porta UDP do servidor")
    parser.add_argument('--protocol', choices=['tcp', 'udp'], required=True, help="Protocolo a ser usado")
    
    args = parser.parse_args()
    
    client = CurrencyClient()
    
    if args.protocol == 'tcp':
        client.tcp_convert(args.host, args.tcp)
    else:
        client.udp_convert(args.host, args.udp)

if __name__ == "__main__":
    main()