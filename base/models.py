from django.db import models

# Create your models here.

class Drone(models.Model):
    serial_number = models.CharField(max_length=20, unique = True)
    closest_approach = models.FloatField(max_length=20)
    last_seen = models.CharField(max_length=20)

    def __str__(self):
        return self.serial_number

class Pilot(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Not currently used.
class DroneFlight(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.drone.name} flight'

# Not currently used.
class DroneFlightDataPoint(models.Model):
    flight = models.ForeignKey(DroneFlight, on_delete=models.CASCADE)
    pos_x = models.FloatField(max_length=20)
    pos_y = models.FloatField(max_length=20)
    # nest_distance = functions.calc_distance(pos_x, pos_y)



