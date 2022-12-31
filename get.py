import requests
import xml.etree.ElementTree as ET
import math
from datetime import *
from datetime import timedelta
from dateutil import parser, relativedelta
from hello.models import Owner
import time as tiima



def violators():
    while True:
        response = requests.get('https://assignments.reaktor.com/birdnest/drones')

        print("doing things")
        root = ET.fromstring(response.text)

        time = root.find("capture").get("snapshotTimestamp")

        time = parser.parse(time)
        drones = root.find("capture").findall("drone")
        violators = []
        for owner in Owner.objects.all():
            if relativedelta.relativedelta(time,owner.lastViolation).minutes >= 10 :
                owner.delete()
            

        for drone in drones: 
            posX = float(drone.find("positionX").text)
            posY = float(drone.find("positionY").text)
            dist = math.sqrt((posX-250000)**2 + (posY-250000)**2 )
            distM = dist/1000
            if distM<100:
                SN = drone.find("serialNumber").text
                json = requests.get('https://assignments.reaktor.com/birdnest/pilots/' + SN).json()
                name = json["firstName"] + " " + json["lastName"] 
                contactInformation = json["phoneNumber"]
                s = Owner.objects.all().filter(name = name).first()
                if s != None: 
                    s.closestViolation = min(s.closestViolation,distM)
                    s.lastViolation = time
                    s.save()
                else:
                    q = Owner(name = name, contactInformation = contactInformation, closestViolation = distM, lastViolation = time)
                    q.save()
                

                violators.append((SN,distM))
                
                tiima.sleep(1)
