<h2 align="center">Status: Working✅</h2>

[Русский](README.md)

# zoom - gif to avatar
## Allows you to put a GIF on the avatar in Zoom
#### Allows you to set a gif on your Zoom profile picture

<h1 align="center">Install 🚀 </h1>


1. Install [Git](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-Git) and Python version at least 3.7. You can do it like this:

    <h3>For Windows</h3>

    Download the installer from [official site](https://www.python.org/downloads/) and run it. Make sure you check the box ![Add Python to PATH](https://user-images.githubusercontent.com/42045258/69171091-557d2780-0b0c-11ea-8adf-7f819357f041.png)
    
    <h3>For Linux</h3>

    You most likely already have Python 3 installed. If not, follow the [guide](https://realpython.com/installing-python/#linux).

2. Enter the following commands ([where?](http://comp-profi.com/kak-vyzvat-komandnuyu-stroku-ili-konsol-windows/)):

```sh
git clone https://github.com/pozhiloy-enotik/zoom-gta
cd zoom-gta
pip3 install -r requirements.txt
```

##### For Termux also enter:
```sh
pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip install --upgrade wheel pillow
```
###### How to upload GIFs in Termux:
1. Create a folder "gifs" on the internal memory and upload gifs there
2. We write in the Termux console:
```sh
cd zoom-gta
cp /storage/emulated/0/gifs/*.gif ./
```


<h1 align="center">🚩 Launch</h1>

Enter the command `python3 main.py` or `python main.py` while in the directory of the cloned repository. <br/>
  <br/>
```sh
Enter your e-mail:
```
Your login email (registration required) <br/>
  <br/>
```sh
Enter your password:
```
Your zoom password. Don't be afraid, I won't steal)) <br/>
  <br/>
```sh
Enter captcha(saved as "captcha.png"):
```
Enter the captcha (On Termux a gallery will open, on systems with a GUI - a window with an input field)
#### Captcha is required only when adding an account, if your system does not have a GUI, you can copy the file "accounts.zoomgtadonotopenverysecret" <br/>
  <br/>

```sh
Enter the name of a .gif:
```
Enter the name of your GIF. It must be placed in the program directory. <br/>
  <br/>
```sh
Enter the delay:
```
Delay between profile picture changes (explained below)

____

## And now the most interesting))
### How does the program work?
Since you can’t just put an animated gif on your profile picture in Zoom, this program breaks it into frames and puts them in turn on your profile picture

### Limitations:
#### Works best with square gifs. You can crop here https://ezgif.com/crop
#### In the same place, you can delete unnecessary frames, I advise you to do this

#### The avatar update interval in the zoom client is about 1 second, which means that if the number of frames in your gif is 50, it will take about a minute to fully play it. Gif templates are in the examples/ folder
#### It is necessary to select a delay somewhere from 0.5 to 1 second.
##### Delay collection algorithm:
##### If there is frame drop, increase
##### If you need faster - reduce
To change the delay while the program is running:
- press Ctrl+C
- enter 4
____
If you like this program, please, [consider](https://donatepay.ru/don/pozhiloyenotik) [donating](https://www.donationalerts.com/r/pozhiloyenotik)

____
<h1 align="center">Update</h1>

Type the following command into the command line:
```sh
git pull
```
____
<h1 align="center">FAQ</h1>

### Endless captcha
  - To get started, log in to your account from a browser and enter the code from the mail so that the zoom remembers your ip
###

![Screenshot_464](https://user-images.githubusercontent.com/49619526/158879597-b0c4b72e-9f27-49f7-940d-4b70a0c2ab8d.png)

### Does not work
  - Update the program
  - Delete "accounts.zoomgtadonotopenverysecret"
  - Check that the information used to log in is correct.
  - Check again.
  - If you want to use a gif from the examples, then you need to not only write the name of the gif, but the full path to it
  ```sh
  Enter the name of a .gif:
  examples/loli
  ```
### Phantomjs demo out of credits
  - Register at https://phantomjscloud.com/
  - Enter api-key in the program
  
### UnicodeEncodeError: 'charmap' codec can't encode characters in position 16-19
  - Use normal command line, not Git Bash
 
### Color issue/inverted colors
  - Go here https://ezgif.com/optimize
  - Uploading a problem GIF
  - In the "Optimization method" select "Optimize Transparency" and turn the slider to 0. You can also try "Coalesce"
  - Click "Optimize gif"
  - Save


### If it didn't help
   - Drop the log in the telegram channel https://t.me/zoomgta
