sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo sysctl -w net.ipv6.conf.all.seg6_enabled=1
sudo sysctl -w net.ipv6.conf.default.seg6_enabled=1
for iface in $(ls /sys/class/net/ | grep -E "^[e]"); do sudo sysctl -w net.ipv6.conf.$iface.seg6_enabled=1; done



sudo ip -6 rule add from 2001:db8:10::4 lookup 100 pref 100

sudo ip -6 route add 2001:db8:13::4/128 encap seg6 mode encap segs 2001:db8:11::4,2001:db8:12::1 dev $(ip route get 2001:db8:11::4 | grep -oP "(?<=dev )[^ ]+") table 100

sudo ip -6 rule add from 2001:db8:10::3 lookup 200 pref 110

sudo ip -6 route add 2001:db8:13::3/128 encap seg6 mode encap segs 2001:db8:11::3,2001:db8:12::1 dev $(ip route get 2001:db8:11::3 | grep -oP "(?<=dev )[^ ]+") table 200

sudo ip -6 route del 2001:db8:13::/64 via 2001:db8:11::3




