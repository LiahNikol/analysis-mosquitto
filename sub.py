import paho.mqtt.client as clientlib
import paho.mqtt.subscribe as sublib
import ssl

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print("Subscriber failed to connect to broker")
    else:
        print("Subscriber successfully connected to broker")
        client.subscribe(topic="my_very_unique_topic") 
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from broker")
    else:
        print("Disconnected from broker successfully")
    
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscription acknowledged by broker (QOS = 0)")
   
def on_message(client, userdata, message): 
    print("Message received from publisher on topic {}: {}".format(message.topic,  message.payload))
    
pathtocerts = "/home/ubuntu/certs/"         
sub = clientlib.Client()
sub.tls_set(ca_certs=pathtocerts + "mosquitto.org.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=2, ciphers=None)
sub.on_connect = on_connect
sub.on_disconnect = on_disconnect
sub.on_subscribe = on_subscribe
sub.on_message = on_message

# socket.gethostbyname expects a host name and not a URL
sub.connect("test.mosquitto.org", port=8883, keepalive=60, bind_address="")
sub.loop_forever()