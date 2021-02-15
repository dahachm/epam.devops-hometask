Boot process:
1.	* Self-study: find a utility to inspect initrd file contents. Find all files that are related to XFS filesystem and give a short description for every file.
2.	* Self-study: explain the difference between ordinary and rescue initrd images.
3.	* Self-study: study dracut utility that is used for rebuilding initrd image. Give an example for adding driver/kernel module for your initrd and recreating it.

4.	Enable recovery options for grub, update main configuration file and find new item in GRUB2 config in /boot.

5.	Modify option vm.dirty_ratio:
a.	using sysctl utility
b.	using sysctl configuration file

6.	Disable selinux using kernel cmdline
