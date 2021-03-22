#!/bin/bash
#set -x
IP=$1
VIP=$2

#echo $CLUSTER_NAME

echo $'\nARP ******************************************'
ssh root@$IP "ping -c 3 $2"
lines=$(ssh root@$IP 'arp -a')
echo "$lines"

echo "EXPECT::Somewhere::"