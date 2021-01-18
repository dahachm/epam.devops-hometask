# Hometask 3

[access.log](/3/access.log)

## AWK

* What is the most frequent browser (user agent) in given access.log?

Let's make a small scriptfile:

scriptfile:
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

![Пример работы скрипта](/3/screenshots/taskAWK_1.png)


* Show number of requests per month for ip 193.106.31.130 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)

scriptfile2:
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

![Пример работы скрипта](/3/screenshots/taskAWK_2.png)


* Show total amount of data which server has provided for each unique ip (i.e. 100500 bytes for 1.2.3.4; 9001 bytes for 5.4.3.2 and so on)

  scriptfile3:
  ```c
  {
    # $1  - remote IP
    # $10 - amount of data (in bytes) that server has sent to remote IP
    
    data[$1]=data[$1]+$10
  }
  
  END {
    for (i in data) {
      printf "%d bytes for %s\n", data[i], i;
    }
  }
  ```
  
  ![Пример работы скрипта](/3/screenshots/taskAWK_3.png)
  
  [Here is OUTPUT file](/3/awk_3_OUTPUT)



