# Flow Rule Timeout Manager using Ryu and Mininet

## Overview
This project demonstrates dynamic flow rule management in Software Defined Networking (SDN) using a Ryu controller and Mininet. The controller installs a temporary drop rule to block traffic from a specific host and automatically removes it after a fixed timeout, allowing normal communication to resume. This showcases the lifecycle of flow rules and centralized control in SDN.

## Objectives
- Demonstrate controller–switch interaction using OpenFlow
- Implement match–action based flow rules
- Show blocking and recovery of network traffic
- Analyze network behavior using ping and iperf
- Demonstrate flow rule lifecycle and timeout handling

## Topology

A simple topology is used:

h1 ----\
        >---- s1 ---- Controller (Ryu)
h2 ----/

- Hosts: h1, h2
- Switch: s1 (Open vSwitch)
- Controller: Ryu
- Protocol: OpenFlow 1.3

## Technologies Used
- Python (Ryu Controller)
- Mininet
- Open vSwitch
- OpenFlow 1.3
- iperf

## Setup and Execution

### 1. Start the Ryu Controller

source ~/ryu-env/bin/activate
python3 -m ryu.cmd.manager timeout_controller.py


### 2. Start Mininet

sudo mn -c
sudo mn --topo single,2 --controller remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13


## Demonstration Steps

### Scenario 1: Blocking Traffic

mininet> h1 ping -c 3 h2

Expected:
- Destination Host Unreachable
- Controller logs show blocking

Start iperf:

mininet> h2 iperf -s &
mininet> h1 iperf -c h2

Expected:
- Low or unstable throughput

### Wait for Timeout
- Wait approximately 10 seconds
- Controller logs display: FLOW EXPIRED

### Scenario 2: Recovery After Timeout

mininet> h1 ping -c 3 h2

Expected:
- Successful ping replies


mininet> h1 iperf -c h2

Expected:
- Stable throughput (~20+ Mbits/sec)

## Flow Table Inspection (Optional)

mininet> dpctl dump-flows


- During blocking: drop rule present
- After timeout: rule removed or inactive

## Key Concepts
- Software Defined Networking (SDN)
- Control plane and data plane separation
- OpenFlow protocol
- Match–action flow rules
- Hard timeout
- Flow rule lifecycle

## Results
- Traffic is initially blocked using a drop rule
- The rule expires automatically after 10 seconds
- Communication is restored without manual intervention
- Throughput improves after rule expiration

## Conclusion
This project demonstrates how SDN enables dynamic and programmable network control. By using timed flow rules, the controller can enforce temporary policies such as blocking and automatically restore connectivity, highlighting the flexibility and power of SDN-based networks.

## How to Run
1. Start the Ryu controller
2. Start Mininet with remote controller
3. Run ping to observe blocking
4. Run iperf to analyze throughput
5. Wait for timeout and observe recovery

## Author
Manasi Sabnis
