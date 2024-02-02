# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
from socket import *

# Default to running on localhost, port 12000
serverName = input('Introduce the IP of the Server :')
serverPort = int(input('Introduce the Port of the Server :'))

# Request IPv4 and TCP communication
#clientSocket = socket(AF_INET, SOCK_STREAM)


clientSocket = socket(AF_INET, SOCK_DGRAM) 

#clientSocket.connect((serverName, serverPort))

print('Contact with the server ', serverName, ' from the port ', serverPort, '')

# Read file from the user
funcion = input('Write what function you want to do (GET o PUT): ')
clientSocket.sendto(funcion.encode(),(serverName,serverPort))

txt = input('Put which file you want to read : ')

if funcion == "GET":
	print('\n\n ================== GET ================== \n\n')

	print('Sending the file to the Server ...')
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	
	print('Recieving the file ...')
	contenido, serverAddress = clientSocket.recvfrom(1024)
	print('File recieved from the Server')

	print('Saving file ...')
	save_path = input('Type the directory,s path where you want to save the file --> ')
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

elif funcion == "PUT" or opcio == "put":
	
	print('\n\n ================== PUT ================== \n\n')
		
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	
	print ('Opening file')
	with open(txt, 'r') as f:
		contenido = f.read()
	print ('------ Opened successfully ------ \n')  
	# Send the file and then wait for a response 
	save_path = input('Type the directory,s path where you want to save the file --> ')

	
	print('Sending the directory,s path to the Server ...\n')
	
	clientSocket.sendto(save_path.encode(),(serverName,serverPort))
	
	file_name = input('Type a new name for the file: ')
	
	print('Sending the new file,s name to the Server...\n')
	clientSocket.sendto(file_name.encode(),(serverName,serverPort))

		
else:
	print('You have not chosen any correct options. Please try again ')



# Print the converted text and then close the socket
#print ('From Server:')
clientSocket.close()
