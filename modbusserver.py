#!/usr/bin/python3
# minimal server send 2 tempature to a queue

import stomp
import json
import time
import uuid
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        #print('received a message "%s"' % message)
        cmds=str.split(message, '-')
        if cmds[0] == "On":
          instrument.write_register(address=3, count=1, unit=2, value=1)
        else:
          instrument.write_register(address=3, count=1, unit=2, value=0)
        if len(cmds) >=2 and cmds[1] == "On":
          instrument.write_register(address=4, count=1, unit=2, value=1)
        else:
          instrument.write_register(address=4, count=1, unit=2, value=0)

# connect to Insdustruino (slave 2)
instrument = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate = 115200, stopbits = 2)

# connection to ActiveMQ on my laptop. 
conn = stomp.Connection([('192.168.1.124', 61613)])
conn.set_listener('', MyListener())
 
# conn.start()
 
conn.connect()

# send Hello and our id.
PIid='MyPI:' + str(uuid.getnode())
mess='Hello'
json_string = '{"deviceID": "' + PIid + '", "text": "' + mess + '"}'
print(json.dumps(json_string))

conn.send(body=json_string, destination='/topic/PITopic')

# receive for our queue (hopefully a welcome or Hello)
conn.subscribe(destination='/queue/' + PIid, id=1, ack='auto')

# read and send temperature every 10 seconds.
while True:
  time.sleep(10)
  temp1 = instrument.read_holding_registers(address=0, count=1, unit=2)
  temp2 = instrument.read_holding_registers(address=1, count=1, unit=2)
  mess='Temperature1: ' + str(temp1.getRegister(0)/100) + ' C Temperature2: ' +  str(temp2.getRegister(0)/100) + ' C '
  print(mess)
  json_string = '{"deviceID": "' + PIid + '", "text": "' + mess + '"}'
  conn.send(body=json_string, destination='/topic/PITopic')
 
conn.disconnect()
