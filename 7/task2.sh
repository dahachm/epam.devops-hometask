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
