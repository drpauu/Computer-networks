#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
import random

# Default port number server will listen on
serverPort = 12000
print ('\n***************')
print('IP Server : ')
os.system("hostname -I")
print ('***************')

print ('\n+++++++++++++++')
#Random port
serverPort = random.randrange(49152, 65535)
#Print Port
print('Port in usage : ', serverPort)
print ('+++++++++++++++\n')

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET, SOCK_DGRAM)

# The welcoming port that clients first use to connect

serverSocket.bind(('0.0.0.0', serverPort))

#buffer
size = 2048

print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

print('Waiting for the option chosen by the Client  ...')
opcio, clientAddress = serverSocket.recvfrom(1024)
opcio = opcio.decode()
print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

if opcio == "PUT" or opcio == "put":
	
	print('\n\n ================== PUT ================== \n\n')
			
	print ('Recieving file,s client ')
	txt, clientAddress = serverSocket.recvfrom(size)
	print (' ------ Recieved successfully ------\n')
			
	print ('Opening file')
	with open(txt, 'r') as f:
	    contenido = f.read()
	print ('------ Opened successfully ------ \n') 
	
	print ('Setting directory,s path ')
	directory, clientAddress = serverSocket.recvfrom(size)
	
	print ('Setting file,s name ')
	name, clientAddress = serverSocket.recvfrom(size)
	print ('\n\n')
	    
	if(os.path.exists(directory)):
		completeName = os.path.join(directory, name)
		
		file1 = open(completeName, "a")
		file1.write(contenido)
		file1.close()
	
		print('File,s content : ')
		print(contenido)
		print('\nThis file has saved in : ', completeName)
	else:
		print('XXXXXXX NO EXIST DIRECTORY XXXXXXX')
	
elif opcio == "GET" or opcio == "get":

	print('\n\n ================== GET ================== \n\n')
			
	print ('Recieving file,s client ')
	arxiu, clientAddress = serverSocket.recvfrom(size)
	print (' ------ Recieved successfully ------\n')
	
	
	print ('Opening file')
	with open(arxiu, 'r') as f:
		contenido = f.read()
	print ('------ Opened successfully ------ \n')
	serverSocket.sendto(contenido.encode(), clientAddress)
	
	
#cerrar
#connectionSocket.close()
	
