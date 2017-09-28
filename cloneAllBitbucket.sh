#!/bin/sh

echo "cloneAllBitbucket.sh username targetuserorteam"

cwd=$(pwd)

#USER=$1; curl --user ${USER} https://api.bitbucket.org/2.0/repositories/$2 | grep -o '"ssh:[^ ,]\+' | xargs -L1 git clone

curl -u ${1} https://api.bitbucket.org/1.0/users/${2} > repoinfo

if [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX

for repo_name in `cat repoinfo | gsed -r 's/("name": )/\n\1/g' | gsed -r 's/"name": "(.*)"/\1/' | gsed -e 's/{//' | cut -f1 -d\" | tr '\n' ' '`
do
    echo "Cloning " $repo_name
    git clone git@bitbucket.org:${2}/$repo_name.git
    cd $repo_name
    git pull
    cd $cwd
    echo "---"
done

else
        # Unknown.

for repo_name in `cat repoinfo | sed -r 's/("name": )/\n\1/g' | sed -r 's/"name": "(.*)"/\1/' | sed -e 's/{//' | cut -f1 -d\" | tr '\n' ' '`
do
    echo "Cloning " $repo_name
    git clone git@bitbucket.org:${2}/$repo_name.git
    cd $repo_name
    git pull
    cd $cwd
    echo "---"
done

fi
