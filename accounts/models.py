from django.db import models
from django.contrib.auth.models import User
from pica.models import DivDept


class Profile(models.Model):
    GENDER = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan')
    ]
    BOD = [
        ('Y', 'BOD'),
        ('N', 'Non BOD')
    ]
    profile2user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="user2profile")
    birth_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    photo = models.ImageField(null=True, default='images/User1.svg',
                              blank=True, upload_to="images/")
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name="Gender")
    mobile_number = models.CharField(max_length=12, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    profile2divdept = models.ForeignKey(DivDept, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Div/Dept")
    bod = models.CharField(max_length=1, choices=BOD, verbose_name="Status BOD ?")

    def __str__(self):
        return self.profile2user.username
