import json
import argparse
import os


def parse_file(filename):
    path = './channels/' + filename
    if not os.path.isfile(path):
        parser.error('File <' + filename + '> does not exist.')
        return
    with open(path, encoding='utf-8') as data_file:
        with open('./channels/' + filename + '.txt', 'a') as file:
            data = json.loads(data_file.read())
            last_msg_id = ''
            msg_index = 0
            members = data['members']
            members_ids = {}
            for member in members:
                members_ids[member['id']] = member['profile']['real_name_normalized']
            for n in range(len(data['messages']) - 1, -1, -1):
                message = data['messages'][n]
                if last_msg_id != message['user']:
                    file.write('\n')
                    msg_index = 0
                else:
                    msg_index += 1
                last_msg_id = message['user']
                if 'files' not in message:
                    msg = message['text']
                    for user in members_ids:
                        msg = msg.replace('@' + user, members_ids[user])
                    tab = '[' + members_ids[message['user']] + ']: '
                    if msg_index != 0:
                        tab = ' ' * len(tab)
                    file.write(tab + msg.replace('\n', ' ') + '\n')

parser = argparse.ArgumentParser(description='Slacky Parser, Jesús Real Tovar.')
parser.add_argument('-t', '--type', help='Action type', metavar='Type', default='all', required=True)
parser.add_argument('-f', '--filename', help='File name', metavar='FILENAME', default='filename' )
args = parser.parse_args()

if args.type == 'all':
    for file in os.listdir('./channels'):
        if file[-5:] == '.json':
            parse_file(file)
elif args.type == 'f':
    parse_file(args.filename)