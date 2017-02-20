sudo sysctl -w net.ipv4.ip_forward=1
echo 0 | sudo tee /proc/sys/net/ipv4/conf/*/send_redirects
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080
# mitmweb --host
sh -c mitmproxy --host
