[English(Google-translate)](README-ENG.md)

# zoom - gif to avatar
## Позволяет поставить гифку на аватарку в Zoom 
#### Allows you to set a gif on your Zoom profile picture 

<h1 align="center">Установка 🚀 </h1>


1. Установите Python версии не ниже 3.7. Сделать это можно так:

    <h3>Для Windows</h3>

    Скачайте установщик с [официального сайта](https://www.python.org/downloads/) и запустите его. Убедитесь, что при установке отметили галочку ![Add Python to PATH](https://user-images.githubusercontent.com/42045258/69171091-557d2780-0b0c-11ea-8adf-7f819357f041.png)
    
    <h3>Для Linux</h3>

    Скорее всего у вас уже установлен Python 3. Если это не так, следуйте [гайду](https://realpython.com/installing-python/#linux).

2. Введите следующие команды ([куда?](http://comp-profi.com/kak-vyzvat-komandnuyu-stroku-ili-konsol-windows/)):

```sh
git clone https://github.com/pozhiloy-enotik/zoom-gta
cd zoom-gta
pip3 install -r requirements.txt
```

#####      Дополнительно для Termux:
```sh
pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip install --upgrade wheel pillow
```
###### Как закидывать гифки в Termux:
1. Создаем на внутренней памяти папку "gifs" и закидываем туда гифки
2. Прописываем в консоли Termux:
```sh
cd zoom-gta
cp /storage/emulated/0/gifs/*.gif ./
```


<h1 align="center">🚩 Запуск</h1>

Введите команду `python3 main.py` или `python main.py`, находясь в директории склонированного репозитория.  <br/>
  <br/>
```sh
Enter your e-mail:
```
Ваша почта, используемая для входа (необходимо зарегистрироваться)  <br/>
  <br/>
```sh
Enter your password:
```
Ваш пароль от zoom. Не бойтесь, не украду))  <br/>
  <br/>
```sh
Enter the name of a .gif:
```
Вводите название вашей гифки. Ее необходимо поместить в директорию программы.  <br/>
  <br/>
```sh
Enter the delay:
```
Задержка между сменами картинки профиля(ниже пояснение)

____

## А теперь самое интересное))
### Как работает программа?
Так как просто поставить анимированную гифку на аватарку в Zoom нельзя, данная программа разбивает ее на кадры и по очереди ставит их на вашу картинку профиля

### Ограничения: 
#### Лучше всего работает с квадратными гифками. Обрезать можно тут https://ezgif.com/crop
#### Там же, можно удалить ненужные кадры, советую вам это сделать

#### Интервал обновления аватарки в клиенте зума около 1 секунды, это значит что если количество кадров в вашей гифке 50, на полное ее воспроизведение уйдет около минуты. Эталоны гифок есть в папке examples/
#### Необходимо подбирать задержку где-то от 0.5 до 1 секунды.
##### Алгоритм подборки задержки:
##### Если есть пропуск кадров - увеличьте
##### Если надо быстрее - уменьшите
Для смены задержки во время выполнения программы:
- нажмите Ctrl + C
- введите 4
____
Создатель хочет кушать, [помоги](https://donatepay.ru/don/pozhiloyenotik) [создателю](https://www.donationalerts.com/r/pozhiloyenotik)

____
<h1 align="center">Обновление</h1>

Введите следующую команду в командную строку:
```sh
git pull
```
____
<h1 align="center">FAQ</h1>

### Не работает
  - Обновите программу
  - Проверьте правильность данных, используемых для входа. 
  - Проверьте еще раз. 
  - Скиньте лог в телеграм канал https://t.me/zoomgta
  
### Проблема с цветами/инвертированные цвета
  - Переходим сюда https://ezgif.com/optimize
  - Загружаем проблемную гифку
  - В "Optimization method" выбираем "Optimize Transparency" и выкручиваем ползунок на 0. Так же, можно попробовать "Coalesce"
  - Нажимаем "Optimize gif"
  - Сохраняем
