#!/bin/sh

echo "cloneAllBitbucket.sh username targetuserorteam"
USER=$1; curl --user ${USER} https://api.bitbucket.org/2.0/repositories/$2 | grep -o '"ssh:[^ ,]\+' | xargs -L1 git clone
