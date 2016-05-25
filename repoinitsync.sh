mkdir $1
cd $1
wget 192.168.10.120/files/repo
chmod 777 repo
./repo init -u git://192.168.10.120/manifests.git -b $1
./repo sync
      