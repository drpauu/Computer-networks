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
print ('*************************************************************************\n\n')

# Read file from the user
#	RRQ -(GET)-> 1
#	WRQ -(PUT)-> 2
fun = 0
funcion = input('Escriu quina funció vol fer (GET o PUT): ')

if(funcion == "GET" or funcion == "get"):
	fun = 1
elif(funcion == "PUT" or funcion == "put"):
	fun = 2
else:
	print('No heu escollit cap opció correcta. Siusplau torna-ho a provar!!!')
	sys.exit()	#Tanca el programa porque ha habido un error

#File	
txt = input('Posa el fitxer que vol llegir : ')

#mida del file
size = os.stat(txt).st_size
print ('\nMida del fitxer : ', size,  ' Bytes\n')

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
#print ('Mida del paquet: ', paquet_size, ' Bytes\n')

#Lugar donde se quiere guardar el archivo posteriormente recibido por el servidor
save_path = input('\nEscriu l,adreça de directori on vols guardar el fitxer  --> ')

# if the directory,s path don't exist
if(fun == 1 and not os.path.exists(save_path)):
	print('L,adreça que heu triat no existeix. ')
	sys.exit()	#Tanca el programa porque ha habido un error
	

#new name file
file_name = input('\nEscriviu un nom nou per al fitxer: ')

### ENVIAR WRQ o RRQ  ###

num_ack = 0
ACK = 0
ack_ok = False
nseq = 0
while ack_ok == False :
	
	mode = 'octet'
	opcio = 'blocksize'
	#especificar la cantidad de bytes
	formato = '!H{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB'
	#especificar los tamaños de cada campo
	formato = formato.format(len(txt), len(mode), len(opcio), len(str(size)), len(opcio), len(str(paquet_size)), len(opcio), len(str(save_path)), len(opcio), len(str(file_name)), len("tsize"), len("0"))
	#creamos paquete
	arx = struct.pack(formato, fun, txt.encode(), 0, mode.encode(), 0, opcio.encode(), 0, str(size).encode(), 0, opcio.encode(), 0, str(paquet_size).encode(), 0, opcio.encode(), 0 , str(save_path).encode(), 0, opcio.encode(), 0,  str(file_name).encode(), 0, "tsize".encode(), 0, "0".encode(), 0)
	
	print('#########################################################################')
	if(fun == 1):
		print('\n\nEnviant RRQ(GET), <fitxer, octet>   al Servidor ...')
		
	else:
		print('\n\nEnviant WRQ(PUT), <fitxer, octet>   al Servidor ...')
	print('#########################################################################')	
				
	clientSocket.sendto(arx,(serverName,serverPort)) #Enviamos el paquete con (WRQ o RRQ) y el arxiu
	
	if(fun == 2):
		sentence, serverAddress = clientSocket.recvfrom(1024)
		sentence = sentence.decode()
	
		if (sentence == "incorrecto"):
			print('L,adreça que heu triat no existeix. ')
			sys.exit()	#Tanca el programa porque ha habido un error

	
	ack_tipo, clientAddress = clientSocket.recvfrom(4) #Recibimos el ack
	
	ack = struct.unpack('HH', ack_tipo) #ack sera el array que guarda 
	
	if ack[0] == 4:  #el codigo de operacion del ack = 4
		nseq = ack[1] #en la posicion 1 del array se guardan el nº de paquetes 
		
		print('REBUT ACK,', ACK, '  DEL SERVIDOR \n\n')
		ACK += 1
		
		ack_ok = True
	else :
		print('no rebut correctament ')
		


if (funcion == "GET" or funcion == "get"):
	#print('\n\n ================== GET ================== \n\n')
	
	with open(txt, 'r') as f:
		contenido = f.read()
	
	#crear el nuevo file
	completeName = os.path.join(save_path, file_name)
	
	file1 = open(completeName, "wb")

#*************************** CANAL (GET) **********************************************************************
	print('\n\n Creant un nou canal per transmetre els paquets ...')
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
	
	bytes_reb = 0  #Es guarden els bytes que es van recibint
	npack = 0
	#Obrim l'arxiu
	print ('\n\n##########################   Obrint canal     ########################## \n')
	print('-------------------   Rebre contingut de el fitxer     -------------------\n')
	
	with open(txt, 'rb') as f:
		
		while (bytes_reb < int(size)):
			
			print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , clientPort ,' ,', serverPort , ') \n')
			a = "listo"
			
			clientS.sendto(a.encode(), (serverName,serverPort) ) #Enviar un listo para recibir proximo paquete
			
			arxiu_pack, serverAddress = clientS.recvfrom(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			if nseq + 1 > 65535:
				nseq = -1 
				
			if(nseq + 1 == arxiu[1]):	#Comprobar que el num_ack+1 sea igual al codigo de operacion 3 del arxiu
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				
				nseq = arxiu[1]
				
				ack_buff = struct.pack('HH', 4, nseq)	#Empaquetando paquete de ACK				
				clientS.sendto(ack_buff, (serverName,serverPort))
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
				bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
				
				npack += 1
			else :
				print('Error en rebre el paquet')
		
		if(int(bytes_reb) % int(paquet_size) == 0): #En caso de que se tiene que recibir un ultimo paquete vacio
			print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , clientPort ,' ,', serverPort , ') \n')
			a = "listo"
			
			clientS.sendto(a.encode(), (serverName,serverPort) ) #Enviar un listo para recibir proximo paquete
			
			arxiu_pack, serverAddress = clientS.recvfrom(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			if nseq + 1 > 65535:
				nseq = -1 
				
			
			if(nseq + 1 == arxiu[1]):	#Comprobar que el num_ack+1 sea igual al codigo de operacion 3 del arxiu
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				nseq = arxiu[1]
				
				ack_buff = struct.pack('HH', 4, nseq)	#Empaquetando paquete de ACK				
				clientS.sendto(ack_buff, (serverName,serverPort))
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
		file1.close()
	   	    	   
	print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')       
	print ('##########################   TANCANT CANAL     ########################## \n')   
	clientS.close()

	print('Contingut de el fitxer : \n\n')
	print(contenido, "\n \n")
	print('\nAquest fitxer s,ha desat a  : ', completeName)

		
elif (funcion == "PUT" or funcion == "put"):
	nseq+=1
		   
	#Leer el archivo con paquetes
	arxiu = open(txt, 'rb')
	buff = arxiu.read(int(paquet_size))  #buff =  contenido del primer paquete del arxiu	
	buff_size = len(buff)	#guarda la mida del primer paquete
	
	
#*************************** CANAL (put) **********************************************************************
	print('Creant un nou canal per transmetre els paquets ...')
	
	#Creando puerto para transmitir a traves del canal
	clientPort = random.randrange(49152, 65535)
	print('Port en ús  : ', clientPort,'\n')
	
	clientSocket.sendto(str(clientPort).encode(),(serverName,serverPort))	#Enviar puerto que usaremos en el cliente

	serverPort, serverAddress = clientSocket.recvfrom(1024)  #Recibir puerto que usara el servidor
	serverPort = int(serverPort.decode())
	
	print('serverPort en ús  : ', serverPort)
	serverAddress = (serverAddress[0], serverPort)
	
	clientS = socket(AF_INET, SOCK_DGRAM) 
		
#********************************************************************************************************	
		
		
	print ('\n\n##########################   Obrint canal     ########################## \n')
	print ('###################   Enviant contingut del fitxer    ################## \n')
	
	npack = 0 #Es guarden el nombre de paquets rebuts
	bytes_reb = 0  #Es guardan el nombre de bytes rebuts o transmitidos
	while bytes_reb < int(size):
		
		if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
			nseq = 0
			
		print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , clientPort ,' ,', serverPort , ')\n')
		
		#Empaquetando    (codigo de operacion : 3)
		buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  #Empaquetando
		
		clientS.sendto(buff_pack,(serverName, serverPort))
		
		buff_ack, serverAddress = clientS.recvfrom(4)
		ack_buff = struct.unpack('HH', buff_ack)
		
		if ack_buff[0] == 4 :
			print('REBUT ACK,',ACK, '  DEL SERVIDOR\n\n')
			ACK += 1
			
			buff = arxiu.read(int(paquet_size))

			previous = buff_size   #size del ultimo paquete enviado
			buff_size = len(buff)  #Se guarda la mida del siguiente paquete 
			
			bytes_reb += int(paquet_size)
			
			npack += 1	 #Se itera el numero de paquetes
			
			nseq += 1
		else :
			print('no rebut correctament ')
	
	if(int(previous) == int(paquet_size)):	#Si la mida del ultimo paquete transmitido es igual a la mida del paquete
		if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
			nseq = 0
		
		print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , serverPort ,' ,', clientPort , ')\n')			
		#Empaquetando    (codigo de operacion : 3)
		buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  #Empaquetando
		
		clientS.sendto(buff_pack,(serverName, serverPort))
		
		buff_ack, serverAddress = clientS.recvfrom(4)
		ack_buff = struct.unpack('HH', buff_ack)
		
		if ack_buff[0] == 4 :
			print('REBUT ACK,',ACK, '  DEL SERVIDOR\n\n')
			ACK += 1
	
	
	print(' -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n')				
	
	print ('##########################   TANCANT CANAL     ########################## \n')
	
	clientS.close()

print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')	
#cerrar
clientSocket.close()
