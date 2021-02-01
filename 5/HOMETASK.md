# Hometask 5

  **remotehost** - 40.68.74.188 (public IP)
  **webserver** - 10.0.0.5 (private IP)


## Task 1

### 1.1
  - SSH to **remotehost**(40.68.74.188) using username and password provided to you in Slack. Log out from **remotehost**.
    
    To log in:
    
    ```
    $ ssh Darya_Chemyakina@40.68.74.188
    ```
    
    To log out: 
    
    ```
    $ exit
    ```
    
    ![Example output](/5/screenshots/task1_1.png)
    
### 1.2
  - Generate new SSH key-pair on your **localhost** with name "hw-5" (keys should be created in ~/.ssh folder).
  
    ```
    $ ssh-keygen 
    ```
    
    ![Example output](/5/screenshots/task1_2.png)
    
### 1.3
  - Set up key-based authentication, so that you can SSH to remotehost without password.
    
    **ssh-copy-id** can be used:
    
    on localhost:
    
    ```
    $ ssh-copy-id -i ~/.ssh/hw-5.pub Darya_Chemyakina@40.68.74.188
    ```
    
    Also access privileges of **~/.ssh** must be set to *700*, of **~/.ssh/authorized_keys** must be set to *644*.
    
    on remotehost:
    
    ```
    $ chmod 700 ~/.ssh && chmod 644 ~/.ssh/authorized_keys
    ```
    
    ![Example output](/5/screenshots/task1_3.png)
    
    Or *Public Key* can be added manually to **remotehost** in file */home/$USER/.ssh/authorized_keys*. 
    
    Copy Public Key from ~/.ssh/hw-5.pub:
    
    ```
    $ cat ~/.ssh/hw-5.pub
    ```
    
    Paste copied Key at the end of **~/.ssh/autorized_keys** on **remotehost**. If there are no **.ssh** directory or **autorized_keys** file they need to be created with only-user-has-access privileges. 
    
    ```
    $ vi ~/.ssh/authorized_keys || mkdir ~/.ssh && vi ~/.ssh/authorized_keys
    ```
    
    ```
    $ chmod 700 ~/.ssh && chmod 644 ~/.ssh/authorized_keys
    ```
    
    ![Example output](/5/screenshots/task1_4.png)
    
### 1.4
  - SSH to **remotehost** without password. Log out from **remotehost**.
  
    To log in again without password we need to use **-i** parameter that points to demanded Private Key:
    
    ```
    $ ssh -i ~/.ssh/hw-5 Darya_Chemyakina@40.68.74.188
    $
    $ exit
    ```
    
    ![Example output](/5/screenshots/task1_5.png)
    
### 1.5
  - Create SSH config file, so that you can SSH to **remotehost** simply running *ssh remotehost* command. As a result, provide output of command *cat ~/.ssh/config*.
  
    We need to put followinf context in **~/.ssh/config**:
    
    ```
    Host remotehost
      HostName 40.68.74.188
      User Darya_Chemyakina
      IdentityFile /home/admin/.ssh/hw-5
    ``` 
    
    And change its privileges to only-user-has-access:
    
    ```
    $ chmod 600 ~/.ssh/config
    ```
    
    ```
    $ ssh remotehost
    ```
    
    ![Example output](/5/screenshots/task1_6.png)
    
    Output of command *cat ~/.ssh/config*:
    
    ![Example output](/5/screenshots/task1_7.png)
    
### 1.6
  - Using command line utility (curl or telnet) verify that there are some webserver running on port 80 of **webserver**.  Notice that webserver has a private network IP, so you can access it only from the same network (when you are on **remotehost** that runs in the same private network). Log out from **remotehost**.
    
    ```
    $ ssh remotehost
    $ curl http://10.0.0.5:80
    ```

    ![Example output](/5/screenshots/task1_8.png)
  
### 1.7
  - Using SSH setup port forwarding, so that you can reach **webserver** from your **localhost** (choose any free local port you like).
  
    ```
    $ ssh -L 62000:10.0.0.5:80 remotehost
    ```
    
    And to list listening ports on localhost:
    
    on **localhost**:
    ```
    $ ss -lnt
    ```
    
    -l - show only listening sockets
    -n - show port numbers not names of services
    -t - show TCP sockets
    
    ![Example output](/5/screenshots/task1_9.png)
    

### 1.8
  - Like in ***1.6***, but on localhost using command line utility verify that **localhost** and port you have specified act like **webserver**, returning same result as in ***1.6***.
    
    on **localhost**:
    ```
    $ curl localhost:62000
    ```
    
    Got the same answer as in **1.6**:
    
    ![Example output](/5/screenshots/task1_10.png)

### 1.9
  - Open **webserver** webpage in browser of your Host machine of VirtualBox (Windows, or Mac, or whatever else you use). You may need to setup port forwarding in settings of VirtualBox.

***

## Task 2

### 2.1
  - Change the time zone on the localhost to Havana and verify the time zone has been changed properly (may be multiple commands).
  
    ```
    # timedatectl set-timezone 'America/Havana'
    # date
    ```
    
    ![Example output](/5/screenshots/task2_1.png)
    
    To proof that timezone was changed properly check local time in Havana usiny **tzselect** utility:
    
    ```
    # tzselect
    ```
    
    Then choose *2) America* and then *16) Cuba* and compare given time with the one wich was set:
    
    ![Example output](/5/screenshots/task2_2.png)
    
### 2.2
  - Find all systemd journal messages on localhost, that were recorded in the last 50 minutes and originate from a system service started with user id 81 (single command).
    
    ```
    # journalctl -S -50min --system _UID=81 
    ```
    
    ![Example output](/5/screenshots/task2_3.png)
    
    To see information with fileds listed (and check wich UID these records have):
    
    ```
    # journalctl -S -50min --system _UID=81 -o verbose
    ```
    
    ![Example output](/5/screenshots/task2_4.png)
    
### 2.3
  - Configure **rsyslogd** by adding a rule to the newly created configuration file */etc/rsyslog.d/auth-errors.conf* to log all **security and authentication messages** with the priority **alert and higher** to the */var/log/auth-errors* file. Test the newly added log directive with the logger command (multiple commands).
    
    Create */etc/rsyslog.d/auth-errors.conf* with following context:
    
    ```
    authpriv.alert /var/log/auth-errors
    ```
    
    Then restart rsyslogd and check if it started witn no errors:
    
    ```
    # systemctl restart rsyslog
    # systemctl status rsyslog
    ```
    
    ![Example output](/5/screenshots/task2_5.png)
    
    Let's test newly if it works:
    
    ```
    # logger -p authpriv.alert "This is alert message"
    # logger -p authpriv.emerg "This is emerg message"
    # logger -p alert "This message must be absent in log file"
    # logger -p authpriv.err "This one also must be absent"
    # cat /var/log/auth-errors
    ```
    
    ![Example output](/5/screenshots/task2_6.png)
    
