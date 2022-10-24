# modbusOpenShift
Sending modbus data to ActiveMQ running on OpenShift

# install in the RPI what is needed
```bash
sudo apt-get update
sudo apt-get -y install git
sudo apt-get install -y python3-stomp python3-pymodbus python3-pip
pip3 install -U minimalmodbus
```

# Testing
Install ActiveMQ and start it on a box (change 192.168.1.124 in modbusserver.py and client.html by the IP of your box).

A queue MyPI:nnnnn is receiving for the RPI and a topic PITopic is used to send commands.

Run the client "client.html" on a browser, you should get something like: https://raw.githubusercontent.com/jfclere/modbusOpenShift/main/client.png
