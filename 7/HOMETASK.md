# Hometask 7

## Bash

### Task 1
  - Find a sum of all running process' PIDs.
    
    [task1.sh](/7/task1.sh):
    ```sh
    #!/bin/bash -x
    
    sum=0
    for pif in $(ps -eo pid); do
        sum=$(( $sum + $pid ));
    done
    echo $sum
    ```
    
    ```
    $ chmod +x task1.sh
    $ ./task1.sh |& tee output_1.txt
    ```
    
    [Output sample with debug messages](/7/output_1.txt)
    
    ![Example output](/7/screenshots/task1_1.png)
    
    
### Task 2
  - A lucky number is one whose individual digits add up to 7, in successive additions. For example, 62431 is a lucky number (6 + 2 + 4 + 3 + 1 = 16, 1 + 6 = 7). Find all the lucky numbers between 1000 and 10000.
    
    [task2.sh](/7/task2.sh):
    ```sh
    #!/bin/bash -x
    isLucky() {
        num=$1
        while : ; do
                sum=0
                while [[ $num -ne 0 ]]; do
                        sum=$(( $sum + $(( $num % 10 )) ))
                        num=$(( $num / 10 ));
                done

                if [ $sum -gt 15 ]
                        then num=$sum
                        else break
                fi
        done

        if [[ $sum -eq 7 ]]
                then return 1
                else return 0
        fi
    }

    total=0
    for i in {1000..10000}; do
            isLucky $i
            if [ $? =  1 ]
                    then echo $i; total=$(( total + 1 ))
            fi
    done
    echo "TOTAL: $total lucky numbers"
    ```

    ```
    $ chmod +x task2.sh
    $ ./task1.sh |& tee output_2.txt
    ```
        
    [Output sample with debug messages](/7/output_2.txt)
    
    [List of found lucky numbers](/7/lucky_numbers.txt)
    
    ![Example output](/7/screenshots/task2_1.png)
    
    
### Task 3
  - Write a script that takes a list of words (or even phrases) as an arguments. Script should ask a user to write something to stdin until user won't provide one of argument phrases.

    [task3.sh](/7/task3.sh):
    ```sh
    #!/bin/bash -x
    f=0
    while read input; do
            for word in $input; do
                    if [[ "$@" == *$word* ]]
                            then f=1
                    fi
            done

            if [ $f = 1 ]
                    then echo Correct!; break
                    else echo Try again!
            fi
    done < /dev/tty
    ```
    
    ```
    $ chmod +x task3.sh
    $ ./task3.sh apple beetle coffee danon egg friend 
    ```
    
    ![Example output](/7/screenshots/task3_1.png)
    
    

### Task 4
  - As bash doesn't have any syntax standardisation a lot of bash users develop scripts that make further readers very unhappy. Also, these guys often over engineers such scripts. This is an example of this script. Please analyse a script and try to make it as readable and functional as possible from your sense of beauty.
    
    ```
    export SUM=0; for f in $(find src -name "*.java");
    do export SUM=$(($SUM + $(wc -l $f | awk '{ print $1 }'))); done; echo $SUM
    ```
    
    As this script doesn't seem to have any child processes, I would exclude *'export'*, and would write it like this:
    
    ```sh
    #!/bin/bash
    
    SUM=0
    for f in $(find src -name "*.java")
    do 
        ROWS=$(wc -l $f | awk '{ print $1 }')
        SUM=$(( $SUM + $ROWS )) 
    done
    
    echo $SUM    
    ```
    


### Task 5
  - `stat` command shows when a particular file was accessed. Unfortunately, it can't show who it was.
  As a first step, you should study a Shell Variables section of man bash, enable an unlimited history size and time stamping of command execution.
  As a second step*, provide a script that will get list of files as arguments, it should find a user who have last accessed each file and print a line in the following fashion:
  
  `<filename> <user> <time>` 
  
  and color it red if file was not just accessed but also modified.
  ___
  
  

____

## RegExp


### Task 1
  - Stacktraces of JVM languages looks the following way:
    
    ```
      Caused by: org.apache.thrift.transport.TTransportException
      at org.apache.thrift.transport.TIOStreamTransport.read(TIOStreamTransport.java:132)
      at org.apache.thrift.transport.TTransport.readAll(TTransport.java:86)
      at org.apache.thrift.transport.TSaslTransport.receiveSaslMessage(TSaslTransport.java:178)
      at org.apache.thrift.transport.TSaslTransport.open(TSaslTransport.java:305)
      at org.apache.thrift.transport.TSaslClientTransport.open(TSaslClientTransport.java:37)
      at com.cloudera.hivecommon.api.HiveServer2ClientFactory.createTransport(Unknown Source)
      at com.cloudera.hivecommon.api.HiveServer2ClientFactory.createClient(Unknown Source)
      at com.cloudera.hivecommon.core.HiveJDBCCommonConnection.establishConnection(Unknown Source)
      at com.cloudera.impala.core.ImpalaJDBCConnection.establishConnection(Unknown Source)
      at com.cloudera.jdbc.core.LoginTimeoutConnection.connect(Unknown Source)
      at com.cloudera.jdbc.common.BaseConnectionFactory.doConnect(Unknown Source)
      at com.cloudera.jdbc.common.AbstractDriver.connect(Unknown Source)
      at org.apache.commons.dbcp2.DriverConnectionFactory.createConnection(DriverConnectionFactory.java:55)
      at org.apache.commons.dbcp2.PoolableConnectionFactory.makeObject(PoolableConnectionFactory.java:355)
      at org.apache.commons.dbcp2.BasicDataSource.validateConnectionFactory(BasicDataSource.java:115)
      at org.apache.commons.dbcp2.BasicDataSource.createPoolableConnectionFactory(BasicDataSource.java:665)
      at org.apache.commons.dbcp2.BasicDataSource.createDataSource(BasicDataSource.java:544)
      at org.apache.commons.dbcp2.BasicDataSource.getConnection(BasicDataSource.java:753)
      at org.apache.commons.dbutils.AbstractQueryRunner.prepareConnection(AbstractQueryRunner.java:319)
      at org.apache.commons.dbutils.QueryRunner.query(QueryRunner.java:345)
      at com.blah.nbs.validation.util.client.sql.AbstractSqlClient.lambda$executeQuery$0(AbstractSqlClient.java:55)
      at com.machinezoo.noexception.CheckedExceptionHandler$CheckedFunction.apply(CheckedExceptionHandler.java:723)
      at com.blah.nbs.validation.util.client.sql.AbstractSqlClient.lambda$executeSql$2(AbstractSqlClient.java:71)
      at java.util.concurrent.FutureTask.run(FutureTask.java:266)
      at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
      at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
      at java.lang.Thread.run(Thread.java:748)
    ```
    
    Write a sed one-liner that will show stack traces lines in the following fashion:
    
    ```
    You have a problem with entity org.apache.hadoop.fs.FileSystem$Cache.getInternal! 
    You can find more info about it in file FileSystem.java at line 2703. This file is written on java.
    ```
    ___
    
    
    



### Task 2
  - Write a RegEx that validates entries under */etc/passwd*.


### Task 3
  - Write a RegEx that will validate URI: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier 
