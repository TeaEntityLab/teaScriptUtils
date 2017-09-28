#!/bin/sh

echo "cloneAllGithub.sh targetuserorteam"
curl -s https://api.github.com/orgs/$1/repos\?per_page\=200 | grep clone_url | awk -F '"' '{print $4}' | xargs -n 1 -P 4 git clone
