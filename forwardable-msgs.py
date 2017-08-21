import socket
import hashlib
import signal
import sys

class TimeoutError(Exception):
    pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_address = '0.0.0.0'
client_rcv_port = int(sys.argv[1])
client = (client_address, client_rcv_port)
sock.bind(client)

print("This socket identified by: " + client_address + ":" + str(client_rcv_port))

server_ip = sys.argv[2]
server_port = int(sys.argv[3])

def hash(message):
    utf8_message = message.encode('utf-8')
    return hashlib.sha224(utf8_message).hexdigest()

def package_message(message):
    checksum = hash(message)
    # checksum is 28 bytes
    return (checksum + message).encode('utf-8')

def wait_for_ack(payload):
    response = None
    while response != "ACK".encode('utf-8'):
        sock.sendto(payload, (server_ip, server_port))
        print("sent: " + str(payload))
        socket_response, response_address = sock.recvfrom(1024)
        response = socket_response
        print("response: ", response)

def _handle_timeout(signum, frame):
    raise TimeoutError("timed out")
    
while True:
    message = input('Enter a string to be echoed: ')
    packaged_message = package_message(message)

    # give the client three seconds to respond
    retrying = True
    while retrying:
        try:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(3)
            wait_for_ack(packaged_message)
        except TimeoutError:
            continue
        retrying = False
        signal.alarm(0)
