# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
from socket import *

#server name argument
host = input('Insert IP,s server :')

#server port number
port = int(input('Insert port,s server :'))

print ('*************************************************************************')
print('\nContact with the server ', host, ' from the port ', port, '\n')
print ('*************************************************************************')

size = 2048


# Connecting the socket
with socket(AF_INET, SOCK_STREAM) as clientSocket:
	
	clientSocket.connect((host, port))
	print('\n \n [**********] Successfully connection with the Server [**********] \n \n')
    	
	funcion = input('Escriu quina funcio vol fer (GET o PUT): ')
	
	#sending the option mode
	clientSocket.send(funcion.encode())
	
	txt = input('Quin arxiu vol llegir: ')
	sf = os.stat(txt).st_size	#calcular size del archivo
	print(sf)
	

	if funcion == "GET" or funcion == "get":
	
		print('\n\n ================== GET ================== \n\n')

		
		# Elegir el size del arxivo del que quieres transmitir
		correcte = False
		while correcte == False:
			paquet_size = input('Choose the paquet size (32, 64, 128, ... , 2048 bytes): ')
			
			if paquet_size == '32':
			    correcte = True
			elif paquet_size == '64':
			    correcte = True
			elif paquet_size == '128':
			    correcte = True
			elif paquet_size == '256':
			    correcte = True
			elif paquet_size == '512':
			    correcte = True
			elif paquet_size == '1024':
			    correcte = True
			elif paquet_size == '2048':
			    correcte = True
			else:
			    print ("Error: try again\n")

		print ('The paquet size is ', paquet_size, ' Bytes\n')
		clientSocket.send(paquet_size.encode())
		
		paq = sf//paquet_size #parte entera del cociente
		
		ultim_paq = sf%paquet_size #siza del ultimo paq
		num_paq = paq+1 #nbloc
		
		print('Sending the file to the Server ...')
		clientSocket.send(txt.encode(paquet_size))
		
		print('Recieving the file ...')
		contenido = clientSocket.recv(paquet_size).decode()
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
		
		# Elegir el size del arxivo del que quieres transmitir
		correcte = False
		while correcte == False:
			paquet_size = input('Choose the paquet size (32, 64, 128, ... , 2048 bytes): ')
			
			if paquet_size == '32':
			    correcte = True
			elif paquet_size == '64':
			    correcte = True
			elif paquet_size == '128':
			    correcte = True
			elif paquet_size == '256':
			    correcte = True
			elif paquet_size == '512':
			    correcte = True
			elif paquet_size == '1024':
			    correcte = True
			elif paquet_size == '2048':
			    correcte = True
			else:
			    print ("Error: try again\n")

		print ('The paquet size is ', paquet_size, ' Bytes\n')
		clientSocket.send(paquet_size.encode())
		
		
		print ('Opening file')
		with open(txt, 'r') as f:
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
		print('You have not chosen any correct options. Please try again ')
	print('\n\n >>>>>>>>>> END OF CONNECTION <<<<<<<<<< \n\n ')	
	clientSocket.close()


