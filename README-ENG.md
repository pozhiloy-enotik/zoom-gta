[Русский](README.md)

# zoom - gif to avatar
## Lets you put a gif on your avatar in Zoom
<h1 align = "center"> Installation 🚀 </h1>


1. Install Python version no lower than 3.7. You can do it this way:

    <h3> For Windows </h3>

    Download the installer from the [official site](https://www.python.org/downloads/) and run it. Be sure to check the box ![Add Python to PATH](https://user-images.githubusercontent.com/42045258/69171091-557d2780-0b0c-11ea-8adf-7f819357f041.png)
    
    <h3> For Linux </h3>

    Most likely you already have Python 3 installed. If this is not the case, follow the [guide](https://realpython.com/installing-python/#linux).

2. Enter the following commands ([where?](Http://comp-profi.com/kak-vyzvat-komandnuyu-stroku-ili-konsol-windows/)):

```sh
git clone https://github.com/pozhiloy-enotik/zoom-gta
cd zoom gta
pip3 install -r requirements.txt
```
#####      For Termux also enter:
```sh
pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip install --upgrade wheel pillow
```




<h1 align = "center"> 🚩 Launch </h1>

Enter the command `python3 main.py` or `python main.py` while in the directory of the cloned repository. <br/>
  <br/>
```sh
Enter your e-mail:
```
Your email address used to log in (register required) <br/>
  <br/>
```sh
Enter your password:
```
Your password is from zoom. Do not be afraid, do not steal)) <br/>
  <br/>
```sh
Enter the name of a .gif:
```
Enter the name of your gif. It must be placed in the program directory. <br/>
  <br/>
```sh
Enter the delay:
```
Delay between profile picture shifts (explanation below)

____

## And now the most interesting))
### How does the program work?
Since you can’t just put an animated gif on an avatar in Zoom, this program breaks it into frames and puts them on your profile picture in turn

### Limitations:
#### Fingerprint must be square, otherwise crop to the left. You can trim here https://ezgif.com/crop
#### In the same place, you can delete unnecessary frames, I advise you to do this

#### The avatar update interval in the zoom client is about 1 second, which means that if the number of frames in your GIF is 50, it will take about a minute to fully play it. The standards of gifs are in the examples / folder
#### It is necessary to select a delay somewhere from 0.5 to 1 second.
##### Delay matching algorithm:
##### If there is a frame skip - increase
##### Reduce if necessary - reduce
To change the delay during program execution:
- press Ctrl + C
- enter 4
____
If you like this program, please, [consider](https://donatepay.ru/don/pozhiloyenotik) [donating](https://www.donationalerts.com/r/pozhiloyenotik)

____
<h1 align = "center"> Update </h1>

Enter the following command at the command prompt:
```sh
git pull
```
