# Hometask 9

## Task 1
  #### Create new disk in Virtual Box (5 GB) and attach it to virtual machine. Add some swap space.
  
  
  Creation of new disk in VB:
   
   ![](/9/screenshots/task1_1.png)
   
   ![](/9/screenshots/task1_2.png)
   
   ![](/9/screenshots/task1_3.png)
   
   ![](/9/screenshots/task1_4.png)
   
   ![](/9/screenshots/task1_5.png)
   
   ![](/9/screenshots/task1_6.png)
   
   ![](/9/screenshots/task1_8.png)
  
  **/dev/sdb** - 5GB disk, that just attached to the VM
  
  ![](/9/screenshots/task1_9.png)

***

### 1.1. Create a 2GB GPT partition on /dev/sdb of type "Linux filesystem" (means all the following partitions created in the following steps on /dev/sdb will be GPT as well)
  
  ```
  # gdisk /dev/sdb
  ```
  
  ```
  GPT fdisk (gdisk) version 0.8.10

  Partition table scan:
    MBR: not present
    BSD: not present
    APM: not present
    GPT: not present

  Creating new GPT entries.

  Command (? for help): n
  Partition number (1-128, default 1): 1
  First sector (34-10485726, default = 2048) or {+-}size{KMGTP}: [Enter = 'set default']
  Last sector (2048-10485726, default = 10485726) or {+-}size{KMGTP}: +2G
  Current type is 'Linux filesystem'
  Hex code or GUID (L to show codes, Enter = 8300): [Enter]
  Changed type of partition to 'Linux filesystem'
  ```
  
  The result: 
  
  ![Sample output](/9/screenshots/task1_10.png)
  
### 1.2. Create a 512MB partition on /dev/sdb of type "Linux swap"
  
  In the same session in *gdisk*:
  ```
  Command (? for help): n
  Partition number (2-128, default 2): 2
  First sector (34-10485726, default = 4196352) or {+-}size{KMGTP}:
  Last sector (4196352-10485726, default = 10485726) or {+-}size{KMGTP}: +512M
  Current type is 'Linux filesystem'
  Hex code or GUID (L to show codes, Enter = 8300): 8200
  Changed type of partition to 'Linux swap'
  ```
  
  The result:
  
  ![Sample output](/9/screenshots/task1_11.png)
  
  List of available Hex codes:
  
  ![Sample output](/9/screenshots/task1_12.png)
  
  To verify disk:
  
  ```
  Command (? for help): v

  No problems found. 5242813 free sectors (2.5 GiB) available in 2
  segments, the largest of which is 5240799 (2.5 GiB) in size.
  ```
  
  To write table to disk and exit: 
  
  ```
  Command (? for help): w

  Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
  PARTITIONS!!

  Do you want to proceed? (Y/N): Y
  OK; writing new GUID partition table (GPT) to /dev/sdb.
  The operation has completed successfully.
  ```
  
  The result:
  
  ```
  # fdisk -l
  ```
  
  ![Sample output](/9/screenshots/task1_13.png)

### 1.3. Format the 2GB partition with an XFS file system
   
   ```
   # mkfs -t xfs /dev/sdb1
   ```
   
   To check if file system is set:
   
   ```
   # parted -l
   ```
   
   Will see smth like this:
   
   ![Sample output](/9/screenshots/task1_14.png)

### 1.4. Initialize 512MB partition as swap space
  
  ```
  # mkswap /dev/sdb2
  ```
  
  The result:
  
  ```
  # parted -l
  ```
  
   ![Sample output](/9/screenshots/task1_15.png)

### 1.5. Configure the newly created XFS file system to persistently mount at /backup
  
  To file */etc/fstab*:
  
  ```
  vi /etc/fstab
  ```
  
  add following line:
  
  ```
  /dev/sdb1       /backup                         xfs     defaults        0 0
  ```
  
  Then create a */backup* directory:
  
  ```
  # mkdir /backup
  ```
  
  and remount all the devices from */etc/fstab*:
  
  ```
  # mount -a
  ```
  
  The result:
  
  ```
  df -h
  ```
  
  ![Sample output](/9/screenshots/task1_16.png)  

### 1.6. Configure the newly created swap space to be enabled at boot
  
  Add following line to */etc/fstab*:
  
  ```
  /dev/sdb2       swap                         swap     defaults        0 0
  ```
  
  Enable all the 'swap' devices (that are not available yet) from */etc/fstab*:
  
  ```
  # swapon -a
  ```
  
  The result:
  
  ```
  # swapon --show
  ```
  
  ![Sample output](/9/screenshots/task1_17.png)

### 1.7. Reboot your host and verify that /dev/sdb1 is mounted at /backup and that your swap partition  (/dev/sdb2) is enabled
  
  ```
  # reboot
  ```
  
  ```
  # df -h
  # swapon --show
  ```
  
  ![Sample output](/9/screenshots/task1_18.png)
  
***  

## Task 2. LVM. 
  
  #### Extend size of root device.

***

### 2.1. Create 2GB partition on /dev/sdb of type "Linux LVM"
  
  ```
  # gdisk /dev/sdb
  ```
  
  ```
  GPT fdisk (gdisk) version 0.8.10

  Partition table scan:
    MBR: protective
    BSD: not present
    APM: not present
    GPT: present

  Found valid GPT with protective MBR; using GPT.

  Command (? for help): n
  Partition number (3-128, default 3): 3
  First sector (34-10485726, default = 5244928) or {+-}size{KMGTP}:
  Last sector (5244928-10485726, default = 10485726) or {+-}size{KMGTP}: +2G
  Current type is 'Linux filesystem'
  Hex code or GUID (L to show codes, Enter = 8300): 8e00
  Changed type of partition to 'Linux LVM'
  ```
  
  ![Sample output](/9/screenshots/task1_19.png)
  
  In the same *gdisk*- session:
  
  ```
  Command (? for help): v

  No problems found. 1048509 free sectors (512.0 MiB) available in 2
  segments, the largest of which is 1046495 (511.0 MiB) in size.

  Command (? for help): w

  Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
  PARTITIONS!!

  Do you want to proceed? (Y/N): Y
  OK; writing new GUID partition table (GPT) to /dev/sdb.
  Warning: The kernel is still using the old partition table.
  The new table will be used at the next reboot.
  The operation has completed successfully.
  ```
  
  The result:
  
  ```
  # parted -l
  ```
  
  ![Sample output](/9/screenshots/task2_1.png)
  
  
### 2.2. Initialize the partition as a physical volume (PV)
  
  Each time I tried to create new PV on /dev/sdb3, I got error message "Device /dev/sdb3 not found.".
  
  So I googled this issue a bit and decided to try **partprobe** - command that is used to inform the OS of partition table changes.
  
  ```
  # partprobe
  # pvcreate /dev/sdb3
  ```
  
  ![Sample output](/9/screenshots/task2_2.png)
  
  ![Sample output](/9/screenshots/task2_3.png)
  
### 2.3. Extend the volume group (VG) of your root device using your newly created PV
  
  Let's check what volume groups I have in my system:
  
  ```
  # vgdisplay
  ```
  
  ![Sample output](/9/screenshots/task2_4.png)
  
  So there is only one volume group named **centos**. 
  
  To extend it with */dev/sdb3*:
  
  ```
  # vgextend centos /dev/sdb3
  ```
  
  ![Sample output](/9/screenshots/task2_5.png)
  
  The result:
  
  ```
  # vgdisplay
  ```
  
  ![Sample output](/9/screenshots/task2_6.png)
  
### 2.4. Extend your root logical volume (LV) by 1GB, leaving other 1GB unassigned
  
  ```
  # lvdisplay
  ```
  
  ![Sample output](/9/screenshots/task2_7.png)
  
  ```
  # lvextend -L +1G /dev/centos/root /dev/sdb3
  ```
  
  ![Sample output](/9/screenshots/task2_8.png)
  
  The result:
  
  ```
  # lvdisplay
  ```
  
  ![Sample output](/9/screenshots/task2_9.png)
  
  ```
  # pvdisplay
  ```
  
  ![Sample output](/9/screenshots/task2_10.png)
  
### 2.5. Check current disk space usage of your root device
  
  ```
  # df -h
  ```
  
  ![Sample output](/9/screenshots/task2_11.png)
  
### 2.6. Extend your root device filesystem to be able to use additional free space of root LV
  
  ```
  # xfs_growfs /dev/mapper/centos-root
  ```
  
  ![Sample output](/9/screenshots/task2_12.png)
  
  The result:
  
  ![Sample output](/9/screenshots/task2_13.png)
  
  
### 2.7. Verify that after reboot your root device is still 1GB bigger than at 2.5.
  
  ![Sample output](/9/screenshots/task2_14.png)
