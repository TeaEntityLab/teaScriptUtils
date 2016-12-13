# Usage: cpfromserver.sh $* <<< "-pPassword -i YourRSA.id_rsa yourserver@0.0.0.0"

echo -n "ssh "
read SSH_OPTIONS
LOCAL_ROOT=~/remote
REMOTE_TRANSFER="tar -C / -cf - $*"
LOCAL_TRANSFER="tar -C $LOCAL_ROOT/ -xvf -"
ssh $SSH_OPTIONS $REMOTE_TRANSFER | $LOCAL_TRANSFER
