# Task 4
  
  Создать в домашней директории файлы file_name1.md, file_name2.md и file_name3.md. 
  
  ```
  $ touch file_name{1..3}.md
  ```
  
  ![Результат работы команды](/1/screenshots/task4_1.png)
  
  Используя {}, переименовать:
  
    - file_name1.md в file_name1.textdoc
    - file_name2.md в file_name2
    - file_name3.md в file_name3.md.latest
    - file_name1.textdoc в file_name1.txt
    
  Для реализации напишем следущий [shell-скрипт](/1/task_4):
  
  ```sh
    for file in file_name{{1..3}.md,1.textdoc}; do
      if [ $file == "file_name1.md" ]; then 
        mv $file "file_name1.textdoc";
        echo "$file --> file_name1.textdoc";
      fi

      if [ $file == "file_name2.md" ]; then
        mv $file "file_name2";
        echo "$file --> file_name2";
      fi

      if [ $file == "file_name3.md" ]; then
        mv $file "file_name3.md.latest";
        echo "$file --> file_name3.md.latest";
      fi

      if [ $file == "file_name1.textdoc" ]; then
        mv $file "file_name1.txt";
        echo "$file --> file_name1.txt";
      fi;
    done
  ```
  
  ```
  $ chmod u+x task_4
  $ ./task_4
  ```
  
  ![Результат работы команды](/1/screenshots/task4_2.png)
  
