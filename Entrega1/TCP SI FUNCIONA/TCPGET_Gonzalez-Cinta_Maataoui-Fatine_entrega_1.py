#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
import sys
import random


#Default values
host = gethostbyname(gethostname())
port = 12000

#####################################


#Print IP
print('IP Server : ', gethostbyname(gethostname()))
os.system("hostname -I")

#####################################

#Random port
port = random.randrange(49152, 65535)
#Print Port
print('Port in usage : ', port)

#####################################

#buffer
size = 2048


print ('The Server is ready to recive...')

# Main code
with socket(AF_INET, SOCK_STREAM) as serverSocket:
	serverSocket.bind((host, port)) 
	serverSocket.listen(1) # Waiting for the connection with the client 
	
	connectionSocket, addr = serverSocket.accept()# Connected with the client
	# Connecting the socket
	with connectionSocket:
		print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

		opcio = connectionSocket.recv(128).decode()

		if opcio == "PUT" or opcio == "put":
			print('\n\n ================== PUT ================== \n\n')
			
			print ('Recieving file,s client ')
			txt = connectionSocket.recv(size)
			print (' ------ Recieved successfully ------\n')
			
			print ('Opening file')
			with open(txt, 'r') as f:
			    contenido = f.read()
			print ('------ Opened successfully ------ \n')       
			
			print ('Setting directory,s path ')
			directory = connectionSocket.recv(size).decode()
			
			print ('Setting file,s name ')
			name = connectionSocket.recv(size).decode()
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
			txt = connectionSocket.recv(size)
			print (' ------ Recieved successfully ------\n')
			
			print ('Opening file')
			with open(txt, 'r') as f:
				contenido = f.read()
			print ('------ Opened successfully ------ \n')  
				
			connectionSocket.send(contenido.encode())
				
	print('\n\n >>>>>>>>>> END OF CONNECTION <<<<<<<<<< \n\n ')	
	connectionSocket.close()			
