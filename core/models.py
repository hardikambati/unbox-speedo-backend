from django.db import models


class SensorData(models.Model):
    """
    Sensor Data Model
    To store speed of sensor data device
    """

    speed     = models.FloatField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.timestamp} {self.speed}'