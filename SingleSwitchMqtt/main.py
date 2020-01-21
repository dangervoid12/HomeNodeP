import network
import socket
import machine
from machine import Pin
import time
import sys
import ubinascii
from umqtt.simple import MQTTClient



myId = "hnp001"
myClass = "01" 
apName = ""  // update here
apPass = "" // update here
apIp = ""
myIp = ""

wlan = network.WLAN(network.STA_IF)

myStatus = "0"

client = None

CONFIG = {
    "broker": "", // update here ip
    "switch_pin": 0, 
    "client_id": b"hnp001_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"hnp001",
}

def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")

def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")
        
def mqttRecv(topic, msg):
    print("MQTT message recievied")
    print((topic, msg))
    myParser(msg)

 
def setupMqtt():
   global client;
   #client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
   client = MQTTClient(CONFIG['client_id'], "io.adafruit.com",user="", password="", port=1883) // for adafruit broker update user and pass
   client.set_callback(mqttRecv)
   client.connect()
   #tmp2 =b'dangervoid/feeds/{}/{}'.format(CONFIG['client_id'].decode("utf-8"),CONFIG['topic'].decode("utf-8"))
   tmp2 =b'dangervoid/feeds/{}'.format(CONFIG['topic'].decode("utf-8"))
   
   print("Listening on topic: {}".format(tmp2))
   client.subscribe(tmp2)
   #client.subscribe(topic=tmp2) 
   print("Mqtt connected to {}".format(CONFIG['broker']))
   while True:
        if True:
            # Blocking wait for message
            client.wait_msg()
        else:
            # Non-blocking wait for message
            client.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)
            
	
def sendMqtt(data):
  print("SendMqtt: ", data)
  #client.publish('{}/{}'.format(CONFIG['client_id'].decode("utf-8"),CONFIG['topic'].decode("utf-8")), str(data))
  client.publish('{}'.format(CONFIG['topic'].decode("utf-8")), str(data))
  
def startMain():
  print("");
  print("Welcome to Home Node P");
  print("Configuring connection...");
  connectToWifi();
  print("Configuring mqtt...");
  setupMqtt()
  

	
def connectToWifi():
  global myIp;
  global apIp;
  
  wlan.active(True)
  if not wlan.isconnected():
    sys.stdout.write("Connecting to network ")
    sys.stdout.write(apName)
    wlan.connect(apName, apPass)
    while not wlan.isconnected():
      time.sleep_ms(500)
      sys.stdout.write(".")
    print('Network config:', wlan.ifconfig())
    myIp = wlan.ifconfig()[0]
    apIp = wlan.ifconfig()[3]
    print("My IP:", myIp);
    print("Ap IP:", apIp);
	
def myParser(data):
  global myStatus
  if(len(data) > 7):
    prefix = data[0:9]
    print("prefix=",prefix)
    if(prefix == b'getStatus'):
      print("GetStatus:", myStatus);
      tmp1 = "Status:" + myStatus;		
      sendMqtt(tmp1)
    elif(prefix == b'getClass'):
      print("GetClass:", myClass);
      tmp1 = "myClass:" + myClass;		
      sendMqtt(tmp1)
    elif(prefix == b'setStatus'):
      print("SetStatus:", data[10:11]);
      newVal = data[10:11]
      print("curStatus:", myStatus);
      print("newStatus:", newVal);
      if(newVal == b'1'):
        myStatus = "1"
        updateRelayStatus()
      elif(newVal == b'0'):
        myStatus = "0"
        updateRelayStatus()
      else:
        print("Syntax error: ", data)
  elif(data == b'getInfo'):
    print("Welcome to Home Node P")
    print("My id:", myId)
    print("My class:",myClass)
    print('Network config:', wlan.ifconfig())
    print("My Status:", myStatus)
  elif(prefix == b'getId'):
    print("GetId:", myId);
    tmp1 = "myId:" + myId;		
    sendMqtt(tmp1)
def updateRelayStatus():
    p0 = Pin(5, Pin.OUT)
    if(myStatus == "0"):
      p0.off()
    elif(myStatus == "1"):
      p0.on()
    else:
      print("UpdateRelayStatus Syntax error")
    
    
startMain();












