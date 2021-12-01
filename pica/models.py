from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .validators import validate_empty
from ckeditor_uploader.fields import RichTextUploadingField


class Company(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Company Code")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Company Name")

    def __str__(self):
        return self.name


class DivDept(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nama Divisi/Departemen")
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name


class Peserta(models.Model):
    nama = models.CharField(max_length=50, verbose_name="Nama Peserta", null=True,
                            blank=True)
    email = models.EmailField(null=True, blank=True, verbose_name="Email address")
    bod = models.BooleanField(default=False, verbose_name="Apakah masuk dalam list BOD?", null=True)

    def __str__(self):
        return self.nama


class Forum(models.Model):
    nama_forum = models.CharField(max_length=100, null=True, blank=True, validators=[validate_empty])
    keterangan = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nama_forum


class Signature(models.Model):
    title = models.CharField(max_length=20, null=True)
    nama_bod = models.CharField(max_length=30, null=True)
    presdir = models.BooleanField(default=False, null=True)
    lines = models.CharField(max_length=60, null=True, blank=True)
    signature2forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="forum2signature", null=True,
                                        blank=True, verbose_name="Forum")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        pj_nama = len(self.nama_bod)
        pj_title = len(self.title)
        tot_space = (30 - pj_nama) + (20 - pj_title)
        self.lines = "_" * (tot_space + 10)
        return super(Signature, self).save(*args, **kwargs)


class Meeting(models.Model):
    meeting_date = models.DateField(null=True, blank=True)
    meeting2forum = models.ForeignKey(Forum, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="forum2meeting", verbose_name="Meeting Forum")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    notulen = models.CharField(max_length=50, blank=True, null=True, verbose_name="Notulen Meeting")
    location = models.CharField(max_length=100, blank=True, null=True)
    meeting2peserta = models.ManyToManyField(Peserta, related_name="peserta2meeting", verbose_name="Peserta meeting")

    def __str__(self):
        return self.meeting2forum


class Topik(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('CLOSE', 'CLOSE')
    )
    topik2meeting = models.ForeignKey(Meeting, verbose_name="Meeting", null=True,
                                      related_name="meeting2topik", on_delete=models.SET_NULL)
    topik2divdept = models.ForeignKey(DivDept, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name="divdept2topik", verbose_name="Function/Divisi/Departemen")
    topik2company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="company2topik",
                                      verbose_name="Problem Owner")
    nama_topik = models.CharField(max_length=100, null=True, blank=True, verbose_name="Topik")
    problem = RichTextUploadingField(blank=True, null=True, verbose_name="Problem/Information")
    action = RichTextUploadingField(blank=True, null=True, verbose_name="Action")
    date_created = models.DateField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    due_date = models.DateField(null=True, blank=False, verbose_name="Due date")
    topik2user = models.ManyToManyField(User, verbose_name="Person in charge",
                                        related_name="user2topik")
    topik2peserta = models.ManyToManyField(Peserta, verbose_name="Known By",
                                           related_name="peserta2topik")
    status = models.CharField(max_length=8, choices=STATUS, default="OPEN", null=True)
    expired = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.nama_topik


class Activity(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('CLOSE', 'CLOSE')
    )
    activity2topik = models.ForeignKey(Topik, on_delete=models.CASCADE, null=True, related_name="topik2activity")
    date_activity = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                     verbose_name="Date Activity", default=timezone.now)
    keterangan = models.CharField(max_length=255, verbose_name="Activity/Action", null=True)
    activity2user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user2activity",
                                      verbose_name="PIC")
    due_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                verbose_name="New Due Date (If Any)")
    expired = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=8, choices=STATUS, default="OPEN", null=True)

    def __str__(self):
        return self.keterangan[:50]


class Pic(models.Model):
    nama = models.CharField(max_length=50, verbose_name="Nama Peserta", null=True,
                            blank=True)
    email = models.EmailField(null=True, blank=True, verbose_name="Email address")
    in_charge = models.BooleanField(default=False, verbose_name="In Charge", null=True)
    pic2topik = models.ManyToManyField(Topik, verbose_name="Topik", related_name="topik2pic")

    def __str__(self):
        return self.nama
