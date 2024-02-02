# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
import random
import struct
from socket import *


# Default to running on localhost, port 12000
serverName = input('Introduce the IP of the Server :')

serverPort = 12000

# Request IPv4 and TCP communication
clientSocket = socket(AF_INET, SOCK_DGRAM) 


print ('*************************************************************************')
print('\nContact with the server ', serverName, ' from the port ', serverPort, '\n')
print ('*************************************************************************')

# Read file from the user
funcion = input('Write what function you want to do (GET o PUT): ')
clientSocket.sendto(funcion.encode(),(serverName,serverPort))

txt = input('Put which file you want to read : ')

if funcion == "GET" or funcion == "get":
	print('\n\n ================== GET ================== \n\n')

	print('Enviant fitxer a Servidor ...')
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	
	with open(txt, 'r') as f:
		contenido = f.read()
	
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
	clientSocket.sendto(paquet_size.encode(),(serverName,serverPort))
	
	#Recibir el size del archivo que se va a leer a posteriori
	print ('Recibint mida del fitxer ... ')
	size, serverAddress = clientSocket.recvfrom(1024)
	size = size.decode()
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
		clientSocket.sendto(sentence.encode(),(serverName,serverPort))

#*************************** CANAL (GET) **********************************************************************
			
		#Creando puerto para transmitir a traves del canal
		clientPort = random.randrange(49152, 65535)
		print('Port en ús  : ', clientPort,'\n')
		
		clientSocket.sendto(str(clientPort).encode(),(serverName,serverPort))	#Enviar puerto que usaremos en el cliente
	
		serverPort, serverAddress = clientSocket.recvfrom(1024)  #Recibir puerto que usara el servidor
		serverPort = int(serverPort.decode())
		
		print('serverPort en ús  : ', serverPort)
		serverAddress = (serverName, serverPort)
		
		clientS = socket(AF_INET, SOCK_DGRAM) 
			
#********************************************************************************************************	
		
		#Obrim l'arxiu
		print ('##########################   Obrint fitxer   ########################## \n \n')
		
		with open(txt, 'wb') as f:
			
			while (bytes_reb < int(size)):
				
				print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , clientPort ,' ,', serverPort , ') \n')
				a = "listo"
				clientS.sendto(a.encode(),(serverName,serverPort)) #Enviar un listo para recibir proximo paquete
				
				arxiu_pack, serverAddress = clientS.recvfrom(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
				print ('------   PAQUET NUMERO [ ', npack + 1, ' ]  REBUT AMB EXIT   ------\n')
				
				#Desenpaquetando sin la capçalera (por eso el -4)
				arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
				bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
				
				npack += 1
				
			file1.close()
			   	    	   
		print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')       
		clientS.close()
	
		print('Contingut de el fitxer : \n\n')
		print(contenido, "\n \n")
		print('\nAquest fitxer s,ha desat a  : ', completeName)
	
		
elif funcion == "PUT" or funcion == "put":
	
	print('\n\n ================== PUT ================== \n\n')
		
	clientSocket.sendto(txt.encode(),(serverName,serverPort))
	
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
	clientSocket.sendto(paquet_size.encode(),(serverName,serverPort))
	
	#Lugar donde se quiere guardar el archivo posteriormente recibido por el servidor
	save_path = input('Escriu l,adreça de directori on vols guardar el fitxer  --> ')
	clientSocket.sendto(str(save_path).encode(),(serverName,serverPort))
	
	file_name = input('Escriviu un nom nou per al fitxer: ')
	clientSocket.sendto(str(file_name).encode(),(serverName,serverPort))

	
	sentence, serverAddress = clientSocket.recvfrom(1024)
	sentence = sentence.decode()
	
	if (sentence == "incorrecto"):
		print('L,adreça que heu triat no existeix. ')
	else :
	
		print ('##########################   Obrint fitxer   ########################## \n')
		with open(txt, 'rb') as f:
			buff = f.read()
		
		print ('\n -------------------   FITXER OBERT AMB EXIT   ------------------- \n\n')
		
		#Enviando el size del archivo que se va a leer a posteriori
		size = os.stat(txt).st_size
		print ('Mida del fitxer : ', size,  ' Bytes\n')
		clientSocket.sendto(str(size).encode(),(serverName,serverPort))
		   
		#Leer el archivo con paquetes
		arxiu = open(txt, 'rb')
		buff = arxiu.read(int(paquet_size))  #buff =  contenido del primer paquete del arxiu	
		buff_size = len(buff)	#guarda la mida del primer paquete
		
		#Esperar que el cliente este listo para recibir los paquetes
		sentence, serverAddress  = clientSocket.recvfrom(512)
		sentence = sentence.decode()
		if sentence != "preparat" :
			print ("El client encara no pot rebre informacio.")
		else :  #Cuando si este preparado para recibir 
#*************************** CANAL **********************************************************************
			
			#Creando puerto para transmitir a traves del canal
			clientPort = random.randrange(49152, 65535)
			print('Port en ús  : ', clientPort,'\n')
			
			serverPort, serverAddress = clientSocket.recvfrom(1024)  #Recibir puerto que usara el servidor
			serverPort = int(serverPort.decode())
			print('serverPort en ús  : ', serverPort)
			
			
			clientSocket.sendto(str(clientPort).encode(),(serverName,serverPort))		#Enviar puerto que usaremos en el cliente

			serverAddress = (serverName, serverPort) #Asignarle al serverAddress el puerto que usara el servidor
			
			clientS = socket(AF_INET, SOCK_DGRAM) 
			
#********************************************************************************************************	
			
			
			print ('##########################   Obrint canal     ########################## \n')
			print ('##########################   Enviant contingut del fitxer    ########################## \n')
			
			npack = 0
			while buff:
				
				#Empaquetando    (codigo de operacion : 3)
				buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, npack, buff)  #Empaquetando
				
				print ('Enviant el paquet numero [ ', npack + 1, ' ]  . . .   (' , serverPort ,' ,', clientPort , ')\n')
				a, serverAddress = clientS.recvfrom(1024)
				if (a.decode() == "listo"): #Mientras el cliente este listo para recibir paquetes
					clientS.sendto(buff_pack,(serverName, serverPort))
					
					buff = arxiu.read(int(paquet_size))

					buff_size = len(buff)  #Se guarda la mida del siguiente paquete 
					
					npack += 1;	 #Se itera el numero de paquetes
			
			print('\n -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n\n')				
			
			print ('##########################   TANCANT CANAL     ########################## \n')
			
			clientS.close()
else:
	print('No heu escollit cap opció correcta. Siusplau torna-ho a provar!!!')



print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')	
#cerrar
clientSocket.close()
