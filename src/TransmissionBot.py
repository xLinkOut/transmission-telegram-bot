# -*- coding: utf-8 -*-
import telebot, Keyboard, Emoji, Torrent, Dialog
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

bot = telebot.TeleBot("")
auth = "transmission:transmission"

@bot.message_handler(commands=['start'])
def start_answer(message):
	bot.send_message(message.chat.id,'Hello, '+message.chat.first_name+'! '+Emoji.smile,reply_markup=Keyboard.mainKeyboard)

@bot.message_handler(regexp=Emoji.open_file_folder+" Manage Torrent")
def listTorrent_answer(message):
	bot.send_message(message.chat.id,Dialog.wait,reply_markup=Keyboard.torrentMainKeyboard)
	firstTorrent = Torrent.getSingleTorrent(1)
	print firstTorrent
	if(firstTorrent == -1):
		bot.send_message(message.chat.id,Dialog.noTorrent,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	elif(firstTorrent == -2):
		bot.send_message(message.chat.id,Dialog.genericError,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	elif(firstTorrent == False):
		bot.send_message(message.chat.id,Dialog.retrivingError,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	else:
		bot.send_message(message.chat.id,firstTorrent,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.question+" About")
def about_answer(message):
	bot.send_message(message.chat.id,Dialog.about,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.arrow_forward+" Resume All")
def resumeAll_answer(message):
	if(Torrent.resumeAllTorrent()):
		bot.send_message(message.chat.id,Dialog.resumedAll,reply_markup=Keyboard.torrentMainKeyboard,parse_mode="markdown")
	else:
		bot.send_message(message.chat.id,Dialog.genericError,reply_markup=Keyboard.torrentMainKeyboard,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.pause+" Pause All")
def pauseAll_answer(message):
	if(Torrent.pauseAllTorrent()):
		bot.send_message(message.chat.id,Dialog.pausedAll,reply_markup=Keyboard.torrentMainKeyboard,parse_mode="markdown")
	else:
		bot.send_message(message.chat.id,Dialog.genericError,reply_markup=Keyboard.torrentMainKeyboard,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.plus+' Add Torrent')
def addTorrent_answer(message):
	bot.send_message(message.chat.id,Dialog.sendMe,parse_mode="markdown")

@bot.message_handler(regexp="^magnet")
def magnet_answer(message):
	if(Torrent.addTorrentFromMagnet(message.text)):
		bot.send_message(message.chat.id,Dialog.tAdded,parse_mode="markdown")
	else:
		bot.send_message(message.chat.id,Dialog.genericError,parse_mode="markdown")

@bot.message_handler(content_types=['document'])
def file_answer(message):
	if(message.document.mime_type == "application/x-bittorrent"):
		file_info = bot.get_file(message.document.file_id)
		file_name = file_info.file_path.split("/")
		file_name = file_name[1]
		file_path = file_info.file_path
		if(Torrent.addTorrentFromFile(file_path,file_name)):
			bot.send_message(message.chat.id,Dialog.tAdded,parse_mode="markdown")
		else:
			bot.send_message(message.chat.id,Dialog.genericError,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.ciclo+" Refresh")
def refresh_answer(message):
	firstTorrent = Torrent.getSingleTorrent(1)
	if(firstTorrent == -1):
		bot.send_message(message.chat.id,Dialog.noTorrent,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	elif(firstTorrent == -2):
		bot.send_message(message.chat.id,Dialog.genericError,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	elif(firstTorrent == False):
		bot.send_message(message.chat.id,Dialog.retrivingError,reply_markup=Keyboard.mainKeyboard,parse_mode="markdown")
	else:
		bot.send_message(message.chat.id,firstTorrent,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")

@bot.message_handler(regexp=Emoji.door+" Main Menu")
def mainMenu_answer(message):
	bot.send_message(message.chat.id,Dialog.mainMenu,reply_markup=Keyboard.mainKeyboard)

@bot.callback_query_handler(func=lambda message: message.data == "Resume")
def callback_resume_answer(message):
	if(Torrent.resumeTorrent(Torrent.getTorrentID(message.message.text))):
		bot.answer_callback_query(message.id,Dialog.tResumed)
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Pause")
def callback_pause_answer(message):
	if(Torrent.pauseTorrent(Torrent.getTorrentID(message.message.text))):
		bot.answer_callback_query(message.id,Dialog.tPaused)
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Remove")
def callback_remove_answer(message):
	if(Torrent.removeTorrent(Torrent.getTorrentID(message.message.text))):
		bot.answer_callback_query(message.id,Dialog.tRemoved)
		if(Torrent.getPreviousTorrent(Torrent.getTorrentID(message.message.text))):
			bot.edit_message_text(Torrent.getPreviousTorrent(Torrent.getTorrentID(message.message.text)),message.from_user.id,message.message.message_id,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")
		else:
			bot.edit_message_text(Dialog.noTorrent+"\n\n"+Dialog.addNewTorrent,message.from_user.id,message.message.message_id,reply_markup='',parse_mode="markdown")
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Delete")
def callback_delete_answer(message):
	if(Torrent.deleteTorrent(Torrent.getTorrentID(message.message.text))):
		bot.answer_callback_query(message.id,Dialog.tRemoved)
		if(Torrent.getPreviousTorrent(Torrent.getTorrentID(message.message.text))):
			bot.edit_message_text(Torrent.getPreviousTorrent(Torrent.getTorrentID(message.message.text)),message.from_user.id,message.message.message_id,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")
		else:
			bot.edit_message_text(Dialog.noTorrent+"\n\n"+Dialog.addNewTorrent,message.from_user.id,message.message.message_id,reply_markup='',parse_mode="markdown")
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Files")
def callback_files_answer(message):
	files = Torrent.getFilesTorrent(Torrent.getTorrentID(message.message.text))
	if(files == -1):
		bot.answer_callback_query(message.id,Dialog.noFiles)
	elif(files):
		if(len(files) < 200):
			bot.answer_callback_query(message.id,files,True)
		else:
			bot.answer_callback_query(message.id,Dialog.textTooLarge)
			bot.send_message(message.from_user.id,files)
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Info")
def callback_info_answer(message):
	info = Torrent.getInfoTorrent(Torrent.getTorrentID(message.message.text))
	if(info):
		if(len(info) < 200):
			bot.answer_callback_query(message.id,info,True)
		else:
			bot.answer_callback_query(message.id,Dialog.textTooLarge)
			bot.send_message(message.from_user.id,info)
	else:
		bot.answer_callback_query(message.id,Dialog.genericError)

@bot.callback_query_handler(func=lambda message: message.data == "Next")
def callback_prev_answer(message):
	nextTorrent = Torrent.getNextTorrent(Torrent.getTorrentID(message.message.text))
	if(nextTorrent):
		bot.edit_message_text(nextTorrent,message.from_user.id,message.message.message_id,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")
	else:
		bot.answer_callback_query(message.id,Dialog.noNext)

@bot.callback_query_handler(func=lambda message: message.data == "Prev")
def callback_prev_answer(message):
	prevTorrent = Torrent.getPreviousTorrent(Torrent.getTorrentID(message.message.text))
	if(prevTorrent):
		bot.edit_message_text(prevTorrent,message.from_user.id,message.message.message_id,reply_markup=Keyboard.inlineTorrentKeyboard,parse_mode="markdown")
	else:
		bot.answer_callback_query(message.id,Dialog.noPrevious)

bot.polling()
