from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date


class Client(models.Model):
    """
    Modèle des clients de Epic Event
    """
    CHOICES = [
        ("prospect", "prospect"),
        ("client", "client")
    ]

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=14, default="not available")
    mobile = models.CharField(max_length=14, default="not available")
    company_name = models.CharField(max_length=40, default="private individual")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    # au lieu de (default=timezone.now)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='sales_contact',
        blank=True,
        null=True
        # null=True autorise l'absence de commercial désigné (départ du commercial en charge par exemple)
        # TODO il faudrait que ça envoie un signal/une alerte au management pour assigner qq'un
    )
    status = models.CharField(
        max_length=8,
        choices=CHOICES,
        default="prospect"
    )

    def save(self, *args, **kwargs):
        # + try/except:
        # # TODO vérifier la tournure pour éviter 2 fois le même client (et l'appliquer à User après check)
        # if not Client.objects.filter(first_name=self.first_name).filter(last_name=self.last_name).exists():
        self.last_name = self.last_name.upper()
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"{self.first_name} {self.last_name} ( {self.status}: id. {self.id} )"


class Contract(models.Model):
    """Lors de l'enregistrement du contrat, un évènement ayant pour nom l'objet du contrat est créé,
    Le management peut alors lui attribuer un chargé de support.
    """
    object = models.CharField(max_length=120, unique=True)
    date_signature = models.DateField(default=date.today)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        # à changer pour RESTRICT après les tests pour protéger les contrats
    )

    class Meta:
        # ensures we don't get multiple instances
        # for unique user-project pairs
        unique_together = ('client', 'object',)

    def __str__(self):
        return f"{self.object}(contract {self.id})"

    def save(self, *args, **kwargs):
        """
        surcharge de la fonction save() pour enregistrer
        un évenement lié au contrat
        """
        # TODO : si un client 'prospect' signe un contrat, il devient 'client' xxx

        # à ce moment le event_id n'existe pas
        old_event_id = self.id
        # puis on le créé avec le super().save
        super().save(*args, **kwargs)
        if self.client.status == "prospect":
            self.client.status = "client"  # TODO prospect devient client (ne marche pas comme çà)
        if old_event_id is None:
            Event.objects.create(name=self.object, contract=self, client=self.client)


class Event(models.Model):
    """"""
    name = models.CharField(max_length=120, unique=True)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=120)
    description = models.TextField(max_length=2048, blank=True)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
    )
    support = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='support_contact',
        blank=True,
        null=True
        # null=True autorise l'absence de support désigné lors de la création (contrat enregistré)
        # TODO il faudrait que ça envoie un signal/une alerte au management pour assigner qq'un
    )
    contract = models.ForeignKey(
        to=Contract,
        on_delete=models.CASCADE,
        related_name='event'
    )

    def __str__(self):
        return f"{self.name}(event {self.id})"
