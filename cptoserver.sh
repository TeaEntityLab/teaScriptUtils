# Usage: cptoserver.sh $* <<< "-pPassword -i YourRSA.id_rsa yourserver@0.0.0.0"

echo -n "ssh "
read SSH_OPTIONS
REMOTE_ROOT="~/remote"
LOCAL_TRANSFER="tar -C / -cf - $*"
REMOTE_TRANSFER="tar -C $REMOTE_ROOT/ -xvf -"
ssh $SSH_OPTIONS "mkdir $REMOTE_ROOT"
$LOCAL_TRANSFER | ssh $SSH_OPTIONS $REMOTE_TRANSFER

# tar -C / -cf - \
#   opt/widget etc/widget etc/cron.d/widget etc/init.d/widget \
#   --exclude=opt/widget/local.conf |
#   ssh otherhost tar -C / -xvf -
