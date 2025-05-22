import socket
import json
from threading import Thread

class CurrencyServer:
    def __init__(self):
        self.rates = {
            'USD': 1.0,
            'BRL': 5.04,
            'EUR': 0.92,
            'GBP': 0.79,
            'JPY': 151.50
        }
        self.tcp_port = 12345
        self.udp_port = 12346

    def handle_tcp_client(self, conn, addr):
        print(f"Conexão TCP estabelecida com {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                try:
                    request = json.loads(data.decode())
                    response = self.convert_currency(request)
                    conn.sendall(json.dumps(response).encode())
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    conn.sendall(json.dumps({'error': str(e)}).encode())
        except ConnectionError:
            pass
        finally:
            conn.close()
            print(f"Conexão TCP com {addr} encerrada")

    def handle_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', self.udp_port))
        print(f"Servidor UDP ouvindo na porta {self.udp_port}")
        
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                request = json.loads(data.decode())
                response = self.convert_currency(request)
                sock.sendto(json.dumps(response).encode(), addr)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                sock.sendto(json.dumps({'error': str(e)}).encode(), addr)

    def convert_currency(self, request):
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

    def start(self):
        # Inicia servidor TCP
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(('0.0.0.0', self.tcp_port))
        tcp_socket.listen(5)
        print(f"Servidor TCP ouvindo na porta {self.tcp_port}")
        
        # Inicia servidor UDP em uma thread separada
        udp_thread = Thread(target=self.handle_udp, daemon=True)
        udp_thread.start()
        
        try:
            while True:
                conn, addr = tcp_socket.accept()
                client_thread = Thread(target=self.handle_tcp_client, args=(conn, addr), daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado")
            tcp_socket.close()

if __name__ == "__main__":
    server = CurrencyServer()
    server.start()