import requests
import xml.etree.ElementTree as ET
import math
from datetime import *
from dateutil import parser, relativedelta
from hello.models import Owner
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def violators():

    while True: #Running in a seperate thread always on if the server is on

         #get drone data
        url = 'https://assignments.reaktor.com/birdnest/drones'

        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(url)


        

        
        if response.status_code == 200:
            root = ET.fromstring(response.text) #make xml element tree

            time = root.find("capture").get("snapshotTimestamp") # find the time of the sample
            if time != None:
                time = parser.parse(time) # change time to datetime

                

                for owner in Owner.objects.all(): #delete any users in database with longer that 10min last violation
                    if relativedelta.relativedelta(time,owner.lastViolation).minutes >= 10 :
                        owner.delete()
                    
                drones = root.find("capture").findall("drone") # find all individual drones
                for drone in drones: #calculate drone distance to middle and if its less than 100m update user in database or create one
                    posX = float(drone.find("positionX").text)
                    posY = float(drone.find("positionY").text)
                    dist = math.sqrt((posX-250000)**2 + (posY-250000)**2 )
                    distM = dist/1000
                    if distM<100:
                        serialNumber = drone.find("serialNumber").text
                        request = requests.get('https://assignments.reaktor.com/birdnest/pilots/' + serialNumber)
                        if request.status_code == 200:
                            json = request.json()
                            if "firstName" and "lastName" and "phoneNumber" in json:
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
                            
                        
        sleep(2)
