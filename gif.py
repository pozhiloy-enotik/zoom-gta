import requests
import time
from PIL import Image
import os


class Gif:
    def __init__(self):
        self.login_url = 'https://zoom.us/signin'
        self.save_url = 'https://zoom.us/p/save'

        self.csrf_headers = {'FETCH-CSRF-TOKEN': '1'}
        self.needed = ['_zm_page_auth', '_zm_kms']
        self.save_payload = {"userId": "",
                             "file": "",
                             "x": "0", "y": "0", "w": "438", "h": "438"}
        self.save_headers = {
            'Content-Length': '169', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '_zm_page_auth={}; _zm_kms={};',
            'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
            'ZOOM-CSRFTOKEN': ''}
        self.images = []
        self.delay = 1
        self.wlog_url = 'https://us04web.zoom.us/wlog'
        self.upload_url = 'https://zoom.us/p/upload'

    def log_in(self, email, password):
        self.session = requests.Session()
        login_payload = {'email': email,
                         'password': password,
                         'keep_me_signin': "True",
                         'type': "100"}
        login_resp = self.session.post(self.login_url, data=login_payload)

        if login_resp.json()['status']:
            self.save_headers['Cookie'] = '; '.join(
                [x.name + '=' + x.value for x in login_resp.cookies if x.name in self.needed])
            self.save_headers['ZOOM-CSRFTOKEN'] = self.session.post('https://us04web.zoom.us/csrf_js',
                                                                    headers=self.csrf_headers).text[15:]
            time.sleep(0.5)
            return True
        else:
            return False

    def change_picture(self, x, y, w, h, file_url):
        self.save_payload['x'] = x
        self.save_payload['y'] = y
        self.save_payload['w'] = w
        self.save_payload['h'] = h
        self.save_payload['file'] = file_url or self.save_payload['file']

        save_response = self.session.post(self.save_url, data=self.save_payload, headers=self.save_headers)
        # print(save_response.text)
        time.sleep(self.delay)
        return save_response.json()

    def upload_picture(self, file):
        upload_headers = {'Content-Length': '1998866',
                          # 'Content-Type': 'multipart/form-data; boundary=---------------------------34734475097515124353736042401',
                          'Cookie': self.save_headers['Cookie'],
                          'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
                          'ZOOM-CSRFTOKEN': self.save_headers['ZOOM-CSRFTOKEN']}
        files = {'file': file}
        upload_response = self.session.post(self.upload_url, files=files, headers=upload_headers)
        print(upload_response.text)
        return upload_response.json()

    def process_image(self, infile):
        self.images = []
        if ('0000' + infile)[-4] != '.':
            infile += '.gif'
        try:
            frame = Image.open(infile)
        except IOError:
            print("Cant load", infile)
            return 1
        i = 0

        try:
            while frame:
                self.w, self.h = frame.size
                if self.w == self.h and self.h <= 400:
                    frame.resize((400, 400), Image.ANTIALIAS)
                    self.w, self.h = frame.size
                frame.save('temp.gif', 'gif')
                self.images.append(self.upload_picture(open('temp.gif', 'rb'))['result'])
                i += 1
                frame.seek(i)

        except EOFError:
            pass
        link = self.images[-1]
        start = link.find('zoom.us/p/') + 10
        end = start
        while link[end] != '/':
            end += 1
        self.save_payload["userId"] = link[start:end]
        return 0


if __name__ == '__main__':
    pass
