# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 1060))
while 1:
    data = raw_input ( "SEND( TYPE q or Q to Quit):" )
    if (data <> 'Q' and data <> 'q'):
        client_socket.send(data)
    else:
        client_socket.send(data)
        client_socket.close()
        break;
    server_message = client_socket.recv(512)
    print "Message from server:", server_message
            