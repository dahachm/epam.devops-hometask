# Hometask 9

## Task 1
  #### To simulate appearance of new physical disk in server, please create new disk in Virtual Box (5 GB) and attach it to your virtual machine. Add some swap space.
  
  
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
  /dev/sdb2       /boot                         swap     defaults        0 0
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

### 2.1. Create 2GB partition on /dev/sdc of type "Linux LVM"
### 2.2. Initialize the partition as a physical volume (PV)
### 2.3. Extend the volume group (VG) of your root device using your newly created PV
### 2.4. Extend your root logical volume (LV) by 1GB, leaving other 1GB unassigned
### 2.5. Check current disk space usage of your root device
### 2.6. Extend your root device filesystem to be able to use additional free space of root LV
### 2.7. Verify that after reboot your root device is still 1GB bigger than at 2.5.
