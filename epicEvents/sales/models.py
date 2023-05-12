from django.db import models
from django.conf import settings


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone = models.CharField(max_length=20, default=None, blank=True)
    company = models.CharField(max_length=250, default=None)
    dateCreated = models.DateField(auto_now_add=True, null=True)
    dateUpdated = models.DateField(auto_now=True, null=True)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                      related_name='sale_clients')

    class Meta:
        db_table = 'client'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                      related_name='sale_contracts')
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='contract_client', blank=False, )
    dateCreated = models.DateField(auto_now_add=True, null=True)
    dateUpdated = models.DateField(auto_now=True, null=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(blank=False)
    paymentDue = models.DateField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'contract'

    def __str__(self):
        return f" {self.client} {self.amount} {self.sales_contact}"

    def save(self, *args, **kwargs):
        self.sales_contact = self.client.sales_contact
        super(Contract, self).save(*args, **kwargs)


class Event(models.Model):
    CHOICES = (
        ('1', 'Booked'),
        ('2', 'In progress'),
        ('3', 'Done')
    )
    event_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name='event_client')
    dateCreated = models.DateField(auto_now_add=True, null=True)
    dateUpdated = models.DateField(auto_now=True, null=True)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='support_contracts')
    eventStatus = models.CharField(max_length=10, blank=False, choices=CHOICES, default="1")
    attendes = models.IntegerField(blank=True, null=True, default=0)
    eventDate = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return f"{self.eventDate} {self.attendes} {self.support_contact}"
