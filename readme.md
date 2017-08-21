## Creating Reliable Transport

This folder contains 3 *very simplistic* Python servers to demonstrate the use of the Socket interface in Python, but also to be used as tools to simulate lossy network behavior. Take a look at the simplest of these servers, `udp-print-server.py`:

```Python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = int(input("Type the port number you desire: "))

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

while True:
    payload, client_address = sock.recvfrom(1024)
    print("received payload: ", str(payload))
```

This server simple listens for messages over UDP on a specific port, and prints them out. Note that the server will only accept the first 1024 bytes of data sent in any particular UDP datagram. This socket is told to use the Internet Protocol, and the UDP protocol on this line: `sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`. For more information on using other protocols see [the docs](https://docs.python.org/3/library/socket.html).

Your goal will be to write your own client and server programs that can reliably communicate across a lossy channel. Our lossy channel is the `forward-unreliable-udp.py` server.

## Getting Started

To explore the data format used, and see the servers and clients in action, you should run them on your localhost. Try the following from your terminal:

Tab one:  
```
python3 udp-print-server.py
Type the port number you desire: 1337
Listening on 0.0.0.0:1337
```

Tab two:
```
python3 forward-unreliable-udp.py
Type the port number you desire for this socket: 1338
Type the fraction of datagrams that should be dropped: .3
Type the fraction of datagrams that should be corrupted: .3
This socket identified by: 0.0.0.0:1338
```

Tab three:
```
python3 forwardable-msgs.py
Type the port number you desire for this socket: 1339
This socket identified by: 0.0.0.0:1339
Enter the ip address you wish to send to: 0.0.0.0
Type the port number you wish to send to: 1338
Enter the ip address to forward this message to: 0.0.0.0
Enter the port to be forwarded to: 1337
Enter a string to be echoed: hello
```

In tab three, send several messages, then checkout tabs one at two. What did your print server and forwarding server do? Examine the code for these servers and the forwarding client.

* Was there packet loss?
* Was there corruption?
* What is the format of the data sent to the forwarding server from the forwarding client?
* How does the forwarding server extract the forwarding address?
* Draw a digram that shows how data travels between the 3 programs we started.
* Determine your IP address on the local network and an IP address of another student on the local network -- send a message to them, and receive a message from them.

## Your Task:

Your task is to design two agents (a client and a server) that can send messages reliably to each other via the unreliable forwarding server. You may wish to use the `forwardable-msgs` client as a starting point, or you may wish to start from scratch or use a different language. You may also wish to reimplement the unreliable forwarding agent in another language (though because we're using sockets, your client and server need not be in python to communicate with the forwarding server).

#### Some Suggestions

* Start by setting the packet drop and corruption rates to 0, and getting any data  though the forwarding server.
* Tackle packet loss and corruption one at a time.
* Refer to the K&R books section of principles of reliable data transfer.
* Remember, there are many ways to solve this problem -- you need not do exactly what TCP does.
* Start simple (and slow) then work your way towards algorithms that allow faster communication only after you have something that works consistently.
