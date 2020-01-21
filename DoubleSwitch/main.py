import network
import socket
from machine import Pin
import time
import sys

myId = "hnp002"
myClass = "02" 
apName = ""  // update here
apPass = "" // update here
apIp = ""
myIp = ""
myUdpPort = 8266
socketUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketUdp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
wlan = network.WLAN(network.STA_IF)

myStatus1 = "0"
myStatus2 = "0"
	
def startMain():
  updateRelayStatus()
  print("");
  print("Welcome to Home Node P");
  print("Configuring connection...");
  connectToWifi();
  print("Configuring udp...");
  setUdpListener()

	
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

def setUdpListener():
  print("My IP:", myIp);
  print("My udp port:", myUdpPort);
  socketUdp.bind((myIp,myUdpPort))
  print('Ready for data....')
  while True:
    data,addr=socketUdp.recvfrom(1024)
    print('Received:',data,'from',addr)
    myParser(data)
def sendData(data):
  socketUdp.sendto(str(data),(apIp,myUdpPort))
  tmpstr = "SendData to: " + apIp + " data: " + data;
  print(tmpstr);
	
def myParser(data):
  global myStatus1
  global myStatus2
  if(len(data) > 7):
    prefix = data[0:9]
    print("prefix=",prefix)
    if(prefix == b'getStatus'):
      print("GetStatus Status1:", myStatus1);
      print("GetStatus Status2:", myStatus2);
      tmp1 = "Status1:" + myStatus1 + "Status2:" + myStatus2;		
      sendData(tmp1)
    elif(prefix == b'getId'):
      print("GetId:", myId);
      tmp1 = "myId:" + myId;		
      sendData(tmp1)
    elif(prefix == b'getClass'):
      print("GetClass:", myClass);
      tmp1 = "myClass:" + myClass;		
      sendData(tmp1)
    elif(prefix == b'setStatus'):
      print("SetStatus Status1:", data[10:11]);
      print("Status2:", data[11:12]);
      newVal1 = data[10:11]
      newVal2 = data[11:12]
      print("curStatus Status1:", myStatus1);
      if(newVal1 == b'1'):
        myStatus1 = "1"
      elif(newVal1 == b'0'):
        myStatus1 = "0"
      else:
        print("Syntax error: ", data)
      if(newVal2 == b'0'):
        myStatus2 = "0"
      elif(newVal2 == b'1'):
        myStatus2 = "1"
      updateRelayStatus()
  elif(data == b'getInfo'):
    print("Welcome to Home Node P")
    print("My id:", myId)
    print("My class:",myClass)
    print('Network config:', wlan.ifconfig())
    print("My Status Status1:", myStatus1)
    print("My Status Status2:", myStatus2)
		
def updateRelayStatus():
    p0 = Pin(5, Pin.OUT)
    p1 = Pin(4, Pin.OUT)
    if(myStatus1 == "0"):
      p0.off()
    elif(myStatus1 == "1"):
      p0.on()
    else:
      print("UpdateRelayStatus Syntax error1")
    if(myStatus2 == "0"):
      p1.off()
    elif(myStatus2 == "1"):
      p1.on()
    else:
      print("UpdateRelayStatus Syntax error2")
    
startMain();







