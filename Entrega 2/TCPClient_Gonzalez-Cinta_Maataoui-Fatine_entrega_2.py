# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
from socket import *
import struct
import random

#server name argument
host = input('Insert IP,s server :')
#host = '10.192.23.233'
#server port number
port = 12000

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
	
	with open(txt, 'r') as f:
		contenido = f.read()

	if funcion == "GET" or funcion == "get":
	
		print('\n\n ================== GET ================== \n\n')

		print('Enviant fitxer a Servidor ...')
		clientSocket.send(txt.encode())
		
		# Elegir el size del arxivo del que quieres transmitir
		correcte = False
		while correcte == False:
			paquet_size = input('Tria la mida d,el paquet  (32, 64, 128, ... , 2048 bytes): ')
			
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
			    print ("Error: torna a intentar-ho \n")

		print ('Mida del paquet: ', paquet_size, ' Bytes\n')
		clientSocket.send(paquet_size.encode())
		
		#Recibir el size del archivo que se va a leer a posteriori
		print ('Recibint mida del fitxer ... ')
		size = clientSocket.recv(1024).decode().strip()
		print ('Mida del fitxer : ', size,  ' Bytes\n')
		
		#Lugar donde se quiere guardar el archivo posteriormente recibido por el servidor
		save_path = input('Escriu l,adreça de directori on vols guardar el fitxer  --> ')
		
		# if the directory,s path don't exist
		if not os.path.exists(save_path):
			print('L,adreça que heu triat no existeix. ')
		else:
			file_name = input('Escriviu un nom nou per al fitxer: ')
			
			completeName = os.path.join(save_path, file_name)
			
			file1 = open(completeName, "wb")
			
		
			bytes_reb = 0  #Es guarden els bytes que es van recibint
			npack = 0	#Es guarden el nombre de paquets rebuts
			
			#Decirle al servidor que estamos listos para recibir
			sentence = "preparat"
			clientSocket.send(sentence.encode())
			
#*************************** CANAL (get) **********************************************************************
			
			#Creando puerto para transmitir a traves del canal
			port = random.randrange(49152, 65535)
			print('Port en ús  : ', port,'\n')
			
			clientSocket.send(str(port).encode())		#Enviar puerto que usaremos en el cliente
			
			serverPort = clientSocket.recv(1024)  #Recibir puerto que usara el servidor
			serverPort = int(serverPort.decode())
			print('serverPort: ',serverPort)
			
			clientS = socket(AF_INET, SOCK_STREAM) 
	
			clientS.connect((host, serverPort))
			
#********************************************************************************************************			
			#Obrim l'arxiu
			print ('##########################   Obrint canal     ########################## \n')
			
			print('\n-------------------   Rebre contingut de el fitxer     -------------------')
			
			with open(txt, 'wb') as f:
				
				while (bytes_reb < int(size)):
					
					print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , port ,' ,', serverPort , ') \n')
					arxiu_pack = clientS.recv(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
					print ('------   PAQUET NUMERO [ ', npack + 1, ' ]  REBUT AMB EXIT   ------\n')
					
					#Desenpaquetando sin la capçalera (por eso el -4)
					arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
					
					file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
					
					bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
					
					npack += 1
					
				file1.close()
		
			print('\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n\n')
			
			print ('##########################   TANCANT CANAL     ########################## \n')      
			clientS.close()
				
			print('Contingut de el fitxer : \n\n')
			print(contenido, "\n \n")
			print('\nAquest fitxer s,ha desat a  : ', completeName)
				
		
	elif funcion == "PUT" or funcion == "put":
		
		print('\n\n ================== PUT ================== \n\n')
		
		print('Enviant fitxer a Servidor ...')
		clientSocket.send(txt.encode())
		
		# Elegir el size del arxivo del que quieres transmitir
		correcte = False
		while correcte == False:
			paquet_size = input('Tria la mida d,el paquet  (32, 64, 128, ... , 2048 bytes):  ')
			
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
				print ("Error: torna a intentar-ho \n")

		print ('Mida del paquet: ', paquet_size, ' Bytes\n')
		clientSocket.send(paquet_size.encode())
	
		
		#Lugar donde se quiere guardar el archivo posteriormente recibido por el servidor
		save_path = input('Escriu l,adreça de directori on vols guardar el fitxer  --> ')
		clientSocket.send(str(save_path).encode())
		
		file_name = input('Escriviu un nom nou per al fitxer: ')
		clientSocket.send(str(file_name).encode())
		
		sentence = clientSocket.recv(1024).decode()
		if (sentence == "incorrecto"):
			print('L,adreça que heu triat no existeix. ')
		else :
			
			with open(txt, 'rb') as f:
				buff = f.read()
			
			print ('\n -------------------   FITXER OBERT AMB EXIT   ------------------- \n\n')
			
			#Enviando el size del archivo que se va a leer a posteriori
			size = os.stat(txt).st_size
			print ('Mida del fitxer : ', size,  ' Bytes\n')
			clientSocket.send(str(size).encode())
			   
			#Leer el archivo con paquetes
			arxiu = open(txt, 'rb')
			buff = arxiu.read(int(paquet_size))  #buff =  contenido del primer paquete del arxiu	
			buff_size = len(buff)	#guarda la mida del primer paquete
			
			
			#Esperar que el cliente este listo para recibir los paquetes
			sentence = clientSocket.recv(512).decode()
			if sentence != "preparat" :
				print ("El client encara no pot rebre informacio.")
			else :  #Cuando si este preparado para recibir 
				print ('                               Creando canal . . .                               \n\n')
#*************************** CANAL (pyt) **********************************************************************
			
			#Creando puerto para transmitir a traves del canal
			port = random.randrange(49152, 65535)
			print('Port en ús  : ', port,'\n')
			
			clientSocket.send(str(port).encode())		#Enviar puerto que usaremos en el cliente
			
			serverPort = clientSocket.recv(1024)  #Recibir puerto que usara el servidor
			serverPort = int(serverPort.decode())
			print('serverPort: ',serverPort)
			
			clientS = socket(AF_INET, SOCK_STREAM) 
	
			clientS.connect((host, serverPort))
			
#********************************************************************************************************											
			print ('##########################   Obrint canal     ########################## \n')
			print('\n-------------------   Enviant contingut del fitxer    -------------------')
			
			npack = 0
			while buff:
				
				#Empaquetando    (codigo de operacion : 3)
				buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, npack, buff)  #Empaquetando
				
				print ('Enviant el paquet numero [ ', npack + 1, ' ]  . . .    (' , port ,' ,', serverPort , ') \n')
				clientS.send(buff_pack)
				
				buff = arxiu.read(int(paquet_size))

				buff_size = len(buff)  #Se guarda la mida del siguiente paquete 
				
				npack += 1;	 #Se itera el numero de paquetes
			
			print('\n -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n\n')
			print ('##########################   TANCANT CANAL     ########################## \n')
			clientS.close()
	
	else:
		print('No heu escollit cap opció correcta. Siusplau torna-ho a provar!!!')
	
	print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')	
	clientSocket.close()


