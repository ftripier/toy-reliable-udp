import ast
import random
import socket
import sys
import traceback

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = int(input("Type the port number you desire for this socket: "))
reliability = float(input("Type the fraction of datagrams that should be dropped: "))
corruption_rate = float(input("Type the fraction of datagrams that should be corrupted: "))

proxy_client_ip = input("Type the proxy client's ip: ")
proxy_client_port = int(input("Type the proxy client's port: "))
proxy_client = (proxy_client_ip, proxy_client_port)

proxy_server_ip = input("Type the proxy server's ip: ")
proxy_server_port = int(input("Type the proxy server's port: "))
proxy_server = (proxy_server_ip, proxy_server_port)

client = (server_address, server_port)
sock.bind(client)
print("This socket identified by: " + server_address + ":" + str(server_port))

# disgusting hack
sender = None
responder = None

def send_back(payload, client_address):
    if client_address == proxy_server:
        sock.sendto(payload, proxy_client)
    elif client_address == proxy_client:
        sock.sendto(payload, proxy_server)
    else:
        raise Exception("sorry, only proxy client or proxy server traffic allowed: ", client_address)

while True:
    payload, client_address = sock.recvfrom(1024)
    print("\n===New Packet===")
    if random.random() < reliability:
        print("  Dropped packet: {}".format(payload))
        continue

    try:
        print("  Received payload: ", payload.decode("utf-8"))

        if random.random() < corruption_rate:
            payload = payload.decode("utf-8")
            corruption_index = random.randint(0, len(payload) - 1)
            corruption_bit_index = random.randint(0, len(payload[corruption_index]) - 1)
            new_character = chr(ord(payload[corruption_index]) ^ (1 << corruption_bit_index))
            corrupted_payload = payload[:corruption_index] + new_character + payload[corruption_index+1:]
            print("  Corruption event: {} became {}".format(payload, corrupted_payload))
            payload = corrupted_payload.encode("utf-8")

        send_back(payload, client_address)

    except:
        print("  Failed to handle: {}".format(payload))
        traceback.print_exc()
