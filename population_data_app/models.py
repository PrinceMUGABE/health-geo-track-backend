# models.py
from django.db import models
from django.conf import settings
from django.forms import ValidationError

class PopulationData(models.Model):
    SOCIOECONOMIC_STATUS_CHOICES = [
        ('LOW', 'Low Income'),
        ('MIDDLE', 'Middle Income'),
        ('HIGH', 'High Income')
    ]
    
    district = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    total_population = models.IntegerField()
    male_population = models.IntegerField()
    female_population = models.IntegerField()
    children_under_5 = models.IntegerField()
    youth_population = models.IntegerField()  # Ages 15-24
    adult_population = models.IntegerField()  # Ages 25-64
    elderly_population = models.IntegerField()  # Ages 65+
    population_density = models.FloatField()  # People per square kilometer
    socioeconomic_status = models.CharField(max_length=20, choices=SOCIOECONOMIC_STATUS_CHOICES)
    unemployment_rate = models.FloatField()
    literacy_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['district', 'sector']
        
    def clean(self):
        # Validate total population matches demographic breakdowns
        total_by_gender = self.male_population + self.female_population
        total_by_age = (self.children_under_5 + self.youth_population + 
                       self.adult_population + self.elderly_population)
                       
        if self.total_population != total_by_gender:
            raise ValidationError('Total population must match sum of male and female population')
        if self.total_population != total_by_age:
            raise ValidationError('Total population must match sum of age groups')
            
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.district} - {self.sector} Population Data"