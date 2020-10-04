from django.db import models

from django.db import models

class Echipa(models.Model):
    nume = models.CharField(max_length=250)
    antrenor = models.CharField(max_length=250)
    valoare = models.IntegerField()

class Jucator(models.Model):
    nume = models.CharField(max_length=250)
    valoare = models.IntegerField()
    echipa = models.ForeignKey("Echipa", on_delete=models.CASCADE)

class Meci(models.Model):
    etapa = models.IntegerField()
    gazda = models.CharField(max_length=50)
    oaspete = models.CharField(max_length=50)
    scor = models.CharField(max_length=250)

class Clasament(models.Model):
    etapa = models.IntegerField()
    echipa = models.CharField(max_length=250)
    victorii = models.IntegerField()
    egaluri = models.IntegerField()
    infrangeri = models.IntegerField()
    goluri_primite = models.IntegerField()
    goluri_inscrise = models.IntegerField()
    punctaj = models.IntegerField()
