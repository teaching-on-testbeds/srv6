"""SRv6 hand-drawn topology"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

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

# Node source-classic
node_source_classic = request.RawPC('source-classic')
node_source_classic.hardware_type = 'd430'
node_source_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface0 = node_source_classic.addInterface('interface-2', pg.IPv4Address('10.0.10.3','255.255.255.0'))

# Node source-l4s
node_source_l4s = request.RawPC('source-l4s')
node_source_l4s.hardware_type = 'd430'
node_source_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface1 = node_source_l4s.addInterface('interface-0', pg.IPv4Address('10.0.10.4','255.255.255.0'))

# Node source-router
node_source_router = request.RawPC('source-router')
node_source_router.hardware_type = 'd430'
node_source_router.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface2 = node_source_router.addInterface('interface-1', pg.IPv4Address('10.0.10.1','255.255.255.0'))
iface3 = node_source_router.addInterface('interface-3', pg.IPv4Address('10.0.11.1','255.255.255.0'))

# Node middle-l4s
node_middle_l4s = request.RawPC('middle-l4s')
node_middle_l4s.hardware_type = 'd430'
node_middle_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface4 = node_middle_l4s.addInterface('interface-4', pg.IPv4Address('10.0.11.4','255.255.255.0'))
iface5 = node_middle_l4s.addInterface('interface-6', pg.IPv4Address('10.0.12.4','255.255.255.0'))

# Node middle-classic
node_middle_classic = request.RawPC('middle-classic')
node_middle_classic.hardware_type = 'd430'
node_middle_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface6 = node_middle_classic.addInterface('interface-5', pg.IPv4Address('10.0.11.3','255.255.255.0'))
iface7 = node_middle_classic.addInterface('interface-8', pg.IPv4Address('10.0.12.3','255.255.255.0'))

# Node dest-router
node_dest_router = request.RawPC('dest-router')
node_dest_router.hardware_type = 'd430'
node_dest_router.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface8 = node_dest_router.addInterface('interface-7', pg.IPv4Address('10.0.12.1','255.255.255.0'))
iface9 = node_dest_router.addInterface('interface-10', pg.IPv4Address('10.0.13.1','255.255.255.0'))

# Node dest-l4s
node_dest_l4s = request.RawPC('dest-l4s')
node_dest_l4s.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface10 = node_dest_l4s.addInterface('interface-9', pg.IPv4Address('10.0.13.4','255.255.255.0'))

# Node dest-classic
node_dest_classic = request.RawPC('dest-classic')
node_dest_classic.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD";
iface11 = node_dest_classic.addInterface('interface-11', pg.IPv4Address('10.0.13.3','255.255.255.0'))

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
