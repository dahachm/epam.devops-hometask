# Hometask 10

# Boot process

## 1. Find a utility to inspect *initrd* file contents. Find all files that are related to XFS filesystem and give a short description for every file.
  
  **initramfs** (or **initrd** in earlier versions) - initial ramdisk image - is used as the first root filesystem that machine has access to and carries the modules needed for kernel to mount root filesystem and maybe some other drivers that can be needed for correct/customized system start, but can't be embedded to kernel (due to some reasons). The best thing about **initramfs** (or **initrd**) is that it can be rearranged by (competent) user for specific system features. 
  
  **initramfs** is located in **/boot** directory:
  
  ![](/10/screenshots/task1_1.png)
  
  There are few **initramfs** files for different kernel versions, as you can see.
  
  For now **3.10.0-1160.15.2.el7.x86_64** version is used:
  
  ![](/10/screenshots/task1_2.png)
  
  So let's inspect suited **initramfs**.
  
  ![](/10/screenshots/task1_3.png)
  
  To inspect its content there is **lsinitrd** utility:
  
  ```
  # lsinird /boot/initramfs-3.10.0-1160.15.2.el7.x86_64.img
  ```
  
  ![](/10/screenshots/task1_4.png)
  
  All the files related to XFS filesystem can be found with folllowing command:
  
  ```
  # lsinitrd /boot/initramfs-3.10.0-1160.15.2.el7.x86_64.img | grep xfs
  ```
  
  I got following output:
  
  ```
  drwxr-xr-x   2 root     root            0 Feb  7 09:11 usr/lib/modules/3.10.0-1160.15.2.el7.x86_64/kernel/fs/xfs
  -rw-r--r--   1 root     root       335980 Feb  3 10:18 usr/lib/modules/3.10.0-1160.15.2.el7.x86_64/kernel/fs/xfs/xfs.ko.xz
  -rwxr-xr-x   1 root     root          433 Sep 30 13:51 usr/sbin/fsck.xfs
  -rwxr-xr-x   1 root     root       590208 Feb  7 09:11 usr/sbin/xfs_db
  -rwxr-xr-x   1 root     root          747 Sep 30 13:51 usr/sbin/xfs_metadump
  -rwxr-xr-x   1 root     root       576720 Feb  7 09:11 usr/sbin/xfs_repair
  ```
  
  **usr/lib/modules/3.10.0-1160.15.2.el7.x86_64/kernel/fs/xfs** - XFS kernel module
  
  **usr/lib/modules/3.10.0-1160.15.2.el7.x86_64/kernel/fs/xfs/xfs.ko.xz** - compressed XFS kernel module
  
  **usr/sbin/fsck.xfs** - is used to check and optionally repair XFS filesystem
  
  **usr/sbin/xfs_db** - is used to examine an XFS filesystem
  
  **usr/sbin/xfs_metadump** - is a debugging tool that copies the metadata from an XFS filesystem to a file.
  
  **usr/sbin/xfs_repair** - repairs corrupt or damaged XFS filesystems
  

## 2. Explain the difference between ordinary and rescue initrd images.
  
  When some kernel modules or initramfs files are corrupted or missing, the system can't boot correctly.
  
  For that case there is a **rescue initrd** image that containt all the drivers and kernel modules (usually for the previous stable kernel version) so the system can be
  booted using this image and admin can check what happened to the needed initial ram disk.
  
  So the rescue version of initramfs(initrd) is usually much bigger and generared automatically each time kernel is updated.
  
  ![](/10/screenshots/task1_5.png)
  
  Grub2 menu to choose OS kernel to boot:
  
  ![](/10/screenshots/task1_6.png)
  
## 3. Study dracut utility that is used for rebuilding initrd image. Give an example for adding driver/kernel module for your initrd and recreating it.
  
  
  Some modules can be added to initrd image by:
  
   * adding them to dracut configuration files */etc/dracut.conf.d/*.conf*
   * using -a or --add parameters with *dracut* command utility

  For axample, to list available modules use command:
  
  ```
  # dracut --list-modules
  ```
  
  ![](/10/screenshots/task1_13.png)
  
  There is no module **crypt** in **initramfs-3.10.0-1160.15.2.el7.x86_64.img** so let's try to add it by using dracut:
  
  ```
  # 
  ```
  
  ![Результат](/10/screenshots/task1_14.png)
  
  ![](/10/screenshots/task1_15.png)
    

## 4.	Enable recovery options for grub, update main configuration file and find new item in GRUB2 config in /boot.
  
  Open grub settings file and set GRUB_DISABLE_RECOVERY to 'false':
  ```
  # vim /etc/default/grub
  ```
  
  ```
  GRUB_DISABLE_RECOVERY="false"
  ```
  
  ![](/10/screenshots/task1_7.png)
  
  Then update grun configuration:
  ```
  # grub2-mkconfig -o /boot/grub2/grub.cfg
  ```
  
  ![](/10/screenshots/task1_9.png)
  
  In **/boot/grub2/grub.cfg** file new *menuentry* options were found:
  
  ![](/10/screenshots/task1_12.png)
  
  When booting the system now grub2 menu looks like this:
  
  ![](/10/screenshots/task1_11.png)
  
  If your system fails to boot for whatever reason, it may be useful to boot it into recovery mode. This mode just loads some basic services and drops you into command line mode. You are then logged in as root (the superuser) and can repair your system using command line tools. 
  
  (Src: [https://wiki.ubuntu.com/RecoveryMode](https://wiki.ubuntu.com/RecoveryMode))

## 5.	Modify option vm.dirty_ratio:
  * a.	using sysctl utility
  * b.	using sysctl configuration file

  **vm.dirty_ratio** is the absolute maximum amount of system memory that can be filled with *dirty pages* (memory pages that still need to be written to disk) before everything must get committed to disk. When the system gets to this point all new I/O blocks until dirty pages have been written to disk. This is often the source of long I/O pauses, but is a safeguard against too much data being cached unsafely in memory.
  
  (Src. [https://lonesysadmin.net/2013/12/22/better-linux-disk-caching-performance-vm-dirty_ratio/](https://lonesysadmin.net/2013/12/22/better-linux-disk-caching-performance-vm-dirty_ratio/))
  
  Check the current value of vm.dirty_ratio:
  
  ```
  # sysctl -a | grep vm.dirty_ratio
  ```
  
  ![](/10/screenshots/task1_16.png)
  
  **Set vm.dirty_ratio using *systcl utility*** to *40*:
  
  ```
  # sysctl -w vm.dirty_ratio="40"
  ```
  
  The result:
  
  ![](/10/screenshots/task1_17.png)
  
  **Set vm.dirty_ratio using *systcl configuration file*** back to *30*:
  
  ```
  # vi /etc/sysctl.conf
  ```
  
  Add following line:
  
  ```
  vm.dirty_ratio=30
  ```
  
  Then reload settings (from /etc/sysctl.conf by default):
  
  ```
  # sysctl --load
  ```
  
  The result:
  
  ![](/10/screenshots/task1_18.png)  

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
