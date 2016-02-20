#!/usr/bin/python
import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1235))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)
# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)
Primer = None;
try:
    while True:
        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'Request received'
        peticion = recvSocket.recv(2048)
        print peticion
        print 'Answering back...'
        if Primer == None:
            try:
                Primer = int(peticion.split()[1][1:])
                print 'Numero recibido:' + str(Primer)
            except ValueError:
                None
            html = "<html><body><h1>Dame otro numero</h1> </p> </body></html>"
        else:
            try:
                Segundo = int(peticion.split()[1][1:])
                print 'Numero recibido:' + str(Segundo)
                Suma = Primer + Segundo
                html = '<html><body><h1>La suma es <b>' + str(Suma) + ' </b> </h1> </p> </body></html>'
                Primer = None
            except ValueError:
                None
        respuesta = "HTTP/1.1 200 OK\r\n\r\n" + html + "\r\n"    
        recvSocket.send(respuesta)
        recvSocket.close()
except KeyboardInterrupt:
    print "Closing binded socket"
    mySocket.close()
