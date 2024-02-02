#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
import sys
import random
import struct

#Default values
host = gethostbyname(gethostname())
port = 12000

#####################################


#Print IP
print ('\n***************')
print('IP Server : ')
os.system("hostname -I")
print ('***************')


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
	
	print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

	opcio = connectionSocket.recv(128).decode()

	if opcio == "PUT" or opcio == "put":
		print('\n\n ================== PUT ================== \n\n')
		
		print ('Rebent el fitxer del client ... ')
		txt = connectionSocket.recv(size).decode()
		print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
		
		with open(txt, 'r') as f:
			contenido = f.read()
		
		print ('Recibint mida del paquet ... ')
		mida_paq = connectionSocket.recv(512).decode()
		print ('Mida del paquet:', mida_paq,  ' Bytes\n')
		
		#Lugar donde se quiere guardar
		
		print ('Recibint l,adreça de directori ')
		directory = connectionSocket.recv(1024).decode()
		
		print ('Recibint nom del fitxer ')
		name = connectionSocket.recv(1024).decode()
		print ('\n\n')
		
		#Comprobar que la direccion es correcta
		
		sentence = "correcto"
		
		if not os.path.exists(directory):
			sentence = "incorrecto"
			print('L,adreça que heu triat no existeix. ')
			
			connectionSocket.send(sentence.encode())
		else:
			connectionSocket.send(sentence.encode())
			
			#Recibir el size del archivo leido
			print ('Recibint mida del fitxer ... ')
			size = connectionSocket.recv(1024).decode().strip()
			print ('Mida del fitxer : ', size,  ' Bytes\n')
				
			completeName = os.path.join(directory, name)
			file1 = open(completeName, "wb")
		
		
			bytes_reb = 0  #Es guarden els bytes que es van recibint
			npack = 0	#Es guarden el nombre de paquets rebuts
			
			#Decirle al cliente que estamos listos para recibir
			sentence = "preparat"
			connectionSocket.send(sentence.encode())
#*************************** CANAL (put) **********************************************************************
			
			#Creando puerto para transmitir a traves del canal
			port = random.randrange(49152, 65535)
			print('Port en ús  : ', port, '\n')
			
			clientPort = connectionSocket.recv(1024).decode()
			clientPort = int(clientPort)
			print("clientPort en ús :  ", clientPort)
			
			connectionSocket.send(str(port).encode())
			
			addr = (host, port)
			
			serverS = socket(AF_INET, SOCK_STREAM)
			
			serverS.bind((host, port)) 
			serverS.listen(1) # Waiting for the connection with the client 
			
			connectionS, addr = serverS.accept()# Conectado con el client, se crea un nuevo puerto 
			
#********************************************************************************************************							
			with connectionS:
			#Obrim l'arxiu
				print ('##########################   Obrint canal     ########################## \n')
			
				print('\n-------------------   Enviant contingut del fitxer    -------------------')
			
				with open(txt, 'wb') as f:
				
					while (bytes_reb < int(size)):
						
						print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .   (' , port ,' ,', clientPort , ')\n')
						arxiu_pack = connectionS.recv(int(mida_paq) + 4) # se le suma 4 bytes de capçalera
						print ('------   PAQUET NUMERO [ ', npack + 1, ' ]  REBUT AMB EXIT   ------\n')
						
						#Desenpaquetando sin la capçalera (por eso el -4)
						arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
						
						file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
						
						bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
						
						npack += 1
						
					file1.close()   	
					    	   
				print('\n -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n\n')
				print ('##########################   TANCANT CANAL     ########################## \n')
				
				connectionS.close()
		
			print('Contingut de el fitxer : \n\n')
			print(contenido, "\n \n")
			print('\nAquest fitxer s,ha desat a  : ', completeName)
		
	elif opcio == "GET" or opcio == "get":
	
		print('\n\n ================== GET ================== \n\n')
	
		print ('Rebent el fitxer del client ... ')
		txt = connectionSocket.recv(size).decode()
		print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
		
		print ('Recibint mida del paquet ... ')
		mida_paq = connectionSocket.recv(512).decode()
		print ('Mida del paquet:', mida_paq,  ' Bytes\n')
		
		print ('##########################   Obrint fitxer   ########################## \n')
		with open(txt, 'rb') as f:
			buff = f.read()
		print ('\n -------------------   FITXER OBERT AMB EXIT   ------------------- \n\n')  
		
		#Obtener el size del archivo leido y enviarlo al cliente
		size = os.stat(txt).st_size
		print ('Mida del fitxer : ', size,  ' Bytes\n')
		connectionSocket.send(str(size).encode()) 
		   
		#Leer el archivo con paquetes
		arxiu = open(txt, 'rb')
		buff = arxiu.read(int(mida_paq))  #buff =  contenido del primer paquete del arxiu	
		buff_size = len(buff)	#guarda la mida del primer paquete
		
		#Esperar que el cliente este listo para recibir los paquetes
		sentence = connectionSocket.recv(512).decode()
		if sentence != "preparat" :
			print ("El client encara no pot rebre informacio.")
		else :  #Cuando si este preparado para recibir 
			
			print ('                               Creando canal . . .                               \n\n')
			
			#Creando puerto para transmitir a traves del canal
			port = random.randrange(49152, 65535)
			print('Port en ús  : ', port, '\n')
			
			clientPort = connectionSocket.recv(1024).decode()
			clientPort = int(clientPort)
			print("clientPort en ús :  ", clientPort)
			
			connectionSocket.send(str(port).encode())
			
			addr = (host, port)
			
			serverS = socket(AF_INET, SOCK_STREAM)
			
			serverS.bind((host, port)) 
			serverS.listen(1) # Waiting for the connection with the client 
			
			connectionS, addr = serverS.accept()# Conectado con el client, se crea un nuevo puerto 
			
			print('Conexión aceptada en {}'.format(addr))
			
			with connectionS:
			
				print ('##########################   Obrint canal     ########################## \n')
				print('\n-------------------   Enviant contingut del fitxer    -------------------')
				
				npack = 0
				while buff:
					
					#Empaquetando    (codigo de operacion : 3)
					buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, npack, buff)  
					
					print ('Enviant el paquet numero [ ', npack + 1 , ' ]  . . .   (' , port ,' ,', clientPort , ')\n')
					connectionS.send(buff_pack)
					
					buff = arxiu.read(int(mida_paq))

					buff_size = len(buff) #Se guarda la mida del siguiente paquete 
					
					npack += 1;   #Se itera el numero de paquetes
				
				print('\n -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n\n')
				print ('##########################   TANCANT CANAL     ########################## \n')
			connectionS.close()
			
	print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')	
	connectionSocket.close()			
