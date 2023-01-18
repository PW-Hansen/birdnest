from django.db import models

# Create your models here.

class Drone(models.Model):
    serial_number = models.CharField(max_length=20, unique = True)
    closest_approach = models.FloatField(max_length=20)
    last_seen = models.DateTimeField()

    class Meta:
        ordering = ['last_seen']

    def __str__(self):
        return self.serial_number

class Pilot(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name