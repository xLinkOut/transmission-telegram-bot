# -*- coding: utf-8 -*-
import os,re,Emoji,requests,shutil
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

def check():
	response = os.popen('transmission-remote --auth '+auth+' --list').read()
	if(re.search("Couldn't connect to server",response)):
		return False
	else:
		return True

def getSingleTorrent(id):
	response = getAllTorrent()
	if(response):
		if(isinstance(response, list)):
			if(len(response) > 0):
				return response[id-1]
			else:
				return -1 #NO TORRENT
		elif(response == -1): #NO TORRENT FROM LIST
			return -1
		else:
			return -2 #GENERIC ERROR
	else:
		return False #RESPONSE FAILED
def getAllTorrent():
	if(check()):
		response = os.popen('transmission-remote --auth '+auth+' --list').read()
		response = response.split("\n")
		if(len(response) == 3):
			return -1
		response.pop(0)
		response.pop(-1)
		response.pop(-1)
		torrentList = []
		indexTorrentList = 0
		for current in response: #" *" + info[0]  + "* "
			info = re.sub('\s+',' ',current).strip()
			info = info.split(' ',8) #ARRAY CHE CONTIENE TUTTE LE PROPRIETA' DEL TORRENT ATTUALE #" *" + index[0] + "* " +
			torrent = Emoji.id_viola 	+ " *" + info[0]  + "*    " + \
					  Emoji.magnifier 	+ " *" + index[2] + "* " + info[7]+ "\n\n"+ \
					  Emoji.bookmark 	+ " *" + index[1] + "* " + info[8]+ "\n\n"+ \
					  Emoji.arrow_down 	+ " *" + index[3] + "* " + info[4]+ "   " + \
					  Emoji.arrow_up 	+ " *" + index[4] + "* " + info[5]+ "\n\n"+ \
					  Emoji.black_mark 	+ " *" + index[5] + "* " + info[1]+ "   " + \
					  Emoji.inbox_tray 	+ " *" + index[6] + "* " + info[2]+ "\n\n"+ \
					  Emoji.clessidra 	+ " *" + index[7] + "* " + info[3]+ "   " + \
					  Emoji.ciclo 		+ " *" + index[8] + "* " + info[6]+ "\n"
			torrentList.insert(indexTorrentList,torrent)
			indexTorrentList += 1
		return torrentList
	else:
		return False

def getTorrentID(text):
	textRow = text.split("\n")
	idRow = textRow[0]
	idArray = idRow.split(" ")
	tid = idArray[1]
	tid = tid.replace("*","")
	return int(tid)

def resumeTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --start').read()
	if(re.search("success",response)):
		return True
	else:
		return False

def pauseTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --stop').read()
	if(re.search("success",response)):
		return True
	else:
		return False

def removeTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --remove').read()
	if(re.search("success",response)):
		return True
	else:
		return False

def deleteTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --remove-and-delete').read()
	if(re.search("success",response)):
		return True
	else:
		return False

def getFilesTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --files').read()
	if(response != ''):
		response = response.split("\n")
		if(len(response) > 3):
			summary = response[0]
			response.pop(0)
			response.pop(0)
			response.pop(-1)
			torrentFileList = ''
			for file in response:
				info = re.sub('\s+',' ',file).strip()
				info = info.split(' ',6) #ARRAY CHE CONTIENE TUTTE LE PROPRIETA' DEL TORRENT ATTUALE
				temp = info[6].split('/',1)
				name = temp[1]
				torrentFileList = torrentFileList + info[1] + " " + temp[1] + "\n"
			return torrentFileList
		else:
			return -1 #NO FILE LISTED
	else:
		return False

def getInfoTorrent(id):
	response = os.popen('transmission-remote --auth '+auth+' -t '+str(id)+' --info').read()
	if(response != ''):
		response = response.split("\n")
		totalSize = response[15][2:]
		totalSize = totalSize.split('(')
		totalSize = totalSize[0]
		totalSize = re.sub('\s+',' ',totalSize).strip()
		downloadingTime = response[24][2:]
		downloadingTime = downloadingTime.split('(')
		downloadingTime = downloadingTime[0]
		dateAdded =  re.sub('\s+',' ',response[23]).strip()
		info = response[8][2:] + "\n" +\
			   totalSize + "\n" +\
			   response[16][2:] + "\n" +\
			   response[17][2:] + "\n" +\
			   dateAdded + "\n" +\
			   downloadingTime
		return info
	else:
		return False
#response[20][2:] + "\n" +\ peers #response[3][2:] + "\n" +\ hash #response[8][2:] + "\n" +\ location

def resumeAllTorrent():
	allTorrent = getAllTorrent()
	if not(allTorrent): return False
	result = False
	for torrent in allTorrent:
		response = os.popen('transmission-remote --auth '+auth+' -t '+str(getTorrentID(torrent))+' --start').read()
		if(re.search("success",response)):
			result = True
		else:
			response = False
	return result

def pauseAllTorrent():
	allTorrent = getAllTorrent()
	if not(allTorrent): return False
	result = False
	for torrent in allTorrent:
		response = os.popen('transmission-remote --auth '+auth+' -t '+str(getTorrentID(torrent))+' --stop').read()
		if(re.search("success",response)):
			result = True
		else:
			response = False
	return result

def addTorrentFromFile(file_path,file_name):
	url = 'https://api.telegram.org/file/botINSERT_TOKEN_HERE/'+file_path
	r = requests.get(url,verify=False,stream=True)
	r.raw.decode_content = True
	with open(file_name, 'wb') as f:
		shutil.copyfileobj(r.raw, f)
	response = os.popen('transmission-remote --auth '+auth+' --add '+file_name).read()
	os.remove(file_name)
	if(re.search("success",response)):
		return True
	else:
		return False

def addTorrentFromMagnet(magnet):
	response = os.popen('transmission-remote --auth '+auth+' --add "'+magnet+'"').read()
	if(re.search("success",response)):
		return True
	else:
		return False

def getPreviousTorrent(id):
	response = getAllTorrent()
	if(response):
		if(isinstance(response, list)):
			if(len(response) > 0):
				if id-1 in response:
					return response[id-1]
				else:
					return False #NO PREVIOUS TORRENT
			else:
				return False #NO TORRENT
		else:
			return False #GENERIC ERROR
	else:
		return False #RESPONSE FAILED

def getNextTorrent(id):
	response = getAllTorrent()
	if(response):
		if(isinstance(response, list)):
			if(len(response) > 0):
				if id+1 in response:
					return response[id+1]
				else:
					return False #NO PREVIOUS TORRENT
			else:
				return False #NO TORRENT
		else:
			return False #GENERIC ERROR
	else:
		return False #RESPONSE FAILED
