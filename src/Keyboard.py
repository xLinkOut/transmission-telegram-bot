# -*- coding: utf-8 -*-
from telebot import types
import Emoji

mainKeyboard = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
mainKeyboardAddTorrent 		= types.KeyboardButton(Emoji.plus+' Add Torrent')
mainKeyboardManageTorrent 	= types.KeyboardButton(Emoji.open_file_folder+' Manage Torrent')
mainKeyboardAbout 			= types.KeyboardButton(Emoji.question+' About')
mainKeyboard.add(mainKeyboardAddTorrent,mainKeyboardManageTorrent,mainKeyboardAbout)

inlineTorrentKeyboard = types.InlineKeyboardMarkup()
inlineTorrentKeyboardResume = types.InlineKeyboardButton('▶ Resume',callback_data='Resume')
inlineTorrentKeyboardPause 	= types.InlineKeyboardButton(Emoji.pause +' Pause' ,callback_data='Pause')
inlineTorrentKeyboardRemove = types.InlineKeyboardButton('❌ Remove',callback_data='Remove')
inlineTorrentKeyboardDelete = types.InlineKeyboardButton('🔥 Delete',callback_data='Delete')
inlineTorrentKeyboardFiles	= types.InlineKeyboardButton('📑 Files' ,callback_data='Files')
inlineTorrentKeyboardInfo 	= types.InlineKeyboardButton('🏷 Info'  ,callback_data='Info')
inlineTorrentKeyboardPrec 	= types.InlineKeyboardButton('👈🏼 Previous',callback_data='Prev')
inlineTorrentKeyboardSucc 	= types.InlineKeyboardButton('👉🏼 Next',callback_data='Next')
inlineTorrentKeyboard.add(inlineTorrentKeyboardResume,inlineTorrentKeyboardPause,inlineTorrentKeyboardRemove,inlineTorrentKeyboardDelete,inlineTorrentKeyboardFiles,inlineTorrentKeyboardInfo,inlineTorrentKeyboardPrec,inlineTorrentKeyboardSucc)

torrentMainKeyboard = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
torrentMainKeyboardResumeAll = types.KeyboardButton(Emoji.arrow_forward+' Resume All')
torrentMainKeyboardPauseAll  = types.KeyboardButton(Emoji.pause+' Pause All')
torrentMainKeyboardAdd   	 = types.KeyboardButton(Emoji.plus+' Add Torrent')
torrentMainKeyboardRefresh   = types.KeyboardButton(Emoji.ciclo+' Refresh')

torrentMainKeyboardMainMenu  = types.KeyboardButton(Emoji.door+' Main Menu')
torrentMainKeyboard.add(torrentMainKeyboardResumeAll,torrentMainKeyboardPauseAll,torrentMainKeyboardAdd,torrentMainKeyboardRefresh,torrentMainKeyboardMainMenu)

forceReplyKeyboard = types.ForceReply(selective=False)
