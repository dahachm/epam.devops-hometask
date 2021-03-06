# Hometask 6

## Task 1 
  С помощью утилиты nmcli добавить второй IP адрес сетевому интерфейсу enp0s3:
  
   - IP Адрес должен быть назначен из пула немаршрутизируемых в Интернете пулов (aka серых IP)
   - Адрес НЕ должен принадлежать пулу адресов, который уже назначен какому-либо из интерфейсов
   - В подсети нового адреса должно быть как можно меньше адресов (broadcast и network адрес назначать интерфейсу нельзя)
   - перезагрузить машину, убедиться что оба интерфейса имеют оба адреса (должна быть возможность подключиться по ssh к новому IP адресу с виртаульной машины)
   
   ___
   
   IP адрес, назначенный на интерфейс **enp0s3** - **10.0.2.15/24** (выдается автоматически службой *dhcp*).
   
   ![Результат работы команды](/6/screenshots/task1_1.png)
   
   Назначим ему 2-й IP адрес - **10.0.0.1/30** (всего 4 адреса в подсети: 2 хоста + broadcast + network):
   
   ```
   # nmcli con modify enp0s3 +ipv4.addresses "10.0.0.1/30"
   ```
   
   И проверим, как внесенные изменения отразились на кофигурационном файле интерфейса **enp0s8**:
   
   ```
   $ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
   ```
   
   ![Результат работы команды](/6/screenshots/task1_2.png)
   
   Перезагрузим машину и посмотрим на состояние **enp0s3**:
   
   ```
   # reboot
   ```
   
   ```
   $ ip a
   ```
   
   ![Результат работы команды](/6/screenshots/task1_3.png)
   
   Проверим возможность подключения к **10.0.0.1** по **ssh**:
   
   ![Результат работы команды](/6/screenshots/task1_4.png)
   ___  
     
   
## Task 2
  Новый IP адрес должен "резолвиться" в "private" DNS запись, а hostname вашей машины должен быть таким же, как у ближайшей галактики к нашей Солнечной системе 
(или выбрать обычное скучное имя). Продемонстрировать результаты с помощью  одной из утилит (dig, nslookup, host)* или другой.

  ___
  Настройка DNS сервера
  
  ```
  # yum install bind bind-utils
  # vi /etc/named.conf
  ```
  
  Добавить слово **any** в список прослушиваемых интерфейсов:
  
  ```
  listen-on port 53 { 127.0.0.1; any;};
  ```
  
  И в список адресов, которые могут обращаться на наш сервер:
  
  ```
  allow-query     { localhost; any; };
  ```
  
  В конец файла */etc/named.conf* (перед влючаемыми файлами с параметром *include*) добавить следующие описания именных зон (прямого и обратного просмотра):
  
  ```
  zone "mydomain" IN {
          type master;
          file "mydomain.zone";
          allow-update { none; };
  };

  zone "0.0.10.in-addr.arpa" IN {
          type master;
          file "mydomain.rzone";
          allow-update { none; };
  };
  
  ```
  
  Прямая зона *"mydomain"* - основная (type master), её таблица имён содержится в файле "/var/named/mydomain.zone", не получает обновления автоматически  (*allow-update { none; };*, иначе вместо *none* нужно было бы указать IP других dns) - используется для преобразования имён в зоне домена *"mydomain"* в соответствующие IP адреса согласно таблице имён этой зоны.
  
  Обратная (реверсивная) зона "0.0.10.in-addr.arpa" (IP адрес домена "mydomain" назначим **10.0.0.1**) - основная (type master), таблица имён "/var/named/mydomain.rzone", не получает обновления автоматически - используется для преобразования IP адресов в имена своей доменной зоны ("mydomain").
  
  После редактирования файла */etc/named.conf/* проверить его на наличие синтаксических ошибок:
  
  ```
  # named-checkconf /etc/named.conf
  ```
  
  Если вывод пустой - ошибок нет, иначе - комментарий к ошибке с указанием строки.
  
  ![Пример вывода команды](/6/screenshots/task2_3.png)
  
  Создаём */var/named/mydamoin.zone* со следующим содержимым:
  
  ```
  # vi /var/named/mydomain.zone
  ```
  
  ```
  $TTL 86400
  @       IN  SOA  mydomain. admin (
          2021020701      ; Serial - Серийный номер - если изменен, система поймет, что нужно загрузить обновленную таблицу
          3600            ; Refresh - время в секундах до следующей проверки таблицы на необходимость обновления
          1800            ; Retry - время в секундах, которое сервер ожидает при ошибочном сеансе refresh-а чтобы начать его заново
          604800          ; Expire - время, по истечению которого таблица считается устаревшей
          86400           ; Minimum TTL (time-to-live) - время хранения в кжше сервера данные таблицы
  )

          IN NS   mydomain. 

                  IN A 10.0.0.1
  task2           IN A 10.0.0.1

  ```
  
  Данная таблица позволит перевести именя **mydomain** и **task.mydomain** в адрес **10.0.0.1**. Cюда же можно добавлять записи с другими именами зоны **mydomain**.
  
  Создаём */var/named/mydamoin.rzone* со следующим содержимым:
  
  ```
  # vi /var/named/mydomain.rzone
  ```
  
  ```
  $TTL 86400
  @       IN  SOA  mydomain. admin.mydomain. (
          2021020702      ; Serial
          3600            ; Refresh
          1800            ; Retry
          604800          ; Expire
          86400           ; Minimum TTL
  )

          IN NS   mydomain.
  1       IN PTR  task2.mydomain.
  ```
  
  Теперь адрес **10.0.0.1** будет резолвиться в имя **task2.mydomain**.
  
  Проверим содержимое файлов с таблицами имен на наличие синтаксических ошибок:
  
  ```
  # named-checkzone task2.mydomain /var/named/mydomain.zone
  # named-checkzone task2.mydomain /var/named/mydomain.rzone
  ```
  
  ![Пример вывода команды](/6/screenshots/task2_4.png)
  
  Добавим адрес нового dns в файл */etc/resolv.conf*:
  
  ```
  nameserver 10.0.0.1
  ```
  
  Запустим службу named - сервер доменных имен из пакета *bind* (который устанавливали в начале), отвечает за то, чтобы внесенные нами только что настройки сервера вступили в силу.
  
  При первом запуске named: 
  
  ```
  # systemctl enable named
  # systemctl start named
  ```
  
  Или
  
  ```
  # systemctl restart named
  ```
  
  Демонстрация работы сервера с использованием утилиты **dig**:
  ```
  # dig -x 10.0.0.1
  ```
  
  ![Пример вывода команды](/6/screenshots/task2_5.png)
  
  Демонстрация работы сервера с использование утилиты **nslookup**:
  
  ```
  # nslookup 10.0.0.1
  ```
  
  Для обратного преобразования: 
  
  ```
  # nslookup task2.mydomain
  # nslookup mydomain
  ```
  
  ![Пример вывода команды](/6/screenshots/task2_6.png)
  
  ___
  
  Сменим hostname машины на **dracaena** (род растений, один экземляр такой Драцены окаймленной есть среди моих питомцев; *dracaena* с латинского некторые переводят как *драконша*).
  
  Чтобы посмотреть текущее значений *hostname*:
  
  ```
  # hostname 
  ```
  
  Чтобы установить новое значение *hostname*, можно внести изменение в файл */etc/hostname* и перезагрузить систему:
  
  ```
  # vi /etc/hostname
  # reboot
  ```
  
  ![Результат работы команды](/6/screenshots/task2_1.png)
  
  Или воспользоваться службой **hostnamectl**:
  
  ```
  # hostnamectl set-hostname dracaena
  # reboot
  ```
  
  ![Результат работы команды](/6/screenshots/task2_2.png)
  
  ___

## Task 3
  tcpdump и веселье:
  
   - Подключиться по ssh ко второму IP адресу интерфейса **enp0s3** машины, залогиниться.
   - В одной сессии запустить tcpdum, в другой сессии попытаться получить клиент контент страницы по адресу: example.com,  используя любой http.
   - Получить контент страницы с помощью telnet
   - В полученном выводе, найти содержимое страницы и все HTTP заголовки.
   - tcpdump команда должна быть максимально "узконаправленной", то есть, в выводе должно быть минимум трафика, не относящегося к цели задания.
   
   ___
   
   ```
   $ ssh admin@10.0.0.1
   ```
   
   ![Результат работы команды](/6/screenshots/task3_1.png)
   
   Запуск **tcpdump** для отслеживания трафика от/к ***example.com*** через интерфейс **enp0s3**:
   
   ```
   # tcpdump -n -i enp0s3 host example.com
   ```
   
   Получение страницы от ***example.com*** с использованием **curl**:
   
   ```
   $ curl http://example.com
   ```
   
   В ответ на запрос получаем содержимое страницы index.html на сервере **example.com**:
   
   ![Результат работы команды](/6/screenshots/task3_2.png)
   
   Для просмотра заголовков ответа сервера нужно добавить параметр **-I**:
   
   ```
   $ curl http://example.com -I
   ```
   
   ![Результат работы команды](/6/screenshots/task3_6.png)
   
   Анализ трафика, полученного **tcpdump** (*curl*):
   
   ![Результат работы команды](/6/screenshots/task3_4.png)
   
   Здесь и в следующем примере **клиент** - наша ВМ с IP адресом **10.0.2.15**, **сервер** - example.com c IP адресом **93.184.216.34**.
   
   Получение страницы index.html на **example.com** с использованием **telnet**:
   
   ```
   $ telnet example.com 80
   ...
   > GET / HTTP/1.1
   > HOST: example.com
   > [press enter]
   ```
   
   Получаем содержимое страницы index.html на сервере **example.com** (перед вывод содержимого отображаются и http заголовки ответа):
   
   ![Результат работы команды](/6/screenshots/task3_3.png)
   
   Для того, чтобы закрыть соединения необходимо нажать ***Ctrl***+**]** и ввести ***quit***.
   
   Анализ трафика, полученного **tcpdump**(*telnet*):
   
   ![Результат работы команды](/6/screenshots/task3_5.png)
   
   Утилита **telnet** работает по протоколу *telnet* и предназначена для удаленного управления путём передачи текстовых команд (из локального терминала) на сервер. В данной ситуации, мы подключились к порту 80, на котором "поднят" веб-сервер, и отправили http запрос GET на получение содержимого страницы index.html, расположенной на сервере.
   ___
  
## Task 4
  Найти номер порта, на котором запущен SSH сервер на хосте: **79.134.223.227** + все открытые порты.
  
  Следует быть готовым к тому, что сканирование ВСЕХ портов заёмет некоторое продолжительное время:
  
  ```
  # nmap -p- 79.134.223.227
  ```
  
  Как видно на рисунке ниже, сканирование дефолтных портов (1000 штук) не дало каких-либо значимых результатов - трафик на этих портах фильтруется (т.е. скорее всего блокируется брэндмауром или еще чем-то).
  
  ![Результат работы команды](/6/screenshots/task4_1.png)
  
  Спустя 3310.19 секунд (~ 56 минут) получаем результат: открыт только один порт - **60022**.
  
  Узнаем, что за служба обслуживает этот порт:
  
  ```
  # nmap -sV -p 60022 79.134.223.227
  ```
  
  ![Результат работы команды](/6/screenshots/task4_3.png)
  
  Таким образом выяснили, что на единсвтенном открытом порту на хосте **79.134.223.227** запущена служба **SSH**.
  

## Task 5
  Получить доступ на хост с адресом: **45.88.76.32**.
  Цель задания: найти сообщение в icmp трафике, который поступает на этот хост (на lo интерфейс и/или 45.88.76.32). Представить сообщнение 
  в читаемом варианте и предоставить команду которой вы пользовались, чтобы прочесть это сообщение. Подсказка: вам доступен tcpdump (/usr/sbin/tcpdump) на хосте.
  
  ___
  
  Утилита **tcpdump** позволяет выводить на экран содержимое перехватываемых пакетов: в ASCII- или hex-представлении.
  
  Здесь и далее отправляем **1** пакет на **127.0.0.1(localhost)** с помощью **ping**. **tcpdump** отслеживает трафик на интерфейсе **lo**, потому увидит полученный на **localhost** запрос и отправленный с **него же** ответ на запрос - т.е. 2 пакета (но с разным контентом).
  
  ```
  $ sudo tcpdump -i lo -A icmp
  ```
  
  ![Пример вывода команды](/6/screenshots/task5_1.png)
  
  ```
  $ sudo tcpdump -i lo -x icmp
  ```
  
  ![Пример вывода команды](/6/screenshots/task5_2.png)
  
  И моё любимое - параметр **-Х** - отображение содержимого пакета и в hex-, и в ASCII-представлении:
  
  ```
  $ sudo tcpdump -i lo -X icmp
  ```
  
  ![Пример вывода команды](/6/screenshots/task5_3.png)
  
  Значения *type* и *code* в заголовке ICMP пакета [несут смысловую нагрузку](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol#Control_messages), а также влияют на содержимое сегмента *data* в ICMP пакете.
  
  Поэтому, пытаясь выполнить часть задания **"Представить сообщение в читаемом варианте"**, представляю ниже скрипт (python2), который разбирает пакет с трафиком, записанным **tcpdump**, проверяет *тип* и *код* ICMP пакета и выводит соответсвующее сообщение, а также значения других полей IP и ICMP заголовков, сегмента данных ICMP пакета.
  
  Запись трафика в файл ***dumpfile*** с помощью **tcpdump**:
  
  ```
  $ sudo tcpdump icmp -i lo -w dumpfile 
  ```
  
  Далее запускаем [скрипт (python2)](/6/script1.py), который работает  с ***dumpfile*** (имя файла упоминается в коде, поэтому если на предыдущем шаге дается другое имя файла для записи, то соотвествующее изменение нужно внести в скрипт - строка 1):
  
  ```
  $ python script1.py
  ```
  
  Отправим 2 раза по одному пакету с разным содержимым с помощью **ping**:
  
  ![Пример вывода команды](/6/screenshots/task5_4.png)
  
  Полученные сообщения, обработанные нашим скриптом:
  
  ![Пример вывода команды](/6/screenshots/task5_5.png)
  
  ___
  
  
  
