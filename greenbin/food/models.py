from django.db import models
# Import the user Class
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import now
from PIL import Image
# Create your models here.

# We create a CATEGORY MODEL, based on a Django Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    # Define the class Meta for our DB and admin page
    class Meta:
        # The ordering of the elements
        ordering = ['name']
        # Plural name of the elements
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name

# We create a food Model, based on a Django Model
class Food(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    name_eng = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre Ingles')
    weight = models.IntegerField(blank=False, null=False, verbose_name='Peso')
    # We need to install Pillow library to save images (resize, save and more)
    image = models.ImageField(upload_to='food_images', verbose_name='Imagen')
    category = models.ForeignKey(Category, related_name='foods', on_delete=models.CASCADE, verbose_name='Categoría')
    created_by = models.ForeignKey(User, related_name='foods', on_delete=models.CASCADE, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)