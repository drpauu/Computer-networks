#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
import random
import struct

def byte_int(mida_p):
	mida = mida_p.decode()
		
	i = 0
	mida_paq = 0
	
	while(i < len(mida)):
		if(mida[i].isdigit()):
			
			mida_paq *= 10
			mida_paq = mida_paq + int(mida[i])
		i +=1
	return mida_paq
	
# Default port number server will listen on
serverPort = 12000

print ('\n***************')
print('IP Server : ')
os.system("hostname -I")
print ('***************')

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET, SOCK_DGRAM)

# The welcoming port that clients first use to connect

serverSocket.bind(('0.0.0.0', serverPort))

#buffer
size = 2048

### Recibir WRQ o RRQ 
num_ack = 0
ACK = 0
ack_ok = False

nseq = 0	#En esta variable guardaremos el numero de secuencia
while ack_ok == False :
	opcion, clientAddress = serverSocket.recvfrom(46) 
	opcio_ack = struct.unpack('!H', opcion[0:2]) #Guardar en opcio_ack el codigo de operacion, contenido y modo
	fun = opcio_ack[0]  #el codigo de operacion
	
	txt = opcion[2:-7]	#El contenido del paquete se guardara en txt
	
	if opcio_ack[0] == 1 or opcio_ack[0] == 2:  #el codigo de operacion de la opcion triada
		ack = struct.pack('HH', 4, nseq)
		serverSocket.sendto(ack, clientAddress)
		
		ack_ok = True
	else :
		print('Opcio no rebuda correctament ')

print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

if fun == 2:
	
	print(' ================== RRQ/PUT ================== ')
	print(' **************  ACK,', ACK, '  **************\n\n')
	ACK += 1
			
	
	with open(txt, 'r') as f:
			contenido = f.read()
	
	print ('Recibint mida del paquet ... ')
	ack_ok = False
	while ack_ok == False :
		mida_p, clientAddress = serverSocket.recvfrom(46) 
		mida_ack = struct.unpack('!HH', mida_p[0:4])
		
		mida = mida_p[4:]
		nseq = mida_ack[1]
		
		if mida_ack[0] == 3:  #el codigo de operacion de la opcion triada
			print('\n 	**************  ACK,', ACK, '  ************** 	\n')
			ACK += 1
			
			ack = struct.pack('HH', 4, nseq)
			serverSocket.sendto(ack, clientAddress)
			
			ack_ok = True
		else :
			print('Opcio no rebuda correctament ')
	mida_paq = byte_int(mida_p)
	print ('Mida del paquet:', mida_paq,  ' Bytes\n')
	
	#Lugar donde se quiere guardar
	print ('Recibint l,adreça de directori ')
	directory, clientAddress = serverSocket.recvfrom(size)
	
	print ('Recibint nom del fitxer ')
	name, clientAddress = serverSocket.recvfrom(size)
	print ('\n\n')
	
	#Comprobar que la direccion es correcta
	sentence = "correcto"
	if( not os.path.exists(directory)):
		sentence = "incorrecto"
		print('L,adreça que heu triat no existeix. ')
		serverSocket.sendto(sentence.encode(), clientAddress)
	else:	
		serverSocket.sendto(sentence.encode(), clientAddress)	
		
		#Recibir el size del archivo leido
		print ('Recibint mida del fitxer ... ')
		ack_ok = False
		while ack_ok == False :
			size_p, clientAddress = serverSocket.recvfrom(46) 
			size_ack = struct.unpack('!HH', size_p[0:4])
			
				
			nseq = size_ack[1]
			
			if size_ack[0] == 3:  #el codigo de operacion de la opcion triada
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				
				ack = struct.pack('HH', 4, nseq)
				serverSocket.sendto(ack, clientAddress)
				
				ack_ok = True
			else :
				print('Opcio no rebuda correctament ')
		size = byte_int(size_p)
		print ('Mida del fitxer : ', size,  ' Bytes')
				
		completeName = os.path.join(directory, name)		
		file1 = open(completeName, "wb")
		
		
		print('\n\nCreant un nou canal per transmetre els paquets ...')
		#Creando puerto para transmitir a traves del canal
		ServerPort = random.randrange(49152, 65535)
		print('Port en ús  : ', ServerPort, '\n')
		
		
		clientPort, clientAddress = serverSocket.recvfrom(512)
		clientPort = int(clientPort.decode())
		print('clientPort en ús  : ', clientPort, '\n')
		
		serverSocket.sendto(str(ServerPort).encode(), clientAddress)
		
		
		clientAddress = (clientAddress[0], clientPort) #asignarle a clientAddress el nuevo puerto del cliente
		
		
		serverS = socket(AF_INET, SOCK_DGRAM)

		# The welcoming port that clients first use to connect
		
		serverS.bind(('0.0.0.0', ServerPort))

		
		#Obrim l'arxiu
		print ('##########################   Obrint canal     ########################## \n')
			
		print('-------------------   Rebre contingut de el fitxer     -------------------\n')
		
		bytes_reb = 0  #Es guarden els bytes que es van recibint
		npack = 0	#Es guarden el nombre de paquets rebuts
		
		with open(txt, 'rb') as f:
		
			while (bytes_reb < int(size)):
				
				print ('Rebent el paquet numero [ ', npack + 1, ' ]  . . .    (' , ServerPort ,' ,', clientPort , ') \n')
				
				arxiu_pack, clientAddress = serverS.recvfrom(int(mida_paq) + 4) # se le suma 4 bytes de capçalera	
				
				#Desenpaquetando sin la capçalera (por eso el -4)
				arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
				
				if nseq + 1 > 65535:
					nseq = -1 
					
				if(nseq + 1 == arxiu[1]):
					nseq = arxiu[1]
					
					ack_buff = struct.pack('HH', 4, nseq)
					serverS.sendto(ack_buff, clientAddress)
					
					file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
					bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
					
					print('\n 	**************  ACK,', ACK, '  ************** 	\n')
					ACK += 1
					
					npack += 1
					
				else:
					print('ERROR al rebre el paquet')
			if(int(bytes_reb) == int(mida_paq)): #En caso de que se tiene que recibir un ultimo paquete vacio
				print ('Rebent el paquet numero [ ', npack + 1, ' ]  . . .    (' , ServerPort ,' ,', clientPort , ') \n')
				
				arxiu_pack, clientAddress = serverS.recvfrom(int(mida_paq) + 4) # se le suma 4 bytes de capçalera	
				
				#Desenpaquetando sin la capçalera (por eso el -4)
				arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
				
				if nseq + 1 > 65535:
					nseq = -1 
				
				if(nseq + 1 == arxiu[1]):
					nseq = arxiu[1]
					
					print('\n 	**************  ACK,', ACK, '  ************** 	\n')
					ACK += 1
					
					ack_buff = struct.pack('HH', 4, nseq)
					serverS.sendto(ack_buff, clientAddress)
					
					file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
			file1.close()   	
			    	   
		print ('\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
		
		print ('##########################   TANCANT CANAL     ########################## \n')      
		
		serverS.close()
		
		print('\n\n Contingut de el fitxer : \n\n')
		print(contenido, "\n \n")
		print('\nAquest fitxer s,ha desat a  : ', completeName)
		
elif fun == 1:

	print(' ================== WRQ/GET ================== ')
	print(' **************  ACK,', ACK, '  ************** 	\n\n')
	ACK += 1		
	
		
	print ('Rebent mida del paquet ... ')
	ack_ok = False
	while ack_ok == False :
		mida_p, clientAddress = serverSocket.recvfrom(46) 
		mida_ack = struct.unpack('!HH', mida_p[0:4])
		
		mida = mida_p[4:]
		nseq = mida_ack[1]
		
		if mida_ack[0] == 3:  #el codigo de operacion de la opcion triada
			print('\n 	**************  ACK,', ACK, '  ************** 	\n')
			ACK += 1
			
			ack = struct.pack('HH', 4, nseq)
			serverSocket.sendto(ack, clientAddress)
			
			ack_ok = True
		else :
			print('Opcio no rebuda correctament ')

	
	
	mida_paq = byte_int(mida_p)	
	print ('\nMida del paquet:', mida_paq, ' Bytes\n')
	
	
	#Obtener el size del archivo leido y enviarlo al cliente
	size = os.stat(txt).st_size
	print('Enviant mida del fitxer ... ')
	ack_ok = False
	while ack_ok == False :
		size_arx = struct.pack('!HH', 3, nseq)
		size_arx += str(size).encode()
		
		serverSocket.sendto(size_arx, clientAddress)
		
		size_ack, clientAddress = serverSocket.recvfrom(4)
		
		ack = struct.unpack('HH', size_ack)
		
		
		if ack[0] == 4:  #el codigo de operacion de ack
			print('REBUT ACK,',ACK, '  DEL CLIENT\n\n')
			ACK += 1
			
			ack_ok = True
		else :
			print('Opcio no rebuda correctament ')

	nseq += 1
	print ('Mida del fitxer : ', size,  ' Bytes\n')
	
	
	#Leer el archivo con paquetes
	arxiu = open(txt, 'rb')
	buff = arxiu.read(int(mida_paq))  #buff =  contenido del primer paquete del arxiu	
	buff_size = len(buff)	#guarda la mida del primer paquete
	
	
	if ack_ok == False :
		print ("El client encara no pot rebre informacio.")
	else :  #Cuando si este preparado para recibir 
	
		print('Creant un nou canal per transmetre els paquets ...')
		
		#Creando puerto para transmitir a traves del canal	
		ServerPort = random.randrange(49152, 65535)
		print('Port en ús  : ', ServerPort, '\n')
		
		clientPort, clientAddress = serverSocket.recvfrom(512)
		clientPort = int(clientPort.decode())
		print('clientPort en ús  : ', clientPort, '\n')
		
		serverSocket.sendto(str(ServerPort).encode(), clientAddress)
		
		clientAddress = (clientAddress[0], clientPort) #asignarle a clientAddress el nuevo puerto del cliente
		
		serverS = socket(AF_INET, SOCK_DGRAM)

		# The welcoming port that clients first use to connect

		serverS.bind(('0.0.0.0', ServerPort))
		
		print ('##########################   Obrint canal     ########################## \n')
		print ('###################   Enviant contingut del fitxer   ################### \n\n')
		
		npack = 0
		while buff:
			if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
				nseq = 0
			
			a, clientAddress = serverS.recvfrom(512) #Recibimos el listo del cliente para comenzar a enviar
			
			#Empaquetando    (codigo de operacion : 3)
			buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  
			
			print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , ServerPort ,' ,', clientPort , ')\n')		
			serverS.sendto(buff_pack, clientAddress)
			
			buff_ack, clientAddress = serverS.recvfrom(4) #Recibir el paquete del ACK
			ack_buff = struct.unpack('HH', buff_ack)
			
			if(ack_buff[0] == 4): #Codigo de operacion ACK
				print('REBUT ACK,',ACK, '  DEL CLIENT\n\n')	
				ACK += 1
					
				buff = arxiu.read(int(mida_paq))
				
				previous_buff_size = buff_size	#size del ultimo paquete enviado
				buff_size = len(buff) #Se guarda la mida del siguiente paquete 
				
				npack += 1   #Se itera el numero de paquetes
				nseq += 1    #Se itera el numero de secuencia
			else:
				print('Paquet no rebut correctament')
		if(int(mida_paq) == int(previous_buff_size)):	#Si la mida del ultimo paquete transmitido es igual a la mida del paquete
			if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
				nseq = 0
			
			a, clientAddress = serverS.recvfrom(512) #Recibimos el listo del cliente para comenzar a enviar
			
			#Empaquetando    (codigo de operacion : 3)
			buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  
			
			print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , ServerPort ,' ,', clientPort , ')\n')		
			serverS.sendto(buff_pack, clientAddress)
			
			buff_ack, clientAddress = serverS.recvfrom(4) #Recibir el paquete del ACK
			ack_buff = struct.unpack('HH', buff_ack)
			
			if(ack_buff[0] == 4): #Codigo de operacion ACK
				print('REBUT ACK,',ACK, '  DEL CLIENT\n\n')	
				ACK += 1
			
			
		print(' -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n')
		print ('##########################   TANCANT CANAL     ########################## \n')
		serverS.close()
	
print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')		
	
#cerrar
serverSocket.close()
	
