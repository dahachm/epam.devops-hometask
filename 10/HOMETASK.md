# Hometask 10

# Boot process

## 1. Find a utility to inspect initrd file contents. Find all files that are related to XFS filesystem and give a short description for every file.
  
  

## 2. Explain the difference between ordinary and rescue initrd images.
  
  
  
## 3. Study dracut utility that is used for rebuilding initrd image. Give an example for adding driver/kernel module for your initrd and recreating it.
  
  

## 4.	Enable recovery options for grub, update main configuration file and find new item in GRUB2 config in /boot.
  
  

## 5.	Modify option vm.dirty_ratio:
  * a.	using sysctl utility
  * b.	using sysctl configuration file

## 6.	Disable selinux using kernel cmdline
  
  

***

# iptables:
## With enabled firewalld:
## 1.	Add rule using firewall-cmd that will allow SSH access to your server *only* from network 192.168.56.0/24 and interface enp0s8.
  
  Interface **enp0s8** belongs to *public* zone:
  
  ```
  # firewall-cmd --get-zone-of-interface=enp0s8
  ```
  
  ![](/10/screenshots/task2_1.png)
  
  *public* also contains other interfaces - enp0s3,enp0s9:
  
  ```
  # firewall-cmd --zone=public --list-all
  ```
  
  ![](/10/screenshots/task2_2.png)
  
  So I want to create new zone for managing traffic trough **enp0s8**.
  
  Create new zone named *test*:
  
  ```
  # firewall-cmd --permanent --new-zone=test
  ```
  
  ![](/10/screenshots/task2_3.png)
  
  Remove **enp0s8** from *public* zone and add it to newly created *test* zone:
  
  ```
  # firewall-cmd --zone=public --remove-interface=enp0s8
  # firewall-cmd --zone=test --add-interface=enp0s8
  ```
  
  ![Результат выполнения команд](/10/screenshots/task2_4.png)
  
  Remove ssh service for other interfaces:
  
  ```
  # firewall-cmd --zone=public --remove-services=ssh
  ```
  
  ![Лист настроек обеих зон](/10/screenshots/task2_5.png)
    
  As we set static IP for **enp0s8** earlier (HT1), there is no need to enable dhcp-client service for it (at least, there is no need in it just in this case).
  
  Add rule to enable ssh only from 192.168.56.0/24 network:
  
  ```
  # firewall-cmd --zone=test --add-rich-rule='rule family="ipv4" source address="192.168.56.0/24" service name="ssh"'
  ```
  
  ![Отображение правила в списке настроек зоны](/10/screenshots/task2_6.png)
  
  Try to get access trough ssh from host machine (IP - 192.168.56.1):
  
  ![](/10/screenshots/task2_7.png)
  
  Remove the rule and try to log in from host machine again:
  
  ```
  # firewall-cmd --remove-rich-rule='rule family="ipv4" source address="192.168.56.0/24" service name="ssh"'
  ```
  
  or just
  
  ```
  # firewall-cmd --reload
  ```
  
  because parameter *-permanent* wasn't used while setting this rule, it will be erased after service restart.
  
  ![](/10/screenshots/task2_8.png)
  
## 2.	Shutdown firewalld and add the same rules via iptables.
  
  Stop firewalld and check its state:
  
  ```
  # systemctl stop firewalld
  # firewall-cmd --state
  ```
  
  ![](/10/screenshots/task2_9.png)
  
  I have 2 ip addresse on **enp0s8** (added the second using **nmcli**, like in HT6): 192.168.56.2 and 10.0.0.1:
  
  ![](/10/screenshots/task2_10.png)
  
  And my host machine IP is 192.168.56.1.
  
  Add rule to enable ssh only from 192.168.56.0/24 network and through **enp0s8**:
  
  ```
  # iptables -A INPUT -p tcp --dport ssh -s 192.168.56.0/24 -i enp0s8 -j ACCEPT
  # iptables -A INPUT -p tcp --dport ssh -j DROP
  ```
  
  List all rules for INPUT:
  
  ```
  # iptables -L INPUT
  ```
  
  ![](/10/screenshots/task2_11.png)
  
  Attempt to login via ssh to 10.0.0.1 (from the same VM OS):
  
  ![](/10/screenshots/task2_12.png)
  
  Attempt to login via ssh to 192.168.56.2 from 192.168.56.1 (host OS):
  
  ![](/10/screenshots/task2_13.png)
