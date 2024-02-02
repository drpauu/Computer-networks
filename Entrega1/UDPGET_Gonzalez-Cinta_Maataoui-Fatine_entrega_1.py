#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
# Default port number server will listen on
serverPort = 12000

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET,SOCK_STREAM)

# The welcoming port that clients first use to connect
serverSocket.bind(('',serverPort))

print ('El Servidor esta listo para recibir...')

opcio, clientAddress = serverSocket.recvfrom(128).decode()

if opcio == "PUT":
	txt, clientAddress = serverSocket.recvfrom(1024)
	
	with open(txt, 'r') as f:
	    contenido = f.read()
	    
	
	directory, clientAddress = serverSocket.recvfrom(1024).decode()
	name, clientAddress = serverSocket.recvfrom(1024).decode()
	
	    
	completeName = os.path.join(directory, name)
	print('Directori on es vol guardar : ',completeName)
	
	file1 = open(completeName, "w")
	file1.write(contenido)
	file1.close()
	
	print(contenido)
	#connectionSocket.send(capitalizedSentence.encode())
	
elif opcio == "GET":
	arxiu, clientAddress = serverSocket.recvfrom(1024)
	print('El arxiu es leido per el servidor... \n')
	with open(arxiu, 'r') as f:
		contenido = f.read()
	print('Enviando el archivo al cliente... \n')	
	serverSocket.sendto(contenido.encode(), clientAddress)
	
	
#cerrar
connectionSocket.close()

	
