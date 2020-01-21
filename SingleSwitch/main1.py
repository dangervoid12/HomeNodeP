import network
import socket
from machine import Pin
import time
import sys

myId = "hnp001"
myClass = "01" 
apName = ""  // update here
apPass = "" // update here
apIp = ""
myIp = ""
myUdpPort = 8266
socketUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketUdp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
wlan = network.WLAN(network.STA_IF)

myStatus = "0"

	
def startMain():
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
  global myStatus
  if(len(data) > 7):
    prefix = data[0:9]
    print("prefix=",prefix)
    if(prefix == b'getStatus'):
      print("GetStatus:", myStatus);
      tmp1 = "Status:" + myStatus;		
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
		
def updateRelayStatus():
    p0 = Pin(5, Pin.OUT)
    if(myStatus == "0"):
      p0.off()
    elif(myStatus == "1"):
      p0.on()
    else:
      print("UpdateRelayStatus Syntax error")
    
    
startMain();







