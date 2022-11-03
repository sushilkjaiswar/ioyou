import pytest

from django.contrib.auth.models import User
from base.models import Transaction
from datetime import datetime

@pytest.mark.django_db
def test_user_create():
    user = User(username= 'test')
    user.save()
    
    assert User.objects.filter(pk=user.id).count() == 1
    
@pytest.mark.django_db
def test_transaction_create():
    bob = User(username= 'bob')
    bob.save()
    adam = User(username= 'adam')
    adam.save()
    trans = Transaction(borrower= bob, lender=adam, amount=12.00, expiry=datetime.utcnow())
    trans.save()
    
    assert Transaction.objects.filter(pk=trans.id).count() == 1 and trans.borrower.id == bob.id and trans.lender.id == adam.id