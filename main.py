import pyperclip
import requests
import random
import string
import time
import sys
import re
import os

API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com']
domain = random.choice(domainList)


def banner():
    print(r'''
                         ''~``
                        ( o o )
+------------------.oooO--(_)--Oooo.------------------+
|                                                     |
|                    Mail Swipe                       |
|               [by Sameera Madushan]                 |
|               [Modificado por Jeová]                |
|                    .oooO                            |
|                    (   )   Oooo.                    |
+---------------------\ (----(   )--------------------+
                       \_)    ) /
                             (_/
    ''')


def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username


def extract():
    getUserName = re.search(r'login=(.*)&', newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]


# Got this from https://stackoverflow.com/a/43952192/13276219
def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg


def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }

    print_statusline("Disposing your email address - " + mail + '\n')
    req = requests.post(url, data=data)


def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        print_statusline("Seu Email por enquanto está Vazio. Estamos atualizando automaticamente a cada 5s.")
    else:
        idList = []
        for i in req:
            for k, v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'emails' if length > 1 else 'email'
        print_statusline(f"Você está com {length} {x}. Verifique a pasta de emails ")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r' ' + mail)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k, v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v

            mail_file_path = os.path.join(final_directory, f'{mail}.txt')

            with open(mail_file_path, 'w') as file:
                file.write(
                    "Enviado: " + sender + '\n' + "Para: " + mail + '\n' + "Assunto: " + subject + '\n' + "Data: " + date + '\n' + "Conteúdo: " + content + '\n')


banner()
userInput1 = input("Você quer usar um Email temporario (S/N): ").capitalize()

try:

    if userInput1 == 'S':
        userInput2 = input("\nColoque o nome do email (exemplo: jrjeova): ")
        newMail = f"{API}?login={userInput2}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nSeu Email temporário é " + mail + " (Email ja está copiado (Email ja ta no ctrl+c )" + "\n")
        print(f"---------------------------- | Caixa de Entrada  {mail}| ----------------------------\n")

        while True:
            checkMails()
            time.sleep(5)

    if userInput1 == 'N':
        newMail = f"{API}?login={generateUserName()}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nSeu Email Temporário é  " + mail + " (Email ja está copiado (Email ja ta no ctrl+c) " + "\n")
        print(f"---------------------------- | Caixa de Entrada {mail} | ----------------------------\n")
        while True:
            checkMails()
            time.sleep(5)

except(KeyboardInterrupt):
    deleteMail()
    print("\nPrograma Interrompido")
    os.system('cls' if os.name == 'nt' else 'clear')















