# Hometask 8

## l.15

### Подключить репозиторий docker community edition
  
  ```
  $ sudo yum install yum-utils -y
  $ sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  ```
  
  ![Пример вывода команды](/8/screenshots/15task1_1.png)
  
  ![Пример вывода команды](/8/screenshots/15task1_2.png)

### Установить docker-ce версии 19.03.14
  
  ```
  $ sudo yum install docker-ce-19.03.14 -y
  ```

### Убедиться, что установлена нужная версия
  
  ```
  $ sudo yum list installed dicker-ce
  ```
  
  ![Пример вывода команды](/8/screenshots/15task3_1.png)
  
### Обновить docker-ce до последней версии
  
  ```
  $ sudo yum update docker-ce -y
  ```
  
  ![Пример вывода команды](/8/screenshots/15task4_1.png)
  
### Вывести список последних операций yum

  ```
  $ sudo yum history list
  ```
  
  ![Пример вывода команды](/8/screenshots/15task5_1.png)
  
### Вывести полную информацию об установленном ранее пакете
  
  ```
  $ sudo yum info docker-ce
  ```
  
  ![Пример вывода команды](/8/screenshots/15task6_1.png)
  
### Удалить docker-ce
  
  ```
  $ sudo yum remove docker-ce
  ```
  
  ![Пример вывода команды](/8/screenshots/15task7_1.png)


## l.16

### Переместить mlocate.db в новое место
  
  Сразу после установки **mlocate** в моей системе отсутствовал файл *mlocate.db*. Потому сначала вызвала утилиту **updatedb**, которая обновляет/создает содержимое файла *mlocate.db*, а затем проверила(нашла) расположение файла *mlocate.db*:
  
  ```
  $ sudo updatedb
  $ sudo find / -name mlocate.db 
  ```
  
  ![Пример вывода команды](/8/screenshots/16task1_1.png)
  
  
  Затем переместила указанный файл в домашнюю директорию пользователя *admin*:
  
  ```
  $ sudo mv /var/lib/mlocate/mlocate.db ~/mlocate.db
  ```
  
  ![Пример вывода команды](/8/screenshots/16task1_2.png)
  
### Создать новый файл file_task16.txt с любым содержанием и добавить информацию о нём в новый mlocate.db
  
  Создание файла **file_task16.txt**:
  ```
  $ echo "Some content ... la la la ..." > file_task16.txt
  ```
  
  Обновление (перемещенной) БД для **locate**:
  
  ```
  $ sudo update -o ~/mlocate.db
  ```
  
  Для проверки того, что запись добавлена в *нужную* БД:
  
  ```
  $ sudo locate -d ~/mlocate.db file_task16.txt
  ```
  
  ![Пример вывода команды](/8/screenshots/16task2_1.png)
  
  Без указания пути к БД (через парметр **-d**) **locate** сообщит об ошибке, связанной с тем, что дефолтный файл БД недоступен.
  
### Найти файл file_task16.txt через locate и вывести его содержимое на экран (без явного указания полного пути к файлу)
  
  ```
  $ cat $(sudo locate -s ~/mlocate.db file_task16.txt)
  ```
  
  ![Пример вывода команды](/8/screenshots/16task3_1.png)

### Создать хардлинк на file_task16.txt, назвать его file_task16_hard.txt
  
  ```
  $ ln file_task16.txt file_task16_hard.txt
  ```
  
  ![Пример вывода команды](/8/screenshots/16task4_1.png)
  
  
### Внести любые изменения в file_task16.txt
  
  ```
  $ echo "Brand new la la la ..." >> file_task16.txt
  ```
  
  ![Пример вывода команды](/8/screenshots/16task5_1.png)
  
### Удалить file_task16.txt
  
  ```
  $ rm file_task16.txt
  ```
  
  ![Пример вывода команды](/8/screenshots/16task6_1.png)
  
### Вывести на экран file_task16_hard.txt, убедиться, что в нём отражены изменения
  
  ```
  $ cat file_task16_hard.txt
  ```
  
  ![Пример вывода команды](/8/screenshots/16task7_1.png)
  
  


* Создать именованный пайп pipe01
	  В первом терминале запустить считывание с pipe01 (любым способом, можно перечислить несколько)
	  Создать софтлинк на пайп, назвать его pipe01-s
	  Во втором терминале отправить в pipe01-s данные (любым способом, можно перечислить несколько)
	  Убедиться, что данные были считаны первым терминалом
	  # mkfifo
	** Сделать то же самое, используя файл Unix socket (подсказка: используйте пакеты netcat и socat)
