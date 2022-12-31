from django.db import models

# Create your models here.


class Owner(models.Model): 
    name = models.CharField(max_length=200, primary_key=True)
    contactInformation = models.CharField(max_length=200)
    closestViolation = models.FloatField(default=100)
    lastViolation = models.DateTimeField("last Violation")
    def str(self):
        time = self.lastViolation.strftime("%H:%M:%S")
        dist = int(self.closestViolation)
        
        return f"{self.name}, Closest Distance : {dist}m, Phone Number : {self.contactInformation}, Last Seen : {time}" 