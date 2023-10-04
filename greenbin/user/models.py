import datetime
from django.db import models
from django.contrib.auth.models import User
from trash.models import Trash
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE, verbose_name='Usuario')
    processes = models.ManyToManyField(Trash, related_name="process", verbose_name='Procesos')
    profileimg = models.ImageField(upload_to='profile_images', default="blank-profile-picture.webp", verbose_name='Foto de Perfil')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Bio')
    location = models.CharField(max_length=30, blank=True, verbose_name='Ubicación')

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profileimg.path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profileimg.path)

    def total_weight(self):
        return sum([process.user_size for process in self.processes.all()])

# En gramos y ml
    def total_methane(self):
        return float(sum([process.user_size for process in self.processes.all()]) * 300)

# En gramos y ml
    def total_co2(self):
        return float(self.total_weight() *  8400)

# En gramos y ml (convertimos la masa en volumen)
    def total_km(self):
        return round(float(self.total_weight()/73.6),2)

    def total_air(self):
        return round(float(self.total_weight()/160),2)

    def total_energy(self):
        return round(float(self.total_weight()/4),2)

    def total_wood(self):
        return round(float(self.total_weight()/760),2)

    def total_hours(self):
        aux = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        for process in self.processes.all():
            aux += process.user_duration
        return aux
