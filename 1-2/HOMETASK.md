# Hometask 1-2

## Task 1
Используя команду ls, необходимо вывести на экран все файлы, которые расположены в секционных директориях /usr/share/man/manX и содержат слово "config" в имени. 
```sh
$ ls /usr/share/man/man?/*config*
```
![Пример вывода команды](/1-2/screenshots/task1_1.png)

Одним вызовом ls найти все файлы, содержащие слово "system" в каталогах /usr/share/man/man1 и /usr/share/man/man7
```sh
$ ls /usr/share/man/man[1,7]/*system*
```
![Пример вывода команды](/1-2/screenshots/task1_2.png)


