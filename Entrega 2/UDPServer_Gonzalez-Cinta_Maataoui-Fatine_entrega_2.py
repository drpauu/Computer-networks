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
print ('***************')


# Request IPv4 and TCP communication
serverSocket = socket(AF_INET, SOCK_DGRAM)

# The welcoming port that clients first use to connect

serverSocket.bind(('0.0.0.0', serverPort))

#buffer
size = 2048


opcio, clientAddress = serverSocket.recvfrom(1024)
opcio = opcio.decode()
print('\n\n[**********] Successfully connection with the Client [**********]\n\n')

if opcio == "PUT" or opcio == "put":
	
	print('\n\n ================== PUT ================== \n\n')
			
	print ('Rebent el fitxer del client ... ')
	txt, clientAddress = serverSocket.recvfrom(size)
	print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
	
	with open(txt, 'r') as f:
			contenido = f.read()
		
	print ('Recibint mida del paquet ... ')
	mida_paq, clientAddress = serverSocket.recvfrom(size)
	mida_paq = mida_paq.decode()
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
		size, clientAddress = serverSocket.recvfrom(1024)
		size = size.decode().strip()
		print ('Mida del fitxer : ', size,  ' Bytes\n')
				
		completeName = os.path.join(directory, name)		
		file1 = open(completeName, "wb")

		bytes_reb = 0  #Es guarden els bytes que es van recibint
		npack = 0	#Es guarden el nombre de paquets rebuts
		
		#Decirle al cliente que estamos listos para recibir
		sentence = "preparat"
		serverSocket.sendto(sentence.encode(), clientAddress)
		
		
		#Creando puerto para transmitir a traves del canal
		ServerPort = random.randrange(49152, 65535)
		print('Port en ús  : ', ServerPort, '\n')
		
		serverSocket.sendto(str(ServerPort).encode(), clientAddress)
		print("ServerPort enviado")
		
		clientPort, clientAddress = serverSocket.recvfrom(1024)
		clientPort = int(clientPort.decode())
		print("clientPort en ús : ", clientPort)
		
		clientAddress = (clientAddress[0], clientPort) #asignarle a clientAddress el nuevo puerto del cliente
		
		serverS = socket(AF_INET, SOCK_DGRAM)

		# The welcoming port that clients first use to connect
		serverS.bind(('0.0.0.0', ServerPort))
		
		
		#Obrim l'arxiu
		print ('##########################   Obrint canal     ########################## \n')
			
		print('\n-------------------   Rebre contingut de el fitxer     -------------------')
		
		with open(txt, 'wb') as f:
		
			while (bytes_reb < int(size)):
				
				print ('Recibint el paquet numero [ ', npack + 1, ' ]  . . .    (' , ServerPort ,' ,', clientPort , ') \n')
				
				a = "listo"
				serverS.sendto(a.encode(), clientAddress) #Enviar un listo para recibir proximo paquete
				
				arxiu_pack, clientAddress = serverS.recvfrom(int(mida_paq) + 4) # se le suma 4 bytes de capçalera
				print ('------   PAQUET NUMERO [ ', npack + 1, ' ]  REBUT AMB EXIT   ------\n')
				
				#Desenpaquetando sin la capçalera (por eso el -4)
				arxiu = struct.unpack('HH' + str(len(arxiu_pack) - 4) + 's', arxiu_pack )
				
				file1.write(arxiu[2]) #la posicion 2 del array es donde esta el contenido del paquete
				
				bytes_reb += len(arxiu_pack) - 4  #aumentar el size del buffter bytes_reb y restandole la capçalera
				
				npack += 1
				
			file1.close()   	
			    	   
		print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
		
		print ('##########################   TANCANT CANAL     ########################## \n')      
		
		serverS.close()
		
		print('Contingut de el fitxer : \n\n')
		print(contenido, "\n \n")
		print('\nAquest fitxer s,ha desat a  : ', completeName)
		
elif opcio == "GET" or opcio == "get":

	print('\n\n ================== GET ================== \n\n')
			
	print ('Rebent el fitxer del client ... ')
	txt, clientAddress = serverSocket.recvfrom(size)
	print ('\n\n -------------------   FITXER REBUT AMB EXIT   ------------------- \n')
		
	print ('Recibint mida del paquet ... ')
	mida_paq, clientAddress = serverSocket.recvfrom(size)
	mida_paq = mida_paq.decode()
	print ('Mida del paquet:', mida_paq,  ' Bytes\n')
	
	print ('##########################   Obrint fitxer   ########################## \n')
	with open(txt, 'rb') as f:
		buff = f.read()
	print ('\n -------------------   FITXER OBERT AMB EXIT   ------------------- \n\n')  
	
	#Obtener el size del archivo leido y enviarlo al cliente
	size = os.stat(txt).st_size
	print ('Mida del fitxer : ', size,  ' Bytes\n')
	serverSocket.sendto(str(size).encode(), clientAddress)
	
	#Leer el archivo con paquetes
	arxiu = open(txt, 'rb')
	buff = arxiu.read(int(mida_paq))  #buff =  contenido del primer paquete del arxiu	
	buff_size = len(buff)	#guarda la mida del primer paquete
	
	#Esperar que el cliente este listo para recibir los paquetes
	sentence, clientAddress = serverSocket.recvfrom(512)
	sentence = sentence.decode()
	if sentence != "preparat" :
		print ("El client encara no pot rebre informacio.")
	else :  #Cuando si este preparado para recibir 
		
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
		print ('##########################   Enviant contingut del fitxer    ########################## \n')
		
		npack = 0
		while buff:
			
			#Empaquetando    (codigo de operacion : 3)
			buff_pack = struct.pack('HH' + str(buff_size) + 's', 3, npack, buff)  
			
			print ('Enviant el paquet numero [ ', npack + 1 , ' ]  . . .   (' , ServerPort ,' ,', clientPort , ')\n')
			
			a, clientAddress = serverS.recvfrom(512)
			if(a.decode() == "listo"): #Mientras el servidro este listo para recibir paquetes
			
				serverS.sendto(buff_pack, clientAddress)
				
				buff = arxiu.read(int(mida_paq))

				buff_size = len(buff) #Se guarda la mida del siguiente paquete 
				
				npack += 1;   #Se itera el numero de paquetes
		
		print('\n -------------------   CONTINGUT DEL FITXER ENVIAT AMB EXIT   ------------------- \n\n')
		print ('##########################   TANCANT CANAL     ########################## \n')
		serverS.close()
	
print('\n\n >>>>>>>>>> FINAL DE CONEXIÓ <<<<<<<<<< \n\n ')		
	
#cerrar
serverSocket.close()
	
