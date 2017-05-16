#!/bin/bash

is_alive_ping()
{
  ping -c 1 -W 1 $1 > /dev/null
  [ $? -eq 0 ] && echo $i ,Alive
}

for i in 192.168.31.{1..255}
do
#is_alive_ping $i &
is_alive_ping $i
done
