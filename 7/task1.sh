#!/bin/bash -x

sum=0

for pid in $(ps -eo pid); do
	sum=$(( $sum + $pid ));
done

echo $sum
