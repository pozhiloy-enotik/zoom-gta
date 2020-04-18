import gif
import os
import pickle
import configparser

ACCOUNTS_FILE = 'accounts.zoomgtadonotopenverysecret'
CONFIG_FILE = 'config.zoomgta.ini'
gif = gif.Gif()
cfg = configparser.ConfigParser()

if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
    cfg.read(CONFIG_FILE)
    def_gif = cfg['General']['DefaultGifPath']
    def_delay = cfg['General']['DefaultDelay']
else :
    def_gif = None
    def_delay = 1

if os.path.exists(ACCOUNTS_FILE) and os.path.getsize(ACCOUNTS_FILE) > 0:
    accounts = pickle.load(open(ACCOUNTS_FILE, 'rb'))
else:
    accounts = []
# start_gui = input('Start GUI? (y/n)')
# if start_gui == 'y':
#     import gui
#     exit(0)
# TODO: GUI
print('If you like this program, please, consider donating:\n'
      'https://donatepay.ru/don/pozhiloyenotik\n'
      'https://www.donationalerts.com/r/pozhiloyenotik')


def save_account(account):
    accounts.append(account)
    with open(ACCOUNTS_FILE, 'wb') as file:
        pickle.dump(accounts, file)


def delete_account(number):
    accounts.pop(number-1)
    with open(ACCOUNTS_FILE, 'wb') as file:
        pickle.dump(accounts, file)


def save_config(dgif, ddelay):
    if def_gif != None:
        cfg['General']['DefaultGifPath'] = dgif
        cfg['General']['DefaultDelay'] = ddelay
    else:
        cfg.add_section('General')
        cfg.set('General', 'DefaultGifPath', dgif)
        cfg.set('General', 'DefaultDelay', ddelay)
    with open(CONFIG_FILE, 'w') as configfile:
           cfg.write(configfile)


def log_in():
    i = 1
    while i <= len(accounts):
        print(str(i) + '.', accounts[i - 1])
        i += 1
    choice = int(input(str(i) + '. ' + 'Add an account\n' +
                       str(i + 1) + '. ' + 'Delete an account\n'))
    if choice == i:
        email = input('Enter your e-mail:\n')
        password = input('Enter your password:\n')
        if int(input('Do you want to save this account?\n'
                     '1. Yes\n'
                     '2. No\n')):
            save_account((email, password))

    elif choice == i + 1:
        delete_account(int(input('Enter the number of the account\n')))
        log_in()
        return
    else:
        email, password = accounts[choice - 1]
    print('Processing...')
    result = gif.log_in(email, password)
    if result:
        return True
    else:
        print('Wrong email or password')
        log_in()


def upload():
    if def_gif == None:
        file = input('Enter the name of a .gif:\n')
    else:
        file = input('Enter the name of a .gif ( '+def_gif+' ) :\n')
        if file == '':
            file = def_gif
    path = os.path.join(os.path.curdir, file)
    result = gif.process_image(path)
    if result:
        print('Not a .gif')
        upload()
    return file


def set_delay():
    if def_gif == None:
        gif.delay = float(input('Enter the delay:\n').replace(',', '.'))
    else:
        inp = input('Enter the delay ( '+str(def_delay)+' ) :\n')
        if inp == '':
            gif.delay = float(def_delay)
        else:
            gif.delay = float(inp.replace(',', '.'))
    return str(gif.delay)

log_in()
save_config(upload(), set_delay())


while True:
    print('Starting... Press Ctrl+C to stop')
    length = len(gif.images)
    i = 0
    try:
        while True:
            status = gif.change_picture(0, 0, f'{gif.w}', f'{gif.h}', gif.images[i])
            i += 1
            if i == length:
                i = 0
            if status['status']:
                print('Frame:', i)
            else:
                print('Frame', i, f'skipped. An error occurred: "{status["errorMessage"]}"')
    except KeyboardInterrupt:
        print('Stopped')
        a = int(input('1. Start\n'
                      '2. Change account\n'
                      '3. Change gif\n'
                      '4. Change delay\n'
                      '5. Exit\n'))
        if a == 1:
            pass
        elif a == 2:
            log_in()
        elif a == 3:
            upload()
        elif a == 4:
            set_delay()
        elif a == 5:
            exit()
