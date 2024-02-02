# PUT: llegint del disc i mostrant per pantalla en el Client i emmagatzemant en el Servidor.

import sys
import os.path
import random
import struct
from socket import *

# Default to running on localhost, port 12000
serverName = input('Introduce the IP of the Server :')
serverPort = 12000
clientPort = random.randrange(49152, 65535)
# Request IPv4 and TCP communication
clientSocket = socket(AF_INET, SOCK_DGRAM) 


#print("clientPort :", clientPort)

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

while ack_ok == False :
	

	mode = 'octet'
	opcio = 'blocksize'
	#especificar la cantidad de bytes
	formato = '!H{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB{}sB'
	#especificar los tamaños de cada campo
	formato = formato.format(len(txt), len(mode), len(opcio), len(str(size)), len(opcio), len(str(paquet_size)), len(opcio), len(str(save_path)), len(opcio), len(str(file_name)),len(opcio), len(str(clientPort)), len("tsize"), len("0"))
	
	#creamos paquete
	print(txt)
	arx = struct.pack(formato, fun, txt.encode('utf-8'), 0, mode.encode('utf-8'), 0, opcio.encode('utf-8'), 0, str(size).encode('utf-8'), 0, opcio.encode('utf-8'), 0, str(paquet_size).encode('utf-8'), 0, opcio.encode('utf-8'), 0 , str(save_path).encode('utf-8'), 0, opcio.encode('utf-8'), 0,  str(file_name).encode('utf-8'), 0, opcio.encode('utf-8'),0, str(clientPort).encode('utf-8') ,0, "tsize".encode('utf-8'), 0, "0".encode('utf-8'), 0)
	
	print('#########################################################################')
	if(fun == 1):
		print('\n\nEnviant RRQ(GET), <fitxer, octet>   al Servidor ...\n\n')
		
	else:
		print('\n\nEnviant WRQ(PUT), <fitxer, octet>   al Servidor ...\n\n')
	print('#########################################################################')	
				
	clientSocket.sendto(arx,(serverName,serverPort)) #Enviamos el paquete con (WRQ o RRQ) y el arxiu
	
	
	
	if(fun == 2):
		sentence, serverAddress = clientSocket.recvfrom(1024)
		sentence = sentence.decode()
	
		if (sentence == "incorrecto"):
			print('L,adreça que heu triat no existeix. ')
			sys.exit()	#Tanca el programa porque ha habido un error
	
	ack_tipo, serverAddress = clientSocket.recvfrom(512) #Recibimos el oack
	
	#Obtenemos la opcion codificado de tamaño 2 bytes y decodificamos
	opcio_ack = struct.unpack('!H', ack_tipo[0:2]) #Guardar en opcio_ack el codigo de operacion, contenido y modo
	oack = opcio_ack[0]  #el codigo de operacion
	
	## OAK##
	if oack == 6:  #el codigo de operacion del oack = 6
		print('REBUT OACK,0  DEL SERVIDOR \n\n')		

		# Obtenemos 0 que indica donde acaba el final del nombre del archivo 
		name = ack_tipo.find(b'\x00',2)
		# Obtenemos el nombre codificado y decodificamos
		t = ack_tipo[2:name].decode('utf-8')
		
		# Obtenemos 0 que indica donde acaba el final del modo 
		mode = ack_tipo.find(b'\x00', name + 1)
		# Obtenemos el modo codificado y decodificamos
		modo = ack_tipo[name+1:mode].decode('utf-8')
		#print("Mode -> ", modo)
		
		# Obtenemos 0 que indica donde acaba el final de la opción 
		opcio = ack_tipo.find(b'\x00', mode+1)
		# Obtenemos la opción codificada y decodificamos
		opcion = ack_tipo[mode+1:opcio].decode('utf-8')
		
		# Obtenemos 0 que indica donde acaba el final del valor
		valor = ack_tipo.find(b'\x00', opcio+1)
		# Obtenemos el valor codificado y decodificamos
		serverPort = ack_tipo[opcio+1:valor].decode('utf-8')
		print("new Server Port -> ", serverPort)
		serverPort = int(serverPort)
		serverAddress = (serverName, serverPort)
	
		
		ack_ok = True
	else :
		print('ERROR al enviar el paquet')
		


if (funcion == "GET" or funcion == "get"):
	nseq = 0
	
	ack_buff = struct.pack('HH', 4, nseq)	#Empaquetando paquete de ACK
	clientSocket.sendto(ack_buff,(serverName,serverPort))
	print('\n 	**************  ACK,', ACK, '  ************** 	\n')
	ACK += 1
	
	
	with open(txt, 'rb') as f:
		contenido = f.read()
	
	#crear el nuevo file
	completeName = os.path.join(save_path, file_name)
	
	file1 = open(completeName, "wb")

	
	bytes_reb = 0  #Es guarden els bytes que es van recibint
	npack = 0
	
	#Obrim l'arxiu
	print ('\n\n##########################   Obrint canal     ########################## \n')
	print('-------------------   Rebre contingut de el fitxer     -------------------\n')
	
	with open(txt, 'rb') as f:
		
		while (bytes_reb < int(size)):
			
			print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , clientPort ,' ,', serverPort , ') \n')
			a = "listo"
			
			clientSocket.sendto(a.encode(), (serverName,serverPort) ) #Enviar un listo para recibir proximo paquete
			
			arxiu_pack, serverAddress = clientSocket.recvfrom(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			
			if nseq + 1 > 65535:
				nseq = -1 
			
			if(nseq + 1 == arxiu[1]):	#Comprobar que el num_ack+1 sea igual al codigo de operacion 3 del arxiu
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				
				nseq = arxiu[1]
				
				ack_buff = struct.pack('HH', 4, nseq)	#Empaquetando paquete de ACK				
				clientSocket.sendto(ack_buff, (serverName,serverPort))
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
				bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
				
				npack += 1
			else :
				print("ERROR al rebre el paquet")
				ack_buff = struct.pack('HH', 5, nseq)	#Empaquetando paquete de ACK		
				clientSocket.sendto(ack_buff, (serverName,serverPort))
				
		
		if(int(bytes_reb) % int(paquet_size) == 0): #En caso de que se tiene que recibir un ultimo paquete vacio
			print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , clientPort ,' ,', serverPort , ') \n')
			a = "listo"
			
			clientSocket.sendto(a.encode(), (serverName,serverPort) ) #Enviar un listo para recibir proximo paquete
			
			arxiu_pack, serverAddress = clientSocket.recvfrom(int(paquet_size) + 4) # se le suma 4 bytes de capçalera
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			if nseq + 1 > 65535:
				nseq = -1 
			
			if(nseq + 1 == arxiu[1]):	#Comprobar que el num_ack+1 sea igual al codigo de operacion 3 del arxiu
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				nseq = arxiu[1]
				
				ack_buff = struct.pack('HH', 4, nseq)	#Empaquetando paquete de ACK				
				clientSocket.sendto(ack_buff, (serverName,serverPort))
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
			else:
				print('ERROR al rebre el paquet')
				ack_buff = struct.pack('HH', 5, nseq)	#Empaquetando paquete de ACK		
				clientSocket.sendto(ack_buff, (serverName,serverPort))
		file1.close()
	   	    	   
	print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')       
	print ('##########################   TANCANT CANAL     ########################## \n')   
	clientSocket.close()

	print('Contingut de el fitxer : \n\n')
	print(str(contenido,'latin-1'), "\n \n")
	print('\nAquest fitxer s,ha desat a  : ', completeName)

		
elif (funcion == "PUT" or funcion == "put"):
	print('REBUT OACK,0  DEL SERVIDOR\n\n')
	ACK += 1
	
	nseq = 0
	nseq+=1
		   
	#Leer el archivo con paquetes
	arxiu = open(txt, 'rb')
	buff = arxiu.read(int(paquet_size))  #buff =  contenido del primer paquete del arxiu	
	buff_size = len(buff)	#guarda la mida del primer paquete

		
		
	print ('\n\n##########################   Obrint canal     ########################## \n')
	print ('###################   Enviant contingut del fitxer    ################## \n')
	
	
	npack = 0 #Es guarden el nombre de paquets rebuts
	bytes_reb = 0  #Es guardan el nombre de bytes rebuts o transmitidos
	while bytes_reb < int(size):
		
		if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
			nseq = 0
		
		print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , clientPort ,' ,', serverAddress[1] , ')\n')
		
		#Empaquetando    (codigo de operacion : 3)
		buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  #Empaquetando
		
		clientSocket.sendto(buff_pack,(serverName, serverPort))
		
		buff_ack, serverAddress = clientSocket.recvfrom(4)
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
			print('ERROR al enviar el paquet')
	
	if(int(previous) == int(paquet_size)):	#Si la mida del ultimo paquete transmitido es igual a la mida del paquete
		if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
			nseq = 0
		
		print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , serverPort ,' ,', clientPort , ')\n')			
		#Empaquetando    (codigo de operacion : 3)
		buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  #Empaquetando
		
		clientSocket.sendto(buff_pack,(serverName, serverPort))
		
		buff_ack, serverAddress = clientSocket.recvfrom(4)
		ack_buff = struct.unpack('HH', buff_ack)
		
		if ack_buff[0] == 4 :
			print('REBUT ACK,',ACK, '  DEL SERVIDOR\n\n')
			ACK += 1
		else:
			print('ERROR al enviar el paquet')
	
	
	print(' -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n')				
	
	print ('##########################   TANCANT CANAL     ########################## \n')
	
	clientSocket.close()

print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')	
#cerrar
clientSocket.close()
