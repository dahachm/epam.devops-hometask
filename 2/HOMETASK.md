# Hometask 2

[access.log](/2/access.log)

## AWK

* What is the most frequent browser (user agent) in given access.log?

  Let's make a small scriptfile:
  ```awk

  #Setting delimiter BEFORE processing any line

  BEGIN {
    FS="\"";
  }
  
  {
    # 'user agent' is $6 if delimiter set as " (double qoute).
    # So here we make a dictionary ('names') of ALL user agents 
    # that can be found in access.log with number of times each 
    # name appears.
    # Every time when meets new name of user agent - put it in 
    # 'names' (as an index) and set its value to 1.
    # Every time when meets name of user agent that is IN 'names' 
    # already - encrease its value by one

    names[$6]++;
  }

  # This will work AFTER all lines been processed.

  END {
    # Checking through number of appearances of each name 
    # in order to find the first with the biggest number

    bgstNumber=0;
    for (i in names) {
      if (names[i] > grstNum) {
        grstNum=names[i];
        grstName=i;
      }
    }

    printf "The most frequently used user agent if \"%s\" (%d times).\n\n";
  }
  ```
  ```sh
  $ awk -f scriptfile access.log
  ```
  
  ![Пример работы скрипта](/2/screenshots/taskAWK_1.png)


* Show number of requests per month for ip 193.106.31.130 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)

  [scriptfile2](/2/scriptfile2):
  
  ```awk
  {
    # Checking if processed line contains "193.106.31.130".
    # If true: encrease number of requests in substracted date 
    # ('MMM/YYYY', e.g. 'Sep/2016') by one.
    # With default delimiter (space) $4 in each lina has this
    # pattern: '[DD/MMM/YYYY:hh:mm:ss +0100]', where DD - day number,
    # MMM - month name in 3 letters (Sep, Oct, Dec, etc.), 
    # YYYY - year number, hh:mm:ss - time.

    if ($0 ~ /193.106.31.130/) {
     times[substr($4,5,8)]++;
    }
  }
  END {
    for (i in times) {
      printf "%s %s - %d reqs\n", substr(i, 1, 3), substr(i,5,4), times[i];
    }
    printf "\n";
  }
  ```
   ```sh
  $ awk -f scriptfile2 access.log
  ```
  
  ![Пример работы скрипта](/2/screenshots/taskAWK_2.png)


* Show total amount of data which server has provided for each unique ip (i.e. 100500 bytes for 1.2.3.4; 9001 bytes for 5.4.3.2 and so on)

  [scriptfile3:](/2/scriptfile3)
  
  ```c
  {
    # $1  - remote IP
    # $10 - amount of data (in bytes) that server has sent to remote IP
    if ($1 != "") {
        data[$1]=data[$1]+$10
    }
  }
  
  END {
    for (i in data) {
      printf "%-10d bytes for %s\n", data[i], i;
    }
  }
  ```
  
    ```sh
  $ awk -f scriptfile3 access.log
  ```
  
  ![Пример работы скрипта](/2/screenshots/taskAWK_3.png)
   
  [Here is OUTPUT file](/2/AWK_task3_OUTPUT)
 
 
 ## SED 
 
  * Change all user agents to "lynx"
    
    ```sh
    $ sed {s/\"[^\"]*\"/\"lynx\"/3} access.log
    ```
    
    ![Пример работы команды](/2/screenshots/taskSED_1.png)
    
    [Here is OUTPUT file](/2/SED_task1_OUTPUT)
  
  * Masquerade all ip addresses. For example, 1.2.3.4 becomes "ip1", 3.4.5.6 becomse "ip2" and so on. Rewrite file.
  
    As we have to proccess file line by line,  we can not use *-i* mode in *sed* command line to substitute each IP address with "ipN". At the same time we can not write to the file while it's beeing read.
  
    So in this case we use extra file *output* to write results of processed lines from *access.log* and to copy its content in *access.log* after. 
  
    Print time in the begining and in the end here just to show how long does it take to process such big files.  
  sed_task2:
    ```sh 
    #!/bin/bash
   
    echo start at $(date +"%T")

    N=1
    while read line; do
      echo $line | sed "s/^\([0-9]*\.\)\{3\}[0-9]*/ip$((N))/g"
      N=$((N+1));
    done < $1 > output
    cp output access.log && rm output
    
    echo finish at $(date +"%T")
    ```
    ```sh
    $ ./sed_task2 access.log 
    ```
       
    ![Пример работы команды](/2/screenshots/taskSED_2.png)
    
    [Here is OUTPUT file (new access.log)](/SED_task2_OUTPUT)
  
  ## Extra task
  
  Show list of unique ips, who made more then 50 requests to the same url within 10 minutes (for example too many requests to "/").
  
  This one completed using **AWK.**
  
  If we need just a list of unique IP addresses without specifying time and other details of request:

  ```sh
  $ cat access.log | awk '{print substr($4,2,16) " " $1 " " $7}' | sort | uniq -c | awk '{ if ($1 > 50) {print $3}}' | sort | uniq
  ```
  
  ![Пример работы команды](/2/screenshots/task_EXTRA_1.png)
   
   [Here is List of unique IP](/2/task_EXTRA_OUTPUT_1)
  
  
  This script makes a formatted list of IP addresses, that made more then 50 requests to the same url within 10 minutes, specifies details of requests (url, date and time range, and number of requests during this time range) and write it to *output_* file. It also shows the list of unique IP addresses from the list that was made.
  [script](/2/script):
  ```sh
  #!/bin/bash

    makeList () {
      printf "    %s    \t     %s     \t%s\t     %s     \t          %s\n" "DATE" "TIME" "REQ" "IP" "URL"

      cat $1 | awk '{printf "%s %s %s\n", substr($4,2,16), $1, $7}'| sort | uniq -c | awk '{if ($1 > 50) {printf "%s %s %d %s %s\n", substr($2,1,11), substr($2,13,4), $1, $3, $4}}' > temp

      while read line; do
        echo $line | awk '{printf "%s\t%02d:%02d - %02d:%02d\t%d\t%s\t%s\n", $1, substr($2,1,2), substr($2,4,1)*10, substr($2,4,1) < 5 ? substr($2,1,2) : (substr($2,1,2) < 23 ? substr($2,1,2)+1 : 0), substr($2,4,1) < 5 ? (substr($2,4,1)+1)*10 :0, $3, $4, $5}';
      done < temp

      rm temp
    }

    makeList $1 > output_
    cat output_ | awk '{if (NR !=1) {print $6}}' | sort | uniq 
  ```
  
  ```sh
  $ ./script access.log
  ```
  ![Пример работы команды](/2/screenshots/task_EXTRA_2.png)
  
  [Here is Formatted list (*output_*)](/2/task_EXTRA_OUTPUT_2)
  
    
     
  
  
 
  
  
