# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
from socket import *

#server name argument
host = input('Insert IP,s server :')

#server port number
port = int(input('Insert port,s server :'))

size = 2048

# Connecting the socket
with socket(AF_INET, SOCK_STREAM) as clientSocket:
	
	clientSocket.connect((host, port))
	print('\n \n [**********] Successfully connection with the Server [**********] \n \n')
    	
	funcion = input('Escriu quina funcio vol fer (GET o PUT): ')
	
	#sending the option mode
	clientSocket.send(funcion.encode())
	
	txt = input('Quin arxiu vol llegir: ')

	if funcion == "GET" or funcion == "get":
	
		print('\n\n ================== GET ================== \n\n')

		print('Sending the file to the Server ...')
		clientSocket.send(txt.encode())
		
		print('Recieving the file ...')
		contenido = clientSocket.recv(size).decode()
		print('File recieved from the Server')

		print('Saving file ...')
		save_path = input('Type the directory,s path where you want to save the file --> ')
		
		# if the directory,s path don't exist
		if not os.path.exists(save_path):
			print('The path that you have chosen does not exist.')
		else:
			file_name = input('Type a new name for the file: ')
			
			completeName = os.path.join(save_path, file_name)
			
			file1 = open(completeName, "w")
			file1.write(contenido)
			file1.close()
		
			print('File,s content : ')
			print(contenido)
			print('\nThis file has saved in : ', completeName)
			
		
	elif funcion == "PUT" or funcion == "put":
		
		print('\n\n ================== PUT ================== \n\n')
		
		clientSocket.send(txt.encode())
		
		print ('Opening file')
		with open(txt, 'r') as f:
			print('El arxiu SI existeix\n')
			contenido = f.read()
		print ('------ Opened successfully ------ \n')  
			
		# Send the file and then wait for an answer
		save_path = input('Type the directory,s path where you want to save the file --> ')


		print('Sending the directory,s path to the Server ...\n')
		clientSocket.send(save_path.encode())
		
		file_name = input('Type a new name for the file: ')
		
		print('Sending the new file,s name to the Server...\n')
		clientSocket.send(file_name.encode())
			
		
	else:
		print('No has triat cap opcio correcta. Torna-ho a provar')
	print('\n\n >>>>>>>>>> END OF CONNECTION <<<<<<<<<< \n\n ')	
	clientSocket.close()




