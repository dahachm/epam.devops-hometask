# Hometask 4

## Task 1. Processes
  - Run **sleep** command 3 times at different intervals and send a **SIGSTOP** signal to all of them in 3 different ways.
  
    To run any proccess in background you need to put & sign in the end of the command line like this:
    
    ```
    $ sleep 1000 &
    ```
    
    **SIGSTOP** signal can be sent by:
      
     * using **Ctrl+Z** key combination on running in foreground;
      
     * using **kill** command with **-s** parameter and signal name after it (**sigstop** or **stop** for **SIGSTOP**, it's not case sensative) and PID or Job ID;
      
     * using **kill** comand with **-n** parameter and signal number (**19** for **SIGSTOP**) and PID or Job ID.
      
    ```
    $ kill -s sigstop 1525
    $ kill -n sigstop 1526
    ```
      
    ![Результат работы команды](/4/screenshots/task1_1.png)
    
    All the signal's names and numbers can be listed using **kill -l**:
    
    ```
    $ kill -l
    ```
    
  - Check their status with a **job** command.
    
    ```
    $ jobs
    ```
    
    ![Результат работы команды](/4/screenshots/task1_2.png)
    
    Job that was last sent to bascground is marked with '+'. Job that was second last sent to background is marked with '-'.
      
  - **Terminate** any of the processes.
    
    Proccess/Job that is stopped can be terminated by using **kill PID** ot **kill %jn** (where **jn** is a jon ID), but you have to "continue" after so it won't be listed in the list of waiting processes (with **T** status).
    
    ```
    $ kill %1
    $ fg %1
    ```
    
    ![Результат работы команды](/4/screenshots/task1_3.png)
    
  - Send a **SIGCONT** in two different ways

    **SIGCONT** signal can be sent by:
      
     * using **fg %jn** (where **jn** is a jon ID) and it continue to run in the same terminal;
      
     * using **kill** command with **-s** parameter and signal name after it (**sigcont** or **cont** for **SIGCONT**, it's not case sensative) and PID or Job ID;
      
     * using **kill** comand with **-n** parameter and signal number (**18** for **SIGCONT**) and PID or Job ID.
      
     ```
     $ fg %1
     $ kill -s sigcont %1
     $ kill -n 18 %1
     ```
      
     ![Результат работы команды](/4/screenshots/task1_4.png)
      
   - Kill one by PID and the second one by job ID.
     
     ```
     $ kill 1526
     $ kill %3
     ```
     
     ![Результат работы команды](/4/screenshots/task1_5.png)
 
 ***
 
## Task 2. systemd

     

***

## task 3. cron/anacron
   - Create an anacron job which executes a script with *echo Hello > /opt/hello* and runs every 2 days.
     
     Make [sciprt file](/4/script) and save it in **/root/** (so its full path is **/root/script**):
     
      ```
      #!/bin/bash
      echo Hello > /opt/hello
      ```
     
     Add new job in **/etc/anacrontab**:
     
      ![Содержимое файла abacrontab](/4/screenshots/task3_1.png)
     
     To be able to test if it works as we expect immediately I also set the value of RANDOM_DELAY=0.
     
     Run anacron with parameneter **-f** to force execution of all jobs ignoring timestamps.
     
      ```
      # anacron -f
      ```
     
     As the result, we will be able to see that **/opt/hello** file is not empty anymore. To be sure that this task was completed by anacron job we can check **/var/log/cron** file to check its logs:
     
      ```
      # cat /opt/hello
      #
      # tail /var/log/cron 
      ```
      
      ![Результат работы команды](/4/screenshots/task3_2.png)
     
   - Create a cron job which executes the same command and runs it in 1 minute after system boot.
     
     To add new cron job use next command:
      
      ```
      # crontab -e
      ```
      
     And in opened file we add next line:
     
      ```
      @reboot sleep 60 && /root/script
      ```
      
     This means that just after system start it will wait for 60 seconds and than execute **/root/script**.
     
     Before rebooting, check that there is no **/opt/hello** file yet and print current time for the record.
     
      ![Результат работы команды](/4/screenshots/task3_3.png)
     
     After system restart, check **/var/log/cron/** to be sure that cron job has started. And after 1 minute check **/opt/hello** file.
     
      ![Результат работы команды](/4/screenshots/task3_4.png)

***

## Task 4. lsof
   - Run a **sleep** command, redirect *stdout* and *stderr* into two different files (both of them will be empty).
      
      ```
      # sleep 1000 1> output.log 2> error.log &
      ```
      
      ![Результат работы команды](/4/screenshots/task4_1.png)
      
     To find out wich files this process uses will run **lsof** with **-c** parameter:
     
      ```
      # lsof -c sleep
      ```
      
      ![Результат работы команды](/4/screenshots/task4_2.png)
      
     In the end of the given list we can see that out process use to files for *writing* (**output.log** and **error.log**) and one for *reading and writing* (**/dev/pts/0**).
     As this is the only file that is marked as used for reading, can assume that *it is where the process gets stdout from*. To check if it's really our terminal (the one in wich the process was started) will try to **echo** smth in **/dev/pts/0**:
      
      ![Результат работы команды](/4/screenshots/task4_3.png)
      
   - List all ESTABLISHED TCP connections ONLY with lsof.
   
     To list all the network files use **lsof** with **-i** parameter and args that specify IP vers (4 or 6), protocol name (TCP or UDP), hostname and hostaddr, service and port. To spesify protocol state **-s P:S** parameter is used with **P** as protocol name (TCP or UDP) and **S** as protocol state (ESTABLISHED in our case).
     
      ```
      # lsof -i TCP -s TCP:ESTABLISHED
      ```
      
      ![Результат работы команды](/4/screenshots/task4_5.png)
