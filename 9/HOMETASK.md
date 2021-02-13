# Hometask 9

## Task 1
  #### To simulate appearance of new physical disk in server, please create new disk in Virtual Box (5 GB) and attach it to your virtual machine.

  #### Mitigate OutOfMemory errors by adding some swap space.

  **/dev/sdc** - 5GB disk, that just attached to the VM

***

### 1.1. Create a 2GB   !!! GPT !!!   partition on /dev/sdc of type "Linux filesystem" (means all the following partitions created in the following steps on /dev/sdc will be GPT as well)

### 1.2. Create a 512MB partition on /dev/sdc of type "Linux swap"

### 1.3. Format the 2GB partition with an XFS file system

### 1.4. Initialize 512MB partition as swap space

### 1.5. Configure the newly created XFS file system to persistently mount at /backup

### 1.6. Configure the newly created swap space to be enabled at boot

### 1.7. Reboot your host and verify that /dev/sdc1 is mounted at /backup and that your swap partition  (/dev/sdc2) is enabled

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
