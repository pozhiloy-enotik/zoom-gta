import requests
import time
from PIL import Image
import shutil


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
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest, OWASP CSRFGuard Project',
            #wtf is that
            'uQHR71Sqnk-a': 'fR4EEUJum7v4-_eijAf8sYWPaQ9BNO6wJ1ouLZfW-RGUrkz_lMdoN5LCTrzNkhguIWb8z9CDCcGPvq4BCM5a9cQrvqu0Nw8BfuKXa53hzIRq3JFBseA-=dgLukaM73osNAo87Wl_2DcZx9hF_d-vlCnyDbLR5SlJ6o49DTh=6Lz_gFmW3XL1SiEciSOESC9H94KlOCcZ3xS2nHPXL1wnn-0FnFR3s=7HrPElkUh5mU2vOU_LHCGU7cp1uW6_WizZGFmWYcR_=98I-aM5m8MLoypdJrQym7jndIdoSUWlqZ-bZpM_pKXp5hlz11pgrrkoWzJPCGuNviwCmx7l11OA3sXcquVZ9aDbWvwf6jfwD_s80V9oJW1LaywaN-b50BQEkXrAx9N943OTVhCmynjee=-l3eSdnao1U0CJTKDwgGWJdvLh5vabRJ5mnpRsm3xIEVVqZLT75ygsUR5dOEsOFIHNbyCeBobrDyvwZhgxOhmuKPm0FGq1F7frcL8rsf8JuQpuVZ35bsF6j=DuJenym3Z1KQ0dn-7fDEx-m=QDAM9uQiRag3WWHCP3FNhIR=cDCL0uXhmKeGDorQ0S3kksW5SJjOH2msEYPTqcSxijfHyifR7o7Fln9PK5bsoO6yT=K_LdA=-akHBKNkVCxQoVguoAyfIoNqgUuzE4sNXTiWVKQU-gJq0xJi92HoUYsj4Ti=FZagHI-Q16S5_WhHsqmxThXDbSnM0czjph6R84Sr22MU4YccYnPZ0qoGYxkTBMS5ySfU2EZPW-x_f0xun3H_7OvChL8_n0Y5cShrg9TBZYKi9jJDTMNBwAIAJpYIscNOy0Kso-K4-fCr9Pex1vRyfoPXwo5AaoYoSIXBczD1rdwGO0paeMRoQue57SkVRWDNRSr115w4v9cInqpGsPGeNa6ohCjnMr6V53KO0kEQjo3VzXqVYKd1fUxgAIijLuRR1_HRQW4Qgkyn8yv2pmeTi2rcqKb9ecH91N6l1di1Uw_Yh1YO4QeYF_BaQw_IrS4in1emkadKBeJcAqM00zh31lKIm47VPhBenu8pQGAw3W883J-2MeuWNnFF9uubEBeavmjhCiS2_s8NygoT4ozcLvXNF73miwfG8C75xeiLjKSFZFMXhrN_zUAnRWU=322BNrflrCfpnZl1VNP2LDXaaK3UjhTTVM=w-u-j=Ao2wlfS9nv3JgKOw=qhih00bkXzXA4lyBx6_UT_Q4gbg2ThTAnmFK=m4MPEuLCgZ0GkRk9KymV-IOyJlUYU9W9kpD8UayrJPkCZ9IqcSEopG092ZW6pkjPe3CMY9X2_KkY=2UU17QJ=eV37cpUIfQOMlsN8Un0jEqoX4PFQz57W7EE3BPgxBkY592MxEOHuDq8jElfsxhRh6OoQ6voDZfgTgC2wkgsMdPik7MNgMmCEsOkOpNvsLXQ0T4b58n004Krvu-Lax=8QIXVVGX2paCfCeL5v=QdWcb9xxp_SbVPB2fMWg38bEm7F=iGh7ZmDdKkl0lS-0ONbd5aNAexk7mijeWLiIF6MR5IRYvJj8GYIeOhlpi=h5X4IqdG0k2WjN5F8MSgR9zLLYcJWAgzSxIBZSgm-Z5pSD0=9j2rmb-p2ydAkEb_Yk6flffrzEWn4wlRuBZXOA_4QpGwBQwygl-kwRHiB3WOBOYuzz8ZuWR-3xeNyYAg5NyaaTch-qW-UPuYn6aTIP_exqnTRFIVTr6uXhSdfXISAd-OUCu86PO8JOgJNSeYc_rxk7jUyCOq2xLrsy97kIUP4sVpbFdxxpuSN5cHy1c41ne=1RwiOapkeZCjWKlDYfgNwnhiH1ddkwd1EKCvlyHIyL7SR5N8sLP2-1CD6A4gJwbEZzHIUHPYjUrzVA6CAqfJr7oVjR0aa9w=AvGwhPd=vpJ3VqEb4v00_oQkeiJ1MayXkBI9h2oJJdumywuNeT-InZWeysxy-rIzDRW444KNUfgSpLsC=QODLg1OKVkzYXaCdprja_G8JEmaZ3pJYQHd-WX4crdkz8lEL=rOEMezaMF1NrVzm9gZNxhWBaW1_ph_qlbGWsrhRnwWFfIIbzRiZJRuPn-l5uELpdQvd9HVE9Su8ngX5VY1Il2JL525jaBrm3UJKj3QA=4RpyAhXThWnlX5rve_5QaM7-hcAfx4ZcwClPjMJJWQ7apcmqeaPbeXE1kI2NN5YPwVOF8i42=5RrHNxEOQHfeYqdBTyNrKdz1pkWIAa1=ZO1qkBMx79KsjCb7GV4E8wmiwCT3kGeeTv=Y6HmvTgZa2ELKsav8Yr=16s1C5Efryy98-yTm-WWGjZxoqGyIpeNFri1nW8SucwU5YO7EHs9F-jJXWF0=fkfpXMaDrOHohCipopRxdM0WpW_Y73CohW3XFkYCZmW43ERoEvz=g=OCxdyOYiOjrZzP21yfGD3=jjg0P-7zH25NumfxBvm8W1x_jNvbRzibg7cpzkK=xpdyki6UsqDv6I8IHUHczYTI-RQkoAmwdMr4LQb36xeVswFO2B4N5DSxGTTom=IkwXhw3Hm1h4s0m51EdiynScBQgN5GVjSLZ7YfgbwC3qShjb3Crnc=F7aeg6mscyoSKQUZYBIhsccz10cZiIDmPm8ec9qKxAki46skfJPvnOSjCkQNJ8XuRgrJhXr9=wV_jJ0i6Wkm1_GRnQjTinEdpiAb_WSne_1IwJxf5UnYM6p8VMWETqTcX2h3i_0D_58_knjQV=jOQegqA36IhwqEk4gUKrP=XZcQBKmYZBCrr5_5vGdli2YPqyDXj0422uXLOqVjPiCrYLUxRNv6dlikGrnSfH1YZpGlM5BvX1DIuj2Un4O0mh6gD4voZ8qWdOI1oUMq22_l=r3gsH0QieSEYhLdd3UyPsZlISKb9plL88DZP=xoAwum2bQggUV=N8B48ga_Qn2qLHasohSj_R3-R5nix9SgcD1sJAOGA2ukyAxV4FG5QDq_0=GHKTYaW14m=CzonOGlCKy9JQrlLrAR_OSExPIB79d0bLjPq-MMWu8Fch3vVJEDEjD=srjL-axwPJrupCZS-lMSRxen6Op882exGiRNnjzNkpVKbyOcpGfW8SCIv-cVH-8CUaxw1cCI-kuXkFDMhd4BaOTVXpR-8SvkeU9L0oAiDd4--KyVymj3prO4JuG-MNwoN6KYXNWGFSdInUfp2g',
            'uQHR71Sqnk-b': 'nng7i0', 'uQHR71Sqnk-c': 'AMAWSQp6AQAAOrzhBlX2FA5naSfO2uvy2J_RWcOvDHwXY8B4vUf9am_hhRel',
            'uQHR71Sqnk-d': 'AA6ihIjBDKGNgUGASZAQhISy1WJH_Wpv4YUXpQAAAAAbvp8wAFNATWlFGONAg7xD0MJTKks',
            'uQHR71Sqnk-f': 'A2WvTAp6AQAAqd2JhCp81eGtv4M-gTyVaKQX5vCoxBuZ91Gh9gQk2yIMCSU8AbLMgJOcuAA7wH8AAEB3AAAAAA==',
            'uQHR71Sqnk-z': 'q',
            # ?
            'Content-Length': '597',
            'DNT': '1',
            'TE': 'Trailers'}
        self.images = []
        self.delay = 1
        self.wlog_url = 'https://us04web.zoom.us/wlog'
        self.upload_url = 'https://zoom.us/p/upload'
        self.auth_cookies = ''
        self.last_gif = ''
        self.last_frame = ''

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
        captcha_response = self.session.get(self.captcha_url)
        with open(filename, 'wb') as f:
            f.write(captcha_response.content)

    def get_auth_cookies(self, email, password, captcha):

        login_payload = {'email': email,
                         'password': password,
                         'keep_me_signin': "True",
                         'type': "100",
                         'captcha': captcha,
                         'captchaName': 'captcha-text'
                         }
        login_resp = self.session.post(self.login_url, data=login_payload, headers=self.login_headers)
        print(login_resp.status_code)
        if login_resp.json()['status']:
            self.auth_cookies = '; '.join(
                [x.name + '=' + x.value for x in self.session.cookies if x.name in self.needed_auth])
            return True
        else:
            print(login_resp.json())
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
                    new_im = frame.resize((400, 400), Image.ANTIALIAS)
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
