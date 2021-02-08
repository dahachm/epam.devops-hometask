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
