# EOS SDK VRRP IP Tracking

## Switch Setup
### Install
1. Copy `VRRPIPTracking-x.x.x-x.swix` to `/mnt/flash/` on the switch or to the `flash:` directory.
2. Copy and install he `.swix` file to the extensions directory from within EOS.  Below command output shows the copy and install process for the extension.
```
L3-L11#copy flash:VRRPIPTracking-0.2.0-1.swix extension:
Copy completed successfully.
L3-L11#sh extensions
Name                                Version/Release      Status      Extension
----------------------------------- -------------------- ----------- ---------
VRRPIPTracking-0.2.0-1.swix         0.2.0/1              A, NI        1

A: available | NA: not available | I: installed | NI: not installed | F: forced
L3-L11#extension VRRPIPTracking-0.2.0-1.swix
L3-L11#sh extensions
Name                                Version/Release      Status      Extension
----------------------------------- -------------------- ----------- ---------
VRRPIPTracking-0.2.0-1.swix         0.2.0/1              A, I        1

A: available | NA: not available | I: installed | NI: not installed | F: forced
```
3. In order for the extension to be installed on-boot, enter the following command:
```
L3-L11#copy extensions: boot-extensions
```

### VRRP IP Tracking Agent Configuration
1. In EOS config mode perform the following commands for basic functionality (see step #4 for further customization):
```
config
daemon VRRPIPTracking
exec /usr/bin/VRRPIPTracking
no shutdown
```
2. By default, the agent has the following default values in terms of polling:
- master = 110
- standby = 90
- Polling interval = 5 seconds
- Trigger threshold = 3 consecutive failed/success attempts
- VRF = default (VRF used on the switch by default)

To modify the default behavior, use the following commands to override the defaults:
```
config
daemon VRRPIPTracking
option master value {master_value}
option standby value {standby_value}
option poll value {time_in_seconds}
option threshold value {number_of_failures}
option vrf value {vrf_name}
option source value {source_intf}
```
**`master_value` **(optional)** Specify a specific priority level for the node to become the VRRP Master**

**`standby_value` **(optional)** Specify a specific priority level for the node to become the VRRP Backup**

**`time_in_seconds` **(optional)** how much time the agent should wait until it tries to poll the IP addresses**

**`number_of_failures` **(optional)** how many failures should occur consecutively before an action is triggered**

**`email_address` **(required for email alerting)** the email address for the agent to send an alert if the threshold has been reached**

**`vrf_name` **(optional)** the name of the VRF that the pings should originate from (VRF name is case-sensitive)**

**`source_intf` **(optional)** interface to source ping from. ie `et44, et49_1, ma1, vlan100` See conversion list below for interface mappings**

##### Interface Mappings
- et44 --> Ethernet44
- et49_1 --> Ethernet49/1
- ma1 --> Management1
- vlan100 --> Vlan100

3. In order for this agent to monitor IP addresses, the following commands will need to be taken:
```
config
daemon VRRPIPTracking
option {device_name} value {ip_of_device}
```
**`device_name` needs to be a unique identifier for each remote switch/device**

**`ip_of_device` needs to be a valid IPv4 address for the remote device for monitoring**

**To see what unique peer identifiers have been created, enter `show daemon IpMon`**

Example of a full `daemon VRRPIPTracking` config would look like with all parameters specified
```
config
daemon VRRPIPTracking
   option master value 115
   option standby value 95
   option vlan101 value 1
   option remote-host31 value 192.168.12.31
   option poll value 15
   option threshold value 5
   option vrf value MGMT
   option source value vlan100
   no shutdown
```

#### Sample output of `show daemon VRRPIPTracking`
```
L3-L11#sh daemon VRRPIPTracking
Agent: VRRPIPTracking (running with PID 10605)
Uptime: 0:00:03 (Start time: Thu May 19 16:20:14 2022)
Configuration:
Option        Value
------------- -------------
h31           192.168.12.31
vlan101       1

Status:
Data                         Value
---------------------------- ------------------------
Master-Priority              110
Standby-Priority             90
VRF                          default
h31 has been up since:       Thu May 19 16:20:16 2022
vlan101                      master
Arista#
L3-L11#sh daemon VRRPIPTracking
Agent: VRRPIPTracking (running with PID 10605)
Uptime: 0:01:13 (Start time: Thu May 19 16:20:14 2022)
Configuration:
Option        Value
------------- -------------
h31           192.168.12.31
vlan101       1

Status:
Data                           Value
------------------------------ ------------------------
Master-Priority                110
Standby-Priority               90
VRF                            default
h31 has been DOWN since:       Thu May 19 16:21:02 2022
vlan101                        backup
```
