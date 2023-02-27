import paho.mqtt.client as clientlib
import paho.mqtt.publish as publib
import ssl

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print("Publisher failed to connect to broker")
    else:
        print("Publisher successfully connected to broker")
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from broker")
    else:
        print("Disconnected from broker successfully")
    
def on_publish(client, userdata, mid):
    print("Published message sent to broker (QOS = 0)") # may want to bump to qos = 1 to guarantee delivery on_publish
    
pathtocerts = "/home/ubuntu/certs/"    
pub = clientlib.Client()
pub.tls_set(ca_certs=pathtocerts + "mosquitto.org.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=2, ciphers=None)
pub.on_connect = on_connect
pub.on_disconnect = on_disconnect
pub.on_publish = on_publish

# socket.gethostbyname expects a host name and not a URL
pub.connect("test.mosquitto.org", port=8883, keepalive=60, bind_address="") 
pub.loop_start()

counter = 5
while counter > 0: 
    pub.publish(topic="my_very_unique_topic", payload="Hello World!")
    counter-=1
    
pub.loop_stop()
