#GET: llegint del disc i mostrant per pantalla en el Servidor i emmagatzemant en el Client.

# TCP server program that upper cases text sent from the client
from socket import *
import os.path
import random
import struct

	
# Default port number server will listen on
serverPort = 12000

print ('\n***************')
print('IP Server : ')
os.system("hostname -I")
print ('***************\n\n')

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
	paq, clientAddress = serverSocket.recvfrom(512) #Es 512 (0..511 bytes) porque es el size maquimo de un paquete 

#********Creando puerto para transmitir a traves del canal (RFC 1350)***********************************
	serverPort = random.randrange(49152, 65535)
	print('Port en ús  : ', serverPort, '\n')
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('0.0.0.0', serverPort))
	
	print("CLIENT ADDRESS                               :               ", clientAddress)
#********************************************************************************************************	

	#Obtenemos la opcion codificado de tamaño 2 bytes y decodificamos
	opcio_ack = struct.unpack('!H', paq[0:2]) #Guardar en opcio_ack el codigo de operacion, contenido y modo
	fun = opcio_ack[0]  #el codigo de operacion

	# Obtenemos 0 que indica donde acaba el final del nombre del archivo 
	name = paq.find(b'\x00',2)
	# Obtenemos el nombre codificado y decodificamos
	txt = paq[2:name].decode('utf-8')
	print("Filename -> ", txt)

	# Obtenemos 0 que indica donde acaba el final del modo 
	mode = paq.find(b'\x00', name + 1)
	# Obtenemos el modo codificado y decodificamos
	modo = paq[name+1:mode].decode('utf-8')
	#print("Mode -> ", modo)

	# Obtenemos 0 que indica donde acaba el final de la opción 
	opcio = paq.find(b'\x00', mode+1)
	# Obtenemos la opción codificada y decodificamos
	opcion = paq[mode+1:opcio].decode('utf-8')
	
	# Obtenemos 0 que indica donde acaba el final del valor
	valor = paq.find(b'\x00', opcio+1)
	# Obtenemos el valor codificado y decodificamos
	size = paq[opcio+1:valor].decode('utf-8')
	print("size del archivo -> ", size)


	# Obtenemos 0 que indica donde acaba el final de la opción 
	opcio = paq.find(b'\x00', valor+1)
	# Obtenemos la opción codificada y decodificamos
	opcion = paq[valor+1:opcio].decode('utf-8')
	

	# Obtenemos 0 que indica donde acaba el final del valor
	valor = paq.find(b'\x00', opcio+1)
	# Obtenemos el valor codificado y decodificamos
	mida_paq = paq[opcio+1:valor].decode('utf-8')
	print("size del paquete -> ", mida_paq)

	# Obtenemos 0 que indica donde acaba el final de la opción 
	opcio = paq.find(b'\x00', valor+1)
	# Obtenemos la opción codificada y decodificamos
	opcion = paq[valor+1:opcio].decode('utf-8')
	

	# Obtenemos 0 que indica donde acaba el final del valor
	valor = paq.find(b'\x00', opcio+1)
	# Obtenemos el valor codificado y decodificamos
	save_path = paq[opcio+1:valor].decode('utf-8')
	print("path -> ", save_path)
	
	#Comprobar que la direccion es correcta
	if(opcio_ack[0] == 2):
		
		if(not os.path.exists(save_path)):
			print('L,adreça que heu triat no existeix. ')
			sentence = "incorrecto"
			
			serverSocket.sendto(sentence.encode(), clientAddress)
			sys.exit()	#Tanca el programa porque ha habido un error
		else:
			sentence = "correcto"
			serverSocket.sendto(sentence.encode(), clientAddress)


	# Obtenemos 0 que indica donde acaba el final de la opción 
	opcio = paq.find(b'\x00', valor+1)
	# Obtenemos la opción codificada y decodificamos
	opcion = paq[valor+1:opcio].decode('utf-8')

	# Obtenemos 0 que indica donde acaba el final del valor
	valor = paq.find(b'\x00', opcio+1)
	# Obtenemos el valor codificado y decodificamos
	file_name = paq[opcio+1:valor].decode('utf-8')
	print("file name:  -> ", file_name)
	
	# Obtenemos 0 que indica donde acaba el final de la opción 
	opcio = paq.find(b'\x00', valor+1)
	# Obtenemos la opción codificada y decodificamos
	opcion = paq[valor+1:opcio].decode('utf-8')

	# Obtenemos 0 que indica donde acaba el final del valor
	valor = paq.find(b'\x00', opcio+1)
	# Obtenemos el valor codificado y decodificamos
	clientPort = int(paq[opcio+1:valor].decode('utf-8'))
	print("clientPort -->", clientPort)
	
	
	
	#######	OAK ########
	if opcio_ack[0] == 1 or opcio_ack[0] == 2:  #el codigo de operacion de la opcion triada
		mode = 'octet'
		opcio = 'blocksize'
		#especificar la cantidad de bytes
		formato = '!H{}sB{}sB{}sB{}sB{}sB{}sB'
		#especificar los tamaños de cada campo
		formato = formato.format(len(txt), len(modo), len(opcion), len(str(serverPort)), len("tsize"), len("0"))
		#creamos paquete
		oack = struct.pack(formato, 6, txt.encode('utf-8'), 0, modo.encode('utf-8'), 0, opcion.encode('utf-8'), 0, str(serverPort).encode('utf-8'), 0, "tsize".encode('utf-8'), 0, "0".encode('utf-8'), 0)
		
		print("new server port : ", serverPort)
		
		serverSocket.sendto(oack, clientAddress)  #ENVIANDO OACK
		
		ack_ok = True
	else :
		print('ERROR al rebre el paquet')
		ack = struct.pack('HH', 5, nseq)		
		serverSocket.sendto(ack, clientAddress)  #ENVIANDO ERROR
	
	
print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

if fun == 2:
	
	print(' ================== WRQ/PUT ================== ')
	print(' **************  OACK,0  **************\n\n')
	ACK += 1
			
	
	with open(txt, 'rb') as f:
		contenido = f.read()
	
	#Creando el nuevo arxivo
	completeName = os.path.join(save_path, file_name)		
	file1 = open(completeName, "wb")
		
	print('-------------------   Rebre contingut de el fitxer     -------------------\n')
	
	bytes_reb = 0  #Es guarden els bytes que es van recibint
	npack = 0	#Es guarden el nombre de paquets rebuts
	nseq = 0
	with open(txt, 'rb') as f:
	
		while (bytes_reb < int(size)):
			
			print ('Rebent el paquet numero [ ', npack + 1, ' ]  . . .    (' , serverPort ,' ,', clientAddress[1] , ') \n')
			
			arxiu_pack, clientAddress = serverSocket.recvfrom(int(mida_paq) + 4) # se le suma 4 bytes de capçalera	
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			
			if nseq + 1 > 65535:
				nseq = -1 
				
			if(nseq + 1 == arxiu[1]):
				nseq = arxiu[1]
				
				ack_buff = struct.pack('HH', 4, nseq)
				serverSocket.sendto(ack_buff, clientAddress)
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
			
				bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
				
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				
				npack += 1
				
			else:
				print('ERROR al rebre el paquet')
				ack_buff = struct.pack('HH', 5, nseq)	
				serverSocket.sendto(ack_buff, clientAddress)	
				
		if(int(bytes_reb) % int(mida_paq) == 0): #En caso de que se tiene que recibir un ultimo paquete vacio
			print ('Rebent el paquet numero [ ', npack + 1, ' ]  . . .    (' , serverPort ,' ,', clientPort , ') \n')
			
			arxiu_pack, clientAddress = serverSocket.recvfrom(int(mida_paq) + 4) # se le suma 4 bytes de capçalera	
			
			#Desenpaquetando sin la capçalera (por eso el -4)
			arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
			
			if nseq + 1 > 65535:
				nseq = -1 
			
			if(nseq + 1 == arxiu[1]):
				nseq = arxiu[1]
				
				print('\n 	**************  ACK,', ACK, '  ************** 	\n')
				ACK += 1
				
				ack_buff = struct.pack('HH', 4, nseq)
				serverSocket.sendto(ack_buff, clientAddress)
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
			else:
				print('ERROR al rebre el paquet')
				ack_buff = struct.pack('HH', 5, nseq)	
				serverSocket.sendto(ack_buff, clientAddress)	
			
		file1.close()   	
		    	   
	print ('\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
	
	
	
	print('\n\n Contingut de el fitxer : \n\n')
	print(str(contenido,'latin-1'), "\n \n")
	print('\nAquest fitxer s,ha desat a  : ', completeName)
	
elif fun == 1:

	print(' ================== RRQ/GET ================== ')
	print(' **************  OACK,0  **************\n\n')
	
	buff_ack, clientAddress = serverSocket.recvfrom(4) #Recibir el paquete del ACK
	ack_buff = struct.unpack('HH', buff_ack)
	print('REBUT ACK,',ACK, '  DEL CLIENT\n\n')
	ACK += 1		
	nseq += 1
		
	if ack_ok == False :
		print ("El client encara no pot rebre informacio.")
	else :  #Cuando si este preparado para recibir 
	
		print ('###################   Enviant contingut del fitxer   ################### \n\n')
		
		
		#Leer el archivo con paquetes
		arxiu = open(txt, 'rb')
		buff = arxiu.read(int(mida_paq))  #buff =  contenido del primer paquete del arxiu	
		buff_size = len(buff)	#guarda la mida del primer paquete
		
		
		npack = 0
		#Snseq = 0
		while buff:
			
			if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
				nseq = 0
			
			a, clientAddress = serverSocket.recvfrom(512) #Recibimos el listo del cliente para comenzar a enviar
			
			#Empaquetando    (codigo de operacion : 3)
			buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  
			
			print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , serverPort ,' ,', clientPort , ')\n')		
			serverSocket.sendto(buff_pack, clientAddress)
			
			buff_ack, clientAddress = serverSocket.recvfrom(4) #Recibir el paquete del ACK
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
				print('ERROR al enviar el paquet')
				
		if(int(previous_buff_size) == int(mida_paq)):	#Si la mida del ultimo paquete transmitido es igual a la mida del paquete
			if nseq > 65535:	#2^16 es el nº max de paquetes que se pueden transmitir
				nseq = 0
			
			a, clientAddress = serverSocket.recvfrom(512) #Recibimos el listo del cliente para comenzar a enviar
			
			#Empaquetando    (codigo de operacion : 3)
			buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, nseq, buff)  
			
			print ('DATA,', npack + 1, ' <', int(buff_size), ' bytes>  . . .   (' , serverPort ,' ,', clientPort , ')\n')		
			serverSocket.sendto(buff_pack, clientAddress)
			
			buff_ack, clientAddress = serverSocket.recvfrom(4) #Recibir el paquete del ACK
			ack_buff = struct.unpack('HH', buff_ack)
			
			if(ack_buff[0] == 4): #Codigo de operacion ACK
				print('REBUT ACK,',ACK, '  DEL CLIENT\n\n')	
				ACK += 1
			else:
				print('ERROR al enviar el paquet')
			
		print(' -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n')
	
print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')		
	
#cerrar
serverSocket.close()
	
