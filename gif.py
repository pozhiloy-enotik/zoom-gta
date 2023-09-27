import requests
import time
from PIL import Image
import shutil
import random
import string
import json


class Gif:
    def __init__(self, auth_cookies=''):
        self.login_url = 'https://zoom.us/signin'
        self.save_url = 'https://zoom.us/p/save'
        self.captcha_url = 'https://zoom.us/captcha-image?type=1'
        self.csrf_headers = {'FETCH-CSRF-TOKEN': '1'}
        self.needed = ['_zm_page_auth', '_zm_kms', 'zm_gnl_guid', 'zm_gnl_ruid']
        self.needed_temp = ['zm_gnl_guid', 'zm_gnl_ruid']
        self.needed_auth = ['_zm_page_auth', '_zm_kms']
        self.save_payload = {"userId": "",
                             "file": "",
                             "x": "0", "y": "0", "w": "438", "h": "438"}
        self.login_headers = {}
        self.images = []
        self.delay = 1
        self.wlog_url = 'https://us04web.zoom.us/wlog'
        self.upload_url = 'https://zoom.us/p/upload'
        self.auth_cookies = ''
        self.last_gif = ''
        self.last_frame = ''
        self.phantomjs_url = 'http://PhantomJScloud.com/api/browser/v2/{}/'
        self.phantomjs_data = {
            "url": "https://zoom.us/signin",
            'outputAsJson': 'true',
            "renderType": "automation",
            'requestSettings': {'ignoreImages': True},
            "overseerScript": f"""
            await page.waitForNavigation("networkidle2");
            let _user="{self.random_string(2) + '@' + self.random_string(2) + '.' + self.random_string(4)}"; 
            let _pass="{self.random_string(4)}"; 
            await page.type("input#email",_user); 
            await page.waitForSelector("input#password"); 
            await page.evaluate(".signinNeedCaptcha=false");
            await page.type("input#password",_pass); 
            page.click("button#js_btn_login"); 
            page.meta.store.set("request", await page.waitForRequest("https://zoom.us/signin/route"));
            let cookies = await page.cookies();
            page.meta.store.set("cookies", cookies);"""}

    def random_string(self, y):
        return ''.join(random.choice(string.ascii_letters) for _ in range(y))

    def make_session(self):
        self.session = requests.Session()

    def process_cookies(self):
        cookie = '; '.join(
            [x.name + '=' + x.value for x in self.session.cookies])
        self.upload_headers = {'Content-Length': '1998866',
                               'Cookie': cookie,
                               'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
                               }
        self.save_headers = {
            'Content-Length': '169', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie,
            'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
        }

    def get_captcha(self, filename):
        captcha_response = self.session.get(self.captcha_url, headers=self.login_headers)
        with open(filename, 'wb') as f:
            f.write(captcha_response.content)

    def process_phantomjs(self, api_key=''):
        if api_key:
            url = self.phantomjs_url.format(api_key)
        else:
            url = self.phantomjs_url.format("a-demo-key-with-low-quota-per-ip-address")
        phantomjs_response = requests.post(url, data=json.dumps(self.phantomjs_data)).json()
        try:
            self.login_headers = phantomjs_response['storage']['request']['headers']
        except:
            if 'OUT OF CREDITS' in phantomjs_response['message']:
                print('Phantomjs demo out of credits. Read FAQ')
                return 2
            else:
                print(phantomjs_response)
                exit(0)
        self.login_headers['Cookie'] = '; '.join(
            [x['name'] + '=' + x['value'] for x in phantomjs_response['storage']['cookies']])

    def get_auth_cookies(self, email, password, captcha):
        login_payload = {'email': email,
                         'password': password,
                         'keep_me_signin': "True",
                         'type': "100",
                         'captcha': captcha,
                         }
        login_resp_raw = self.session.post(self.login_url, data=login_payload, headers=self.login_headers)
        try:
            login_resp = login_resp_raw.json()
        except:
            print('Error: Code ' + str(login_resp_raw.status_code))
            exit(0)
        if login_resp['status']:
            self.auth_cookies = '; '.join(
                [x.name + '=' + x.value for x in self.session.cookies if x.name in self.needed_auth])
            return True
        else:
            print(login_resp)
            return False

    def get_temp_cookies(self):
        self.token = self.session.post('https://zoom.us/csrf_js',
                                       headers=self.csrf_headers).text[15:]
        self.session.headers.update({'ZOOM-CSRFTOKEN': self.token})

    def change_picture(self, x, y, w, h, file_url):
        self.save_payload['x'] = x
        self.save_payload['y'] = y
        self.save_payload['w'] = w
        self.save_payload['h'] = h
        self.save_payload['file'] = file_url or self.save_payload['file']

        save_response = self.session.post(self.save_url, data=self.save_payload, headers=self.save_headers)
        time.sleep(self.delay)
        try:
            return save_response.json()
        except:
            return {'status': False, "errorMessage": save_response.status_code}

    def upload_picture(self, file):
        files = {'file': file}
        upload_response = self.session.post(self.upload_url, files=files, headers=self.upload_headers)
        try:
            return upload_response.json()
        except:
            if upload_response.status_code == 403:
                return {"status": False, "errorCode": 201}
            else:
                print(upload_response)
                print(upload_response.content)
                raise Exception('Something went wrong with the upload:', upload_response)

    # Print iterations progress
    def print_progress_bar(self, iteration, total, prefix='', suffix='', decimals=0, length=100, fill='█',
                           print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(u'\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()

    def process_image(self, infile):
        """
        Errors:
        1 - Not a gif
        2 - User not login
        """

        if ('0000' + infile)[-4] != '.':
            infile += '.gif'
        try:
            frame = Image.open(infile)
        except IOError:
            print("Cant load", infile)
            return 1
        i = 0
        frames = frame.n_frames
        bar_length, temp = shutil.get_terminal_size()
        bar_length = bar_length - 23
        if self.last_gif == infile:
            i = self.last_frame
        else:
            self.images = []
            self.last_gif = infile
        try:
            while frame:
                self.last_frame = i
                self.w, self.h = frame.size
                new_im = frame
                if self.w == self.h and self.h <= 400:
                    new_im = frame.resize((400, 400), Image.LANCZOS)
                    self.w, self.h = new_im.size
                new_im.save('temp.gif', 'gif')
                res = self.upload_picture(open('temp.gif', 'rb'))
                success = res["status"]
                if not success:
                    if res["errorCode"] == 201:
                        return 2
                    else:
                        raise Exception(res["errorCode"], res["errorMessage"])
                self.images.append(res['result'])
                self.print_progress_bar(i, frames, prefix='Uploading... ', suffix='', length=bar_length)
                i += 1
                frame.seek(i)
        except EOFError:
            pass
        self.print_progress_bar(i, frames, prefix='Uploading... ', suffix='', length=bar_length, print_end='\n')
        link = self.images[-1]
        start = link.find('zoom.us/p/') + 10
        end = start
        while link[end] != '/':
            end += 1
        self.save_payload["userId"] = link[start:end]
        print('Frames:', len(self.images))
        return 0


if __name__ == '__main__':
    pass
