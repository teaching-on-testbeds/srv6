sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo sysctl -w net.ipv6.conf.all.seg6_enabled=1
sudo sysctl -w net.ipv6.conf.default.seg6_enabled=1
for iface in $(ls /sys/class/net/ | grep -E "^[e]"); do sudo sysctl -w net.ipv6.conf.$iface.seg6_enabled=1; done
