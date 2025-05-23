# DSD_2025_1
### Trabalhos da Disciplina DSD (Desenvolvimento de Sistemas Distribuídos)
- [Tarefa_1](./Tarefa_1)

- [Tarefa_2](./Tarefa_2)
 1. __O usuário executa:__  
python cliente.py --protocol tcp  # Usa TCP  
ou  
python cliente.py --host 0.0.0.0 --protocol udp  # Usa UDP
para executar remoto  

3. __O cliente:__
Conecta ao servidor (TCP) ou envia/recebe pacotes (UDP).  
Pede _moeda de origem, moeda destino e valor_.  
Envia os dados em _JSON_.  
Recebe a resposta e mostra o valor convertido.  

4. __Se houver erro__ (timeout, conexão perdida), avisa o usuário.
