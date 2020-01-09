import ESP8266WebServer, network, time, scale
from machine import Pin, PWM
ESP8266WebServer.begin(80)

sound=PWM(Pin(5))
r = PWM(Pin(12))
g = PWM(Pin(13))
b = PWM(Pin(15))
r.duty(0)
g.duty(0)
b.duty(0)
light = 200

def setDuty(rl,gl,bl):
    r.duty(rl)
    g.duty(gl)
    b.duty(bl)

# note=(100, 200, 300, 400, 500)
duration = 4  #聲音長度
def tone(sound,note,duration):
    sound.freq(note)
    sound.duty(512)
#     time.sleep_ms(duration)
#     sound.deinit()
    
def playsound(sound,note):
    j = 0
    d=int(1000/duration)
    p=int(d*0.5)
    tone(sound, note, d)
#     time.sleep_ms(p)

def handleCmd(socket, args):
    if 'led' in args:
        if args['led'] == 'sad':
            setDuty(0,light,0)
            playsound(sound, scale.C5)
        elif args['led'] == 'angry':
            setDuty(0,0,light)
            playsound(sound, scale.D5)
        elif args['led'] == 'neutral':
            setDuty(light,0,0)
            playsound(sound, scale.E5)
        elif args['led'] == 'happy':
            setDuty(light,light,0)
            playsound(sound, scale.F5)
        elif args['led'] == 'surprised':
            setDuty(0,light,light)
            playsound(sound, scale.G5)
        elif args['led'] == 'close':
            setDuty(0,0,0)
            sound.deinit()
        ESP8266WebServer.ok(socket, "200", "OK")
    else:
        ESP8266WebServer.srr(socket, "400", "ERR")
            

ESP8266WebServer.onPath("/cmd", handleCmd)
ESP8266WebServer.setDocPath("/rgbweb")

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("HITRON-9820-2.4G","0988346578") #WiFi更改處
while not sta_if.isconnected():
    pass
print("WiFi Connected")

print(sta_if.ifconfig()[0])
while True:
    ESP8266WebServer.handleClient()
    
#print(sta_if.ifconfig()[0])