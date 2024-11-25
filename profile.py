# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# IPv6 Subnet Assignments
# link-0: 2001:db8:10::/64
# link-1: 2001:db8:11::/64
# link-2: 2001:db8:12::/64
# link-3: 2001:db8:13::/64

# Helper Function to Assign IPv6 Addresses
def assign_ipv6(node, ipv6_addr, ipv4_target):
    command = 'sudo ip -6 addr add {}/64 dev $(ip route get {} | grep -oP "(?<=dev )[^ ]+")'.format(ipv6_addr, ipv4_target)
    node.addService(pg.Execute(shell="bash", command=command))

# Helper Function to Enable SRv6 on All Interfaces
# here we do not not need to be selective, because it does not hurt to turn on srv6. 
def enable_srv6(node):
    commands = [
        'sudo sysctl -w net.ipv6.conf.all.forwarding=1',
        'sudo sysctl -w net.ipv6.conf.all.seg6_enabled=1',
        'sudo sysctl -w net.ipv6.conf.default.seg6_enabled=1',
        'for iface in $(ls /sys/class/net/ | grep -E "^[e]"); do sudo sysctl -w net.ipv6.conf.$iface.seg6_enabled=1; done'
    ]
    for cmd in commands:
        node.addService(pg.Execute(shell="bash", command=cmd))

# Node source-classic
node_source_classic = request.RawPC('source-classic')
node_source_classic.hardware_type = 'd710'
node_source_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface0 = node_source_classic.addInterface('interface-2')
iface0.addAddress(pg.IPv4Address('10.0.10.3','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_source_classic, '2001:db8:10::3', '10.0.10.1')
# Set default IPv6 route via source-router
node_source_classic.addService(pg.Execute(shell="bash", command="sudo ip -6 route add default via 2001:db8:10::1"))

# Node source-l4s
node_source_l4s = request.RawPC('source-l4s')
node_source_l4s.hardware_type = 'd430'
node_source_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface1 = node_source_l4s.addInterface('interface-0')
iface1.addAddress(pg.IPv4Address('10.0.10.4','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_source_l4s, '2001:db8:10::4', '10.0.10.1')
# Set default IPv6 route via source-router
node_source_l4s.addService(pg.Execute(shell="bash", command="sudo ip -6 route add default via 2001:db8:10::1"))

# Node source-router
node_source_router = request.RawPC('source-router')
node_source_router.hardware_type = 'd710'
node_source_router.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface2 = node_source_router.addInterface('interface-1')
iface2.addAddress(pg.IPv4Address('10.0.10.1','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_source_router, '2001:db8:10::1', '10.0.10.3')
iface3 = node_source_router.addInterface('interface-3')
iface3.addAddress(pg.IPv4Address('10.0.11.1','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_source_router, '2001:db8:11::1', '10.0.11.3')
# Enable IPv6 forwarding
node_source_router.addService(pg.Execute(shell="bash", command="sudo sysctl -w net.ipv6.conf.all.forwarding=1"))
# Add static IPv6 routes
node_source_router.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:12::/64 via 2001:db8:11::3"))
node_source_router.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:13::/64 via 2001:db8:11::3"))

enable_srv6(node_source_router)

# Delete the original route that might conflict with SRv6 routing
node_source_router.addService(pg.Execute(shell="bash", command="sudo ip -6 route del 2001:db8:13::/64 via 2001:db8:11::3"))

# For L4S Traffic
# Add policy routing rule to use table 100 for traffic from 2001:db8:10::4
node_source_router.addService(pg.Execute(shell="bash", command='sudo ip -6 rule add from 2001:db8:10::4 lookup 100 pref 100'))
# Add SRv6 route to dest-l4s via middle-l4s in table 100
node_source_router.addService(pg.Execute(shell="bash", command='sudo ip -6 route add 2001:db8:13::4/128 encap seg6 mode encap segs 2001:db8:11::4,2001:db8:12::1 dev $(ip route get 2001:db8:11::4 | grep -oP "(?<=dev )[^ ]+") table 100'))

# For Classic Traffic
# Add policy routing rule to use table 200 for traffic from 2001:db8:10::3
node_source_router.addService(pg.Execute(shell="bash", command='sudo ip -6 rule add from 2001:db8:10::3 lookup 200 pref 110'))
# Add SRv6 route to dest-classic via middle-classic in table 200
node_source_router.addService(pg.Execute(shell="bash", command='sudo ip -6 route add 2001:db8:13::3/128 encap seg6 mode encap segs 2001:db8:11::3,2001:db8:12::1 dev $(ip route get 2001:db8:11::3 | grep -oP "(?<=dev )[^ ]+") table 200'))


# Node middle-l4s
node_middle_l4s = request.RawPC('middle-l4s')
node_middle_l4s.hardware_type = 'd710'
node_middle_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface4 = node_middle_l4s.addInterface('interface-4')
iface4.addAddress(pg.IPv4Address('10.0.11.4','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_middle_l4s, '2001:db8:11::4', '10.0.11.1')
iface5 = node_middle_l4s.addInterface('interface-6')
iface5.addAddress(pg.IPv4Address('10.0.12.4','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_middle_l4s, '2001:db8:12::4', '10.0.12.1')
# Enable IPv6 forwarding
node_middle_l4s.addService(pg.Execute(shell="bash", command="sudo sysctl -w net.ipv6.conf.all.forwarding=1"))
# Add static IPv6 routes
node_middle_l4s.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:10::/64 via 2001:db8:11::1"))
node_middle_l4s.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:13::/64 via 2001:db8:12::1"))

# Enable SRv6 on middle-l4s
enable_srv6(node_middle_l4s)

# Node middle-classic
node_middle_classic = request.RawPC('middle-classic')
node_middle_classic.hardware_type = 'd710'
node_middle_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface6 = node_middle_classic.addInterface('interface-5')
iface6.addAddress(pg.IPv4Address('10.0.11.3','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_middle_classic, '2001:db8:11::3', '10.0.11.1')
iface7 = node_middle_classic.addInterface('interface-8')
iface7.addAddress(pg.IPv4Address('10.0.12.3','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_middle_classic, '2001:db8:12::3', '10.0.12.1')
# Enable IPv6 forwarding
node_middle_classic.addService(pg.Execute(shell="bash", command="sudo sysctl -w net.ipv6.conf.all.forwarding=1"))
# Add static IPv6 routes
node_middle_classic.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:13::/64 via 2001:db8:12::1"))
node_middle_classic.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:10::/64 via 2001:db8:11::1"))

# Enable SRv6 on middle-classic
enable_srv6(node_middle_classic)

# Node dest-router
node_dest_router = request.RawPC('dest-router')
node_dest_router.hardware_type = 'd710'
node_dest_router.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface8 = node_dest_router.addInterface('interface-7')
iface8.addAddress(pg.IPv4Address('10.0.12.1','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_dest_router, '2001:db8:12::1', '10.0.12.3')
iface9 = node_dest_router.addInterface('interface-10')
iface9.addAddress(pg.IPv4Address('10.0.13.1','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_dest_router, '2001:db8:13::1', '10.0.13.3')
# Enable IPv6 forwarding
node_dest_router.addService(pg.Execute(shell="bash", command="sudo sysctl -w net.ipv6.conf.all.forwarding=1"))
# Add static IPv6 routes
node_dest_router.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:10::/64 via 2001:db8:12::3"))
node_dest_router.addService(pg.Execute(shell="bash", command="sudo ip -6 route add 2001:db8:11::/64 via 2001:db8:12::3"))

# Enable SRv6 on dest-router
enable_srv6(node_dest_router)

# Node dest-l4s
node_dest_l4s = request.RawPC('dest-l4s')
node_dest_l4s.hardware_type = 'd710'
node_dest_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface10 = node_dest_l4s.addInterface('interface-9')
iface10.addAddress(pg.IPv4Address('10.0.13.4','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_dest_l4s, '2001:db8:13::4', '10.0.13.1')
# Set default IPv6 route via dest-router
node_dest_l4s.addService(pg.Execute(shell="bash", command="sudo ip -6 route add default via 2001:db8:13::1"))
enable_srv6(node_middle_l4s)


# Node dest-classic
node_dest_classic = request.RawPC('dest-classic')
node_dest_classic.hardware_type = 'd710'
node_dest_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
iface11 = node_dest_classic.addInterface('interface-11')
iface11.addAddress(pg.IPv4Address('10.0.13.3','255.255.255.0'))
# Assign IPv6 Address
assign_ipv6(node_dest_classic, '2001:db8:13::3', '10.0.13.1')
# Set default IPv6 route via dest-router
node_dest_classic.addService(pg.Execute(shell="bash", command="sudo ip -6 route add default via 2001:db8:13::1"))
enable_srv6(node_middle_l4s)


# Link link-0
link_0 = request.Link('link-0')
link_0.Site('undefined')
link_0.addInterface(iface1)
link_0.addInterface(iface2)
link_0.addInterface(iface0)

# Link link-1
link_1 = request.Link('link-1')
link_1.Site('undefined')
link_1.addInterface(iface3)
link_1.addInterface(iface4)
link_1.addInterface(iface6)

# Link link-2
link_2 = request.Link('link-2')
link_2.Site('undefined')
link_2.addInterface(iface5)
link_2.addInterface(iface8)
link_2.addInterface(iface7)

# Link link-3
link_3 = request.Link('link-3')
link_3.Site('undefined')
link_3.addInterface(iface10)
link_3.addInterface(iface9)
link_3.addInterface(iface11)

# Print the generated rspec
pc.printRequestRSpec(request)
