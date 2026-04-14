# SDN Flow Rule Timeout Manager using Ryu and Mininet


#Problem Statement
This project demonstrates flow rule lifecycle in Software Defined Networking (SDN) using a Ryu controller and Mininet.
The controller dynamically installs a drop rule with timeout, blocks traffic, and automatically restores connectivity after rule expiration.

#Objectives

* Demonstrate controller–switch interaction
* Implement match–action flow rules
* Show blocking and recovery behavior
* Observe flow lifecycle using timeout
* Analyze network performance using ping and iperf

#Topology

A simple Mininet topology is used:


h1 ----\
        >---- s1 ---- Controller (Ryu)
h2 ----/


* Hosts: h1, h2
* Switch: s1 (Open vSwitch)
* Controller: Ryu
* Protocol: OpenFlow 1.3

# Setup Requirements

* Ubuntu (VM / AWS)
* Python3
* Mininet
* Ryu Controller
* Wireshark (optional)

#Execution Steps
 1. Start Controller

bash
source ~/ryu-env/bin/activate
python3 -m ryu.cmd.manager timeout_controller.py

2. Start Mininet

bash
sudo mn -c
sudo mn --topo single,2 --controller remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13
3. Clear Previous Flows

bash
mininet> dpctl del-flows

#Testing & Demonstration

 Scenario 1: Blocking Traffic

bash
mininet> h1 ping -c 2 h2


Output:

* Destination Host Unreachable
* Controller log: `BLOCKING h1 TRAFFIC`
bash
mininet> h1 iperf -c h2

Observation:

* Throughput is zero or very low
* Traffic is blocked

# Wait for Timeout (~10 seconds)

Controller log:


FLOW EXPIRED

#Scenario 2: Recovery After Timeout

bash
mininet> h1 ping -c 2 h2

Output:

* Successful ping

bash
mininet> h1 iperf -c h2

Output:

* Non-zero throughput (~20+ Mbits/sec)

Observation:

* Communication restored after rule expiration


# Regression Test

bash
mininet> dpctl del-flows
mininet> h1 ping -c 2 h2
(wait)
mininet> h1 ping -c 2 h2

Observation:

* Same behavior repeats consistently
* Confirms reliability of controller logic

 Flow Table Inspection
bash
mininet> dpctl dump-flows


* Before timeout → shows drop rule
* After timeout → rule removed

# Wireshark Analysis (Optional)

Filter:

```
icmp
```

# During Blocking:

* ICMP request seen
* No reply

### After Timeout:

* ICMP request + reply


#Key Concepts Used

* Software Defined Networking (SDN)
* OpenFlow Protocol
* Match–Action Flow Rules
* PacketIn / PacketOut
* Hard Timeout
* Flow Rule Lifecycle


