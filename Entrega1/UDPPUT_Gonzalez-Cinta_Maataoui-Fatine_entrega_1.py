# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
from socket import *

# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000

# Request IPv4 and TCP communication
clientSocket = socket(AF_INET, SOCK_STREAM)

# Read file from the user

funcion = input('Escriu quina funcio vol fer (GET o PUT): ')
txt = input('Quin arxiu vol llegir: ')


clientSocket.sendto(funcion.encode(),(serverName,serverPort))

if funcion == "GET":
	print('Has triat la funcio GET')
	
	print('Enviando archivo al servidor')
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	print('recibiendo el archivo ...')
	contenido, serverAddress = clientSocket.recvfrom(1024).decode()
	print('...archivo recibido del servidor')
	
	print('Guardando el archivo ...')
	
	save_path = input('En quin directori ho vol guardar: \n')
	if not os.path.exists(save_path):
		print('No existeix el directori que has triat.')
	else:
		file_name = input('Quin nom vol posar al nou fitxer? : ')
		completeName = os.path.join(save_path, file_name)
		print(completeName)
		file1 = open(completeName, "w")
		file1.write(contenido)
		file1.close()
		
		
	print(contenido)
	
elif funcion == "PUT":
	print('Has triat la funcio PUT')
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	with open(txt, 'r') as f:
		print('El arxiu SI existeix\n')
		contenido = f.read()
	# Send the file and then wait for a response 
	save_path = input('En quin directori ho vol guardar: \n')
	
	if not os.path.exists(save_path):
		print('No existeix el directori que has triat.')
	else:
	
		print('Enviando el directori al servidor ...\n')
		clientSocket.sendto(save_path.encode(),(serverName,serverPort))
		
		file_name = input('Quin nom vol posar al nou fitxer? : ')
		print('Enviando el nom del arxiu al servidor ...\n')
		clientSocket.sendto(file_name.encode(),(serverName,serverPort))
	
		
else:
	print('No has triat cap opcio correcta. Torna-ho a provar')





# Print the converted text and then close the socket
#print ('From Server:')
clientSocket.close()
