# -*- coding: utf-8 -*-

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from random import randint
import random
import string

# Enigma
rotKey = {}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotKey['IC'] = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
rotKey['IIC'] = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
rotKey['IIIC'] = 'UQNTLSZFMREHDPXKIBVYGJCWOA'

UKW = {}
UKW['A'] = 'EJMZALYXVBWFCRQUONTSPIKHGD'

blockedUsers = ["EarlyMorningRiceWarning","ThisIsYourTriggerWarning"]

#functions
def rotorselect(bot, update):
    if update.message.from_user.username in blockedUsers:
        return
    rotors = update.message.text[14:]
    rotors = rotors.upper().split(' ')
    key = []
    for j in range(0,len(rotors)):
        key.append(rotKey[rotors[j]])
    return key
def rotation(bot, update):
    if update.message.from_user.username in blockedUsers:
        return
    startrot = update.message.text[19:]
    startrot = startrot.upper().split(' ')
    for t in range(0,len(key)):
        key[t] = key[t][key[t].find(startrot[t]):]+key[t][:key[t].find(startrot[t])]
    return key[:]
def decrypt(bot, update):
    rawmessage = update.message.text[9:]
    rawmessage = rawmessage.upper().strip()
    if update.message.from_user.username in blockedUsers:
        bot.sendMessage(chat_id=update.message.chat_id, text=YoshiEncrypt(rawmessage))
        return
    decoded = ''
    for z in rawmessage:
        if z.isalpha(): decoded += z
    encoded = ''
    char = ''
    transfer = 26
    for i in range(0,len(decoded)):
        char = decoded[i]
        for k in range(0,len(key)):
            transfer = alphabet.find(char)
            char = key[k][transfer]
        transfer = alphabet.find(char)
        char = reflector[transfer]
        for j in range(1,len(key)+1):
            transfer = key[-j].find(char)
            char = alphabet[transfer]
        encoded += char
        rotate()
    bot.sendMessage(chat_id=update.message.chat_id, text=encoded)
    for z in range(0,len(key)):
        key[z] = masterkey[z]
def encrypt(query):
    rawmessage = query.upper().strip()
    decoded = ''
    for z in rawmessage:
        if z.isalpha(): decoded += z
    encoded = ''
    char = ''
    transfer = 26
    for i in range(0,len(decoded)):
        char = decoded[i]
        for k in range(0,len(key)):
            transfer = alphabet.find(char)
            char = key[k][transfer]
        transfer = alphabet.find(char)
        char = reflector[transfer]
        for j in range(1,len(key)+1):
            transfer = key[-j].find(char)
            char = alphabet[transfer]
        encoded += char
        rotate()
    for z in range(0,len(key)):
        key[z] = masterkey[z]
    return encoded
def rotate():
    key[0] = key[0][1:]+key[0][0]
    if key[0][0] == 'R':
        key[1] = key[1][1:]+key[1][0]
    if key[1][0] == 'F':
        key[2] = key[2][1:]+key[2][0]
    return
def YoshiEncrypt(message):
    yoshMess = ""
    for z in message:
        yoshMess += random.choice(string.ascii_uppercase)
    return yoshMess

#setup
key = [rotKey['IC'],rotKey['IIIC'],rotKey['IC'],rotKey['IIIC']]
startrot = ['L','A','N','E']
for t in range(0,len(key)):
        key[t] = key[t][key[t].find(startrot[t]):]+key[t][:key[t].find(startrot[t])]
masterkey = key[:]
reflector = UKW['A']

def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    message = ""

    if update.inline_query.from_user.username in blockedUsers:
        message = YoshiEncrypt(query)
    else:
        message = encrypt(query)

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=message,
                                            input_message_content=InputTextMessageContent(
                                                message)))

    update.inline_query.answer(results)

#tele stuffs
updater = Updater('287243222:AAFAtLm9MvpotjS_nOzV0XXJA__Hm_mX_V0')

updater.dispatcher.add_handler(CommandHandler('rotor_select', rotorselect))
updater.dispatcher.add_handler(CommandHandler('starting_rotation', rotation))
updater.dispatcher.add_handler(CommandHandler('decrypt', decrypt))
updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

updater.start_polling()
updater.idle()