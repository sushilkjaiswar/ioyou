from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from base.models import Transaction
from django.contrib.auth.models import User

class TransactionSerilizer(ModelSerializer):
    borrower =  PrimaryKeyRelatedField(queryset=User.objects.all())
    lender =  PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Transaction
        fields = '__all__'
        
        
class UserSerailizer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username']