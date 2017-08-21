import socket
import hashlib
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = int(sys.argv[1])

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

def hash(message):
    return hashlib.sha224(message).hexdigest().encode("utf-8")

# checksum is 28 bytes
def unwrap_payload(payload):
    checksum = payload[:56]
    message = payload[56:]

    return (checksum, message)


while True:
    payload, client_address = sock.recvfrom(1024)

    checksum, message = unwrap_payload(payload)

    print("received payload: ", message.decode("UTF-8"))

    if hash(message) != checksum:
        sock.sendto("NACK".encode("utf-8"), client_address)
    else:
        sock.sendto("ACK".encode("utf-8"), client_address)