#!/bin/bash


PIECE=$(cat <<EOF
master0 works
master1 works
EOF
)

FILE=$1

echo "START" >> $FILE

sleep 5

for number in {1..10}
do
    echo "$number " >> $FILE
    sleep 1
done

sleep 5

echo $PIECE >> $FILE

sleep 5

echo $PIECE >> $FILE

echo "DONE" >> $FILE


