#!/bin/bash
    
    export SUM=0
    for f in $(find /src -name "*.java")
    do 
        ROWS=$(wc -l $f | awk '{ print $1 }')
        export SUM=$(( $SUM + $ROWS )) 
    done
    
    echo $SUM  
