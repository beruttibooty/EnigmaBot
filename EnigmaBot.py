from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import ast

f = open('EnigmaBotUsers','r')
userData = ast.literal_eval(f.read())
f.close()

# Enigma
rotKey = {}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
rotKey['IC'] = 'DMTWSILRUYQNKFEJCAZBPGXOHV'
rotKey['IIC'] = 'HQZGPJTMOBLNCIFDYAWVEUSRKX'
rotKey['IIIC'] = 'UQNTLSZFMREHDPXKIBVYGJCWOA'

UKW = {}
UKW['A'] = 'EJMZALYXVBWFCRQUONTSPIKHGD'

#functions
'''
def rotorselect(bot, update):
    rotors = update.message.text[14:]
    rotors = rotors.upper().split(' ')
    key = []
    for j in range(0,len(rotors)):
        key.append(rotKey[rotors[j]])
    return key

def rotation(bot, update):
    startrot = update.message.text[19:]
    startrot = startrot.upper().split(' ')
    for t in range(0,len(key)):
        key[t] = key[t][key[t].find(startrot[t]):]+key[t][:key[t].find(startrot[t])]
    return key[:]
'''
def decrypt(bot, update):
    encoded = encrypt(update)
    bot.sendMessage(chat_id=update.message.chat_id, text=encoded)

def encrypt(update):
    try:
        input = update.inline_query.query
        user = update.inline_query.from_user.username
    except:
        pass
    try:
        input = update.message.text[8:]
        user = update.message.from_user.username
    except:
        pass
    rotors = userData[user]['rotors']
    key = []
    for j in range(0,len(rotors)):
        try:
            key.append(rotKey[rotors[j]])
        except KeyError:
            print 'KeyError. Try command again.'
    startrot = userData[user]['startrot']
    for t in range(0,len(key)):
            key[t] = key[t][key[t].find(startrot[t]):]+key[t][:key[t].find(startrot[t])]
    masterkey = key[:]
    reflector = UKW[userData[user]['reflector']]
    
    rawmessage = input.upper().strip()
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
        rotate(key)
    return encoded

def rotate(key):
    key[0] = key[0][1:]+key[0][0]
    if key[0][0] == 'R':
        key[1] = key[1][1:]+key[1][0]
    if key[1][0] == 'F':
        key[2] = key[2][1:]+key[2][0]
    return

#setup

def inlinequery(bot, update):
    results = list()

    message = encrypt(update)

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title=message,
                                            input_message_content=InputTextMessageContent(
                                                message)))

    update.inline_query.answer(results)

#tele stuffs
updater = Updater('287243222:AAFAtLm9MvpotjS_nOzV0XXJA__Hm_mX_V0')

'''
updater.dispatcher.add_handler(CommandHandler('rotor_select', rotorselect))
updater.dispatcher.add_handler(CommandHandler('starting_rotation', rotation))
'''

updater.dispatcher.add_handler(CommandHandler('decrypt', decrypt))
updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

updater.start_polling()
updater.idle()