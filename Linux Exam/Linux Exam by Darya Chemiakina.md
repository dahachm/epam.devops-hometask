# Linux Exam. by Darya Chemiakina.

## Задача
Установить, настроить и запустить Hadoop Сore в минимальной конфигурации. Для этого потребуется подготовить 2 виртуальные машины: *VM1 - headnode*; *VM2 - worker*. Понимание принципов работы Hadoop и его компонентов для успешной сдачи задания не требуется.
Все инструкции и команды для каждого шага задания должны быть сохранены в файле.

## Шаг 1
> Установить CentOS на 2 виртуальные машины с учетом следующих требований к конфигурации:

* **VM1**: 2CPU, 2-4G памяти, системный диск на 15-20G и дополнительные 2 диска по 5G
    
    ![](C:\epam\Images\screenshot_0.png)

* **VM2**: 2CPU, 2-4G памяти, системный диск на 15-20G и дополнительные 2 диска по 5G
    
    ![](C:\epam\Images\screenshot_00.png)

## Шаг 2
> При установке CentOS создать дополнительного пользователя **exam** и настроить для него использование sudo без пароля. Все последующие действия необходимо выполнять от этого пользователя, если не указано иное.

Создание пользователя **exam**
```
$ sudo useradd exam
```
Для того, чтобы пользователь **exam** мог выполнять команды sudo без ввода пароля в файл 
*/etc/sudoers* добавить следующую запись:
```
%exam   ALL=(ALL:ALL) NOPASSWD: ALL
```

## Шаг 3
> Установить OpenJDK8 из репозитория CentOS.

Установка OpenJDK8:
```
$ sudo yum install java-1.8.0-openjdk -y
```
Проверка:
```
$ java -version
```
Версия JDK: 

![](C:\epam\Images\screenshot_2.png)

## Шаг 4
> Скачать архив с Hadoop версии 3.1.2 (https://hadoop.apache.org/release/3.1.2.html).

Установить *wget*:
```
$ sudo yum install wget -y
```
Затем загрузить архив по ссылке:
```
$ wget https://archive.apache.org/dist/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz
```
Процесс загрузки: 

![](C:\epam\Images\screenshot_3.png)

## Шаг 5
> Распаковать содержимое архива в */opt/hadoop-3.1.2/*.

```
$ sudo tar -xf hadoop-3.1.2.tar.gz -C /opt/
```

![](C:\epam\Images\screenshot_4.png)

## Шаг 6
> Сделать симлинк /usr/local/hadoop/current/ на директорию */opt/hadoop-3.1.2/*.

```
$ sudo mkdir /usr/local/hadoop
```
```
$ sudo ln -s /opt/hadoop-3.1.2 /usr/local/hadoop
```
```
$ sudo mv /usr/local/hadoop/hadoop-3.1.2 /usr/local/hadoop/current
```

![](C:\epam\Images\screenshot_5.png)

## Шаг 7
> Создать пользователей **hadoop**, **yarn** и **hdfs**, а также группу **hadoop**, в которую необходимо добавить всех этих пользователей.

Создание группы **hadoop**:
```
$ sudo groupadd hadoop
```
Создание пользователей **hadoop**, **yarn**, **hdfs** в группе **hadoop**:
```
$ sudo useradd hadoop -g hadoop
$ sudo useradd yarn -g hadoop
$ sudo useradd hdfs -g hadoop
```

![](C:\epam\Images\screenshot_6.png)

## Шаг 8
> Создать для обоих дополнительных дисков разделы размером в 100% диска.

```
$ sudo parted /dev/sdb
> mktable
> ... gpt
> mkpart
> Partition name?  []? [Enter]
> File system type?  [ext2]? [Enter]
> Start? 0%
> End? 100%
```

![](C:\epam\Images\screenshot_8.png)

![](C:\epam\Images\screenshot_9.png)

## Шаг 9
> Инициализировать разделы из п.8 в качестве физических томов для LVM.

Установить флаги на разделах из п.8 */dev/sdb* и */dev/sdc*:
```
$ sudo parted /dev/sdb
> set 1 lvm on
```

![](C:\epam\Images\screenshot_10.png)

```
$ sudo pvcreate /dev/sdb1
$ sudo pvcreate /dev/sdc1
```

![](C:\epam\Images\screenshot_11.png)

## Шаг 10 
> Создать две группы LVM и добавить в каждую из них по одному физическому тому из п.9.

```
$ sudo vgcreate vg1 /dev/sdb1
$ sudo vgcreate vg2 /deb/sdc1
```

![](C:\epam\Images\screenshot_12.png)

![](C:\epam\Images\screenshot_13.png)

## Шаг 11
> В каждой из групп из п.10 создать логический том LVM размером 100% группы.

```
$ sudo lvcreate -n /dev/vg1/LV1 -l 100%VG vg1
$ sudo lvcreate -n /dev/vg2/LV2 -l 100%VG vg2
```

![](C:\epam\Images\screenshot_14.png)

![](C:\epam\Images\screenshot_15.png)

## Шаг 12
> На каждом логическом томе LVM создать файловую систему ext4.

```
$ sudo mkfs -t ext4 /dev/vg1/LV1
$ sudo mkfs -t ext4 /dev/vg2/LV2
```

![](C:\epam\Images\screenshot_16.png)

![](C:\epam\Images\screenshot_17.png)

![](C:\epam\Images\screenshot_18.png)

## Шаг 13
> Создать директории и использовать их в качестве точек монтирования файловых систем из п.12 (/opt/mount1 и /opt/mount2 соответсвенно).

```
$ sudo mkdir /opt/mount{1,2}
```
```
$ sudo mount /dev/mapper/vg1-LV1 /opt/mount1
$ sudo mount /dev/mapper/vg2-LV2 /opt/mount2
```

![](C:\epam\Images\screenshot_19.png)

## Шаг 14 
> Настроить систему так, чтобы монтирование происходило автоматически при запуске системы. Произвести монтирование новых файловых систем.

Узнаем UUID новых дисков:
```
$ sudo blkid /dev/mapper/vg*
```

![](C:\epam\Images\screenshot_20.png)

Добавим изменения в */etc/fstab*:
```
UUID=db87737a-cf67-453a-bdbd-3c297b6d4399 /opt/mount1             ext4    defaults        0 0  UUID=6b58b7d2-03da-4ebf-8ea9-894fca933aac /opt/mount2             ext4    defaults        0 0
```
Смонтируем все диски из */etc/fstab*:
```
$ sudo mount -a
```
Теперь после перезагрузки, указанные разделы монтируются автоматически.

![](C:\epam\Images\screenshot_21.png)

## Для VM1 (шаги 15-16):
## Шаг 15
> После монтирования создать 2 директории для хранения файлов Namenode сервиса HDFS:
• /opt/mount1/namenode-dir
• /opt/mount2/namenode-dir

```
$ sudo mkdir /opt/mount{1,2}/namenode-dir
```

![](C:\epam\Images\screenshot_22.png)

## Шаг 16
> Сделать пользователя hdfs и группу hadoop владельцами этих директорий.

```
$ sudo chown hdfs:hadoop /opt/mount{1,2}/namenode-dir
```
После: 

![](C:\epam\Images\screenshot_23.png)

## Для VM2 (шаги 17-20):
## Шаг 17
> После монтирования создать 2 директории для хранения файлов DataNode сервиса HDFS:
• /opt/mount1/datanode-dir
• /opt/mount2/datanode-dir

```
$ sudo mkdir /opt/mount{1,2}/datanode-dir
```

![](C:\epam\Images\screenshot_24.png)

## Шаг 18
> Сделать пользователя **hdfs** и группу **hadoop** владельцами директорий из п.17.

```
$ sudo chown hdfs:hadoop /opt/mount{1,2}/datanode-dir
```

![](C:\epam\Images\screenshot_25.png)

## Шаг 19
> Создать дополнительные 4 директории для Nodemanager сервиса YARN:
• /opt/mount1/nodemanager-local-dir
• /opt/mount2/nodemanager-local-dir
• /opt/mount1/nodemanager-log-dir
• /opt/mount2/nodemanager-log-dir

```
$ sudo mkdir /opt/mount{1,2}/nodemanager-{local,log}-dir
```

![](C:\epam\Images\screenshot_26.png)

## Шаг 20
> Сделать пользователя **yarn** и группу **hadoop** владельцами директорий из п.19.

```
$ sudo chown yarn:hadoop /opt/mount{1,2}/nodemanager-{local,log}-dir
```

![](C:\epam\Images\screenshot_27.png)

***
## Личная заметка
При установке и настройке VM1 оставила дефолтное имя хоста, но здесь хочу его изменить на *headnode*.
```
$ sudo hostnamectl set-hostname headnode
# sudo reboot
```

![](C:\epam\Images\screenshot_28.png)

***Отсюда и далее хост-имена VM1 - *headnode*, VM2 - *worker*.***
***

## Шаг 21
> Настроить доступ по SSH, используя ключи для пользователя hadoop.

Конфигурация сетевого интерфейса внутренней сети (для связи 2-х ВМ между собой):

![](C:\epam\Images\screenshot_29.png)

Генерация ключей:
```
$ ssh-keygen -P '' -f hadoop
```
В результате появятся 2 файла с приватным и публичным ключами: *hadoop* и *hadoop.pub*.

Переместим их в папку *.ssh* в домашней директории пользователя **hadoop**:
```
$ sudo mkdir /home/hadoop/.ssh
$ sudo mv hadoop /home/hadoop/.ssh/hadoop
$ sudo mv hadoop.pub /home/hadoop/.ssh/hadoop.pub
$ sudo chown hadoop:hadoop /home/hadoop/.ssh
$ sudo chown hadoop:hadoop /home/hadoop/.ssh/hadoop{,.pub}
```

![](C:\epam\Images\screenshot_30.png)

Переместим публичные ключи (hadoop.pub) с одного хоста на другой.

На **VM1** (*headnode*):
```
$ sudo ssh-copy-id -i /home/hadoop/.ssh/hadoop.pub hadoop@10.0.3.2
```
На **VM2** (*worker*):
```
$ sudo ssh-copy-id -i /home/hadoop/.ssh/hadoop.pub hadoop@10.0.3.1
```

***
## Личная заметка 2
Вот здесь я выполнила действия **Шага 22**, чтобы упростить команду доступа по ssh. 
***

Далее создадим файлы *.ssh/config* с настройками подключения по ssh.
**VM1**: */home/hadoop/.ssh/config*:
```
Host worker
        HostName        worker
        User            hadoop
        IdentityFile    /home/hadoop/.ssh/hadoop
```
**VM2**: */home/hadoop/.ssh/config*:
```
Host headnode
        HostName        headnode
        User            hadoop
        IdentityFile    /home/hadoop/.ssh/hadoop
```

Попытка соединения к **VM1 (headnode, 10.0.3.1) с **VM2** (worker, 10.0.3.2):

![](C:\epam\Images\screenshot_31.png)

Попытка соединения к **VM2** (worker, 10.0.3.2) с **VM1** (headnode, 10.0.3.1):

![](C:\epam\Images\screenshot_32.png)

## Шаг 22
> Добавить VM1 и VM2 в /etc/hosts.

Добавить в файл */etc/hosts* следующие строки:
```
10.0.3.1    headnode
10.0.3.2    worker
```

## Шаг 23
> Скачать файлы по ссылкам в /usr/local/hadoop/current/etc/hadoop/{hadoop-env.sh,core-site.xml,hdfs-site.xml,yarn-site.xml}. 

```
$ sudo wget -O /usr/local/hadoop/current/etc/hadoop/hadoop-env.sh  https://gist.githubusercontent.com/rdaadr/2f42f248f02aeda18105805493bb0e9b/raw/6303e424373b3459bcf3720b253c01373666fe7c/hadoop-env.sh
```
```
$ sudo wget -O /usr/local/hadoop/current/etc/hadoop/core-site.xml  https://gist.githubusercontent.com/rdaadr/64b9abd1700e15f04147ea48bc72b3c7/raw/2d416bf137cba81b107508153621ee548e2c877d/core-site.xml
```
```
$ sudo wget -O /usr/local/hadoop/current/etc/hadoop/hdfs-site.xml  https://gist.githubusercontent.com/rdaadr/2bedf24fd2721bad276e416b57d63e38/raw/640ee95adafa31a70869b54767104b826964af48/hdfs-site.xml
```
```
$ sudo wget -O /usr/local/hadoop/current/etc/hadoop/yarn-site.xml  https://gist.githubusercontent.com/Stupnikov-NA/ba87c0072cd51aa85c9ee6334cc99158/raw/bda0f760878d97213196d634be9b53a089e796ea/yarn-site.xml
```

> При помощи sed заменить заглушки на необходимые значения.

*  **hadoop-env.sh**
    > Необходимо определить переменные JAVA_HOME (путь до директории с OpenJDK8, установленную в п.3), HADOOP_HOME (необходимо указать путь к симлинку из п.6) и HADOOP_HEAPSIZE_MAX (укажите значение в 512M)
    
    JAVA_HOME:
    ```
    $ sudo sed -i -r 's:(export JAVA_HOME=)(.*):\1/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre:' /usr/local/hadoop/current/etc/hadoop/hadoop-env.sh
    ```
    
    ![](C:\epam\Images\screenshot_34.png)
    
    HADOOP_HOME:
    ```
    $ sudo sed -i -r 's:(export HADOOP_HOME=)(.*):\1/usr/local/hadoop/current:' /usr/local/hadoop/current/etc/hadoop/hadoop-env.sh 
    ```
    
    ![](C:\epam\Images\screenshot_35.png)
    
    HADOOP_HEAPSIZE_MAX:
    ```
    $ sudo sed -i -r 's:(export HADOOP_HEAPSIZE_MAX=)(.*):\1512:' /usr/local/hadoop/current/etc/hadoop/hadoop-env.sh
    ```
    
    ![](C:\epam\Images\screenshot_36.png)

*  **core-site.xml**
    
    > Необходимо указать имя хоста, на котором будет запущена HDFS Namenode (VM1)
    
    ```
    $ sudo sed -i 's/%HDFS_NAMENODE_HOSTNAME%/headnode/' /usr/local/hadoop/current/etc/hadoop/core-site.xml
    ```
    
    ![](C:\epam\Images\screenshot_37.png)

*  **hdfs-site.xml**
    > Необходимо указать директории namenode-dir, а также datanode-dir, каждый раз через запятую (например, /opt/mount1/namenode-dir,/opt/mount2/namenode-dir)
    
    ```
    $ sudo sed -i 's|%NAMENODE_DIRS%|/opt/mount1/namenode-dir,/opt/mount2/namenode-dir|' /usr/local/hadoop/current/etc/hadoop/hdfs-site.xml
    $ sudo sed -i 's|%DATANODE_DIRS%|/opt/mount1/datanode-dir,/opt/mount2/datanode-dir|' /usr/local/hadoop/current/etc/hadoop/hdfs-site.xml
    ```
    
    ![](C:\epam\Images\screenshot_38.png)

*  **yarn-site.xml**
    
    > Необходимо подставить имя хоста, на котором будет развернут YARN Resource Manager (VM1), а также пути до директорий nodemanager-local-dir и nodemanager-log-dir (если необходимо указать несколько директорий, то необходимо их разделить запятыми
    
    ```
    $ sudo sed -i 's|%YARN_RESOURCE_MANAGER_HOSTNAME%|headnode|' /usr/local/hadoop/current/etc/hadoop/yarn-site.xml
    $ sudo sed -i 's|%NODE_MANAGER_LOCAL_DIR%|/opt/mount1/nodemanager-local-dir,/opt/mount2/nodemanager-local-dir|' /usr/local/hadoop/current/etc/hadoop/yarn-site.xml
    $ sudo sed -i 's|%NODE_MANAGER_LOG_DIR%|/opt/mount1/nodemanager-log-dir,/opt/mount2/nodemanager-log-dir|' /usr/local/hadoop/current/etc/hadoop/yarn-site.xml
    ```
    
    ![](C:\epam\Images\screenshot_39.png)

    
## Шаг 24
> Задать переменную окружения HADOOP_HOME через /etc/profile

Добавить следующую строку в файл */etc/profile*:
```
HADOOP_HOME=/usr/local/hadoop/current
```
Загрузить изменения:
```
$ source /etc/profile
```

![](C:\epam\Images\screenshot_40.png)

## Для VM1 (шаги 25-26):
## Шаг 25
> Произвести форматирование HDFS (от имени пользователя hdfs).
    
   При попытке запустить команду, получаем сообщения об ошибках, связанных с недостаточностью прав. 
   ```
   $ sudo su -l hdfs -c "$HADOOP_HOME/bin/hdfs namenode -format cluster1"
   ```
   
   ![](C:\epam\Images\screenshot_43_failure.png)
   
   Для решения проблемы попробуем предпринять следующие шаги.
   
   Проверим права доступа к проблемной директории *$HADOOP_HOME/logs*:
   
   ![](C:\epam\Images\screenshot_44.png)
   
   Как мы видим, у пользователей группы *hadoop* (к ней как раз относится пользователь *hdfs*) нет прав на запись в директорию. 
   Исправим это:
   ```
   $ sudo chmod 775 /usr/local/hadoop/current/logs
   ```
   
   ![](C:\epam\Images\screenshot_45.png)
   
   Успешно форматируем HDFS:
   
   ![](C:\epam\Images\screenshot_46.png)
   
## Шаг 26
> Запустить демоны сервисов Hadoop

* Запуск **NameNode** (от имени пользователя hdfs):
    ```
    $ sudo su -l hdfs -c "$HADOOP_HOME/bin/hdfs --daemon start namenode"
    ```
    Демон запущен:
    
    ![](C:\epam\Images\screenshot_47.png)
    
* Запуск **ResourceManager** (от имени пользователя yarn):
    ```
    $ sudo su -l yarn -c "$HADOOP_HOME/bin/yarn --daemon start resourcemanager"
    ```
    Демон запущен:
    
    ![](C:\epam\Images\screenshot_48.png)

## Для VM2 (шаг 27):
## Шаг 27
> Запустить демоны сервисов Hadoop.

* Запуск **DataNode** (от имени hdfs):
    Сразу создадим директорию */usr/local/hadoop/current/logs* и добавим права доступа к ней для пользователей группы **hadoop**, чтобы предупредить ошибки запуска, с которыми стоклнулись в предущем пункте:
    ```
    $ sudo mkdir /usr/local/hadoop/current/logs
    $ sudo chown hadoop:1002 /usr/local/hadoop/current/logs
    $ sudo chmod 775 /usr/local/hadoop/current/logs
    ```
    
    ![](C:\epam\Images\screenshot_49.png)
    
    ```
    $ sudo su -l hdfs -c "$HADOOP_HOME/bin/hdfs --daemon start datanode"
    ```

* Запуск **NodeManager** (от имени yarn):
    ```
    $ sudo su -l yarn -c "$HADOOP_HOME/bin/yarn --daemon start nodemanager"
    ```
    
Оба демона успешно запущены: 

![](C:\epam\Images\screenshot_50.png)

## Шаг 28
> Проверить доступность Web-интефейсов HDFS Namenode и YARN Resource Manager по портам 9870 и 8088 соответственно (VM1).

```
$ sudo lsof -Pn -i TCP -s TCP:LISTEN
```

![](C:\epam\Images\screenshot_51.png)

Перебросим трафик с портов 8088 и 9870 на порты 65000 и 65070 соответсвенно на хостовой машине:
```
$ ssh -L 65000:headnode:8088 exam@192.168.56.114
$ ssh -L 65070:headnode:9870 exam@192.168.56.114
```

Веб-интерфейс кластера (порт 8088 на headnode): 

![](C:\epam\Images\screenshot_52.png)

Веб-интерйес NameNode (мастер-нода в кластере, порт 9870 на headnode): 

![](C:\epam\Images\screenshot_53.png)

## Шаг 29
> Настроить управление запуском каждого компонента Hadoop при помощи systemd (используя юниты-сервисы).

* **VM1** (headnode):
    
    Юнит для запуска **NameNode** (*/etc/systemd/system/namenode.service*):
    ```
    [Unit]
    Description=NameNode daemon
    
    [Service]
    User=hdfs
    Group=hadoop
    ExecStart=/usr/local/hadoop/current/bin/hdfs --daemon start namenode
    ExecStop=/usr/local/hadoop/current/bin/hdfs --daemon stop namenode
    RemainAfterExit=yes
    Restart=on-failure
    ```
    Юнит для запуска **ResourceManager** (*/etc/systemd/system/resourcemanager.service*):
    ```
    [Unit]
    Description=ResourceManager daemon
    
    [Service]
    User=yarn
    Group=hadoop
    ExecStart=/usr/local/hadoop/current/bin/yarn --daemon start resourcemanager
    ExecStop=/usr/local/hadoop/current/bin/yarn --daemon stop resourcemanager
    RemainAfterExit=yes
    Restart=on-failure
    ```
    
    Запуск служб:
    ```
    $ sudo systemctl enable namenode
    $ sudo systemctl enable resourcemanager
    ```
    ```
    $ sudo systemctl start namenode
    $ sudo systemctl start resourcemanager
    ```
    
    ![](C:\epam\Images\screenshot_54.png)
    
    ![](C:\epam\Images\screenshot_55.png)
    
    ![](C:\epam\Images\screenshot_56.png)
    
* **VM2** (worker):
    
    Юнит для запуска **DataNode** (*/etc/systemd/system/datanode.service*):
    ```
    [Unit]
    Description=DataNode daemon
    
    [Service]
    User=hdfs
    Group=hadoop
    Type=forking
    ExecStart=/usr/local/hadoop/current/bin/hdfs --daemon start datanode
    ExecStop=/usr/local/hadoop/current/bin/hdfs --daemon stop datanode
    Restart=on-failure
    ```
    Юнит для запуска **NodeManager** (*/etc/systemd/system/nodemanager.service*):
    ```
    [Unit]
    Description=NodeManager daemon
    
    [Service]
    User=yarn
    Group=hadoop
    Type=forking
    ExecStart=/usr/local/hadoop/current/bin/yarn --daemon start nodemanager
    ExecStop=/usr/local/hadoop/current/bin/yarn --daemon stop nodemanager
    Restart=on-failure
    ```
    
    Запуск служб:
    ```
    $ sudo systemctl enable datanode
    $ sudo systemctl enable nodemanager
    ```
    ```
    $ sudo systemctl start datanode
    $ sudo systemctl start nodemanager
    ```
    
    ![](C:\epam\Images\screenshot_57.png)
    
    ![](C:\epam\Images\screenshot_58.png)
















