# dont delete this line, help us make the project known :)
print('open-source project by www.OPEN-ATS.eu \n change to your own IP and password')
import socket,threading, time
pwd = b'rmxmjwby'  # password
def srv(port,name): #Server funktion
	print(name+'server running')
	# internet protocol parameters
	soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	soc.bind(('217.61.120.98', port))	# address server (ip and port)
	adrGrs = ('0.0.0.0', 5000)			# address ground station
	adrVhc = ('0.0.0.0', 5000)			# address vehicle
	while True:
		msg, adr = soc.recvfrom(1024)	# msg: reciving message, adr: incoming address
		if adr == adrVhc:
			soc.sendto(msg, adrGrs)		# sent to ground station
		elif adr == adrGrs:
			soc.sendto(msg, adrVhc)		# sent to vehicle
		elif msg == b'a grs '+pwd:		# a 'keepalive' data identification
			print(name+'server: new login: adrGrs: '+str(adr))
			adrGrs = adr				# setting address for ground station
		elif msg == b'a vhc '+pwd:		# a 'keepalive' data identification
			print(name+'server: new login: adrVhc: '+str(adr))
			adrVhc = adr  				# setting address for vehicle

threading.Thread(target=srv, args=[3274,'ctr ']).start() # server for videostream
srv(4582,'vid ') # server for drive motor and steering motors data
# code maintained by Lukas Pfitscher (lukaspfitscher@open-ats.eu)
