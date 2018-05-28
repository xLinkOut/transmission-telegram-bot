import os
import re
auth = "transmission:transmission"
index = ['ID: ','Name: ','Status: ','Down: ','Up: ','Done: ','Have: ','ETA: ','Ratio: '] # 0-8

'''
	0-0 ID
	1-8 NAME
	2-7 STATUS
	3-4 DOWNLOAD SPEED
	4-5 UPLOAD SPEED
	5-1 DONE
	6-2 HAVE
	7-2 ETA
	8-6 RATIO
'''

def create_structure(response):
	response = response.split("\n")
	response.pop(0)
	response.pop(-1)
	response.pop(-1)
	for current in response:
		info = re.sub('\s+',' ',current).strip()
		info = info.split(' ',8) #ARRAY CHE CONTIENE TUTTE LE PROPRIETA' DEL TORRENT ATTUALE
		torrent = index[0]+info[0]+"\n"+ \
				  index[1]+info[8]+"\n"+ \
				  index[2]+info[7]+"\n"+ \
				  index[3]+info[4]+"\n"+ \
				  index[4]+info[5]+"\n"+ \
				  index[5]+info[1]+"\n"+ \
				  index[6]+info[2]+"\n"+ \
				  index[7]+info[3]+"\n"+ \
				  index[8]+info[6]+"\n"
		print torrent+"\n"


create_structure(os.popen('transmission-remote --auth '+auth+' --list').read())
 #ARRAY CHE CONTIENE TUTTI I TORRENT PRESENTI (LA POSIZIONE ZERO VA IGNORATA)
#print response[1] #QUESTO E' UN SINGOLO TORRENT, IL PRIMO NELLO SPECIFICO
#PROCEDURA DI SPLITTING PER OTTENERE LE SINGOLE PROPRIETA'
#tor1 = re.sub('\s+',' ',response[1]).strip()
#tor1 = tor1.split(' ',8)
#print info[1]+": "+tor1[8]