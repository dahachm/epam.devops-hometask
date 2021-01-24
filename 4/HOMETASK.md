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
   -

***

## task 3. cron/Anacron
   - 

***

## Task 4. lsof
   - 
