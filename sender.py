from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time
api_id =                #input App api_id here
api_hash = ''           #input App api_hash here
#prompt to input number.
phone =input("Enter number here: ")

client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

input_file = sys.argv[0]
users = []
with open(r"Scrapped.csv", encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = float(row[2])
        user['name'] = row[3]
        users.append(user)
#prompt to enter message in CMD
message = input("Enter message here: ")
#Only telegram bot can send messages to user id.
#So we only use usernames
for user in users:
    if user['username'] == "":
        continue
    receiver = client.get_input_entity(user['username'])
    try:
        print("Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting for 30 Seconds...")
        time.sleep(random.randrange(10,30))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Waiting for 30 Seconds...")
        time.sleep(random.randrange(60,120))
        #client.disconnect()
        #sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue
client.disconnect()
print("Done. Message sent to all users.")
