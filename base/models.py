from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.models import User
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from django.db.models import Q    
import uuid



class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        OWES = 'OU', _('Owes')
        OWEDBY = 'OB', _('Owed By')
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrower")
    lender= models.ForeignKey(User, on_delete=models.CASCADE, related_name="lender")
    type = models.CharField(max_length=2,choices=TransactionType.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
class Balance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE)
    owed = models.DecimalField(decimal_places=2, max_digits=5)
    owedby = models.DecimalField(decimal_places=2, max_digits=5)
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

