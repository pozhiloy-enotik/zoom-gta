import gif
import os

gif = gif.Gif()


# start_gui = input('Start GUI? (y/n)')
# if start_gui == 'y':
#     import gui
#     exit(0)
# TODO: GUI
print('If you like this program, please, consider donating:\n'
      'https://donatepay.ru/don/pozhiloyenotik\n'
      'https://www.donationalerts.com/r/pozhiloyenotik')


def log_in():
    email = input('Enter your e-mail:\n')
    password = input('Enter your password:\n')
    print('Processing...')
    gif.log_in(email, password)
    upload()


def upload():
    file = input('Enter the name of a .gif:\n')
    print('Uploading')
    path = os.path.join(os.path.curdir, file)
    # print(path)
    result = gif.process_image(path)
    if result:
        print('Not a .gif')
        upload()


def set_delay():
    gif.delay = float(input('Enter the delay:\n').replace(',', '.'))


log_in()
set_delay()

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
                      '4. Change delay\n'))
        if a == 1:
            pass
        elif a == 2:
            log_in()
        elif a == 3:
            upload()
        elif a == 4:
            set_delay()
