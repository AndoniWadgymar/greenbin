from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse
from food.models import Food

# Create your models here.
class Trash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    start_date_formated = models.CharField(max_length=255,blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    user_duration = models.DurationField(blank=True, null=True)
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    SIZE_CHOICES = [
        (SMALL, "Small (100g-200g)"),
        (MEDIUM, "Medium (200g-350g)"),
        (LARGE, "Large (350g-500g)" ),
    ]
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default=MEDIUM,
    )
    user_size = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0), MaxValueValidator(500.0)])
    processed_size = models.FloatField(blank=True, null=True)
    foods = models.ManyToManyField(Food, related_name='food')
    on_process = models.BooleanField(default=False)

    class Meta:
        # Plural name of the elements
        verbose_name_plural = 'Trashes'

    def __str__(self) -> str:
        return "TP0" + str(self.id)

    def get_absolute_url(self):
        return reverse('trash:details', args=(self.id,))
