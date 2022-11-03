
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from base.models import Transaction
from .serializers import TransactionSerilizer, UserSerailizer
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
import json
from django.db import IntegrityError

@api_view(['POST'])
def add_user(request):
    """
    Add new user  to the system
    {"user":"bob"}
    """     
    payload = request.data
    try:
        t = User(username=payload.get('user').lower())
        t.save()
        serializer = UserSerailizer(t)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except IntegrityError as e: 
        
        if 'unique constraint failed' in e.args[0].lower(): # or e.args[0] from Django 1.10
            return Response('User already exists', status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except Exception as ex:
        print(ex)
        return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST'])
def add_transactions(request):
    # ----- YAML below for Swagger -----
    """
    Add transaction of borroing and lending
    
    {"lender":"bob","borrower":"adam","amount":5.25, "expiration":"2022-11-10"}
    """ 
    
    payload = request.data
    borrower =  request.data.get('borrower')
    lender =  request.data.get('lender')
    amount =  float(request.data.get('amount'))
    expiration =  request.data.get('expiration') 
    borrower_obj = User.objects.filter(username=borrower)[0]
    lender_obj = User.objects.filter(username=lender)[0]
    
    try:
        t = Transaction(borrower=borrower_obj, lender=lender_obj, amount= amount, expiry=expiration)
        t.save()
        serializer = TransactionSerilizer(t)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

        
    except Exception as ex:
        print(ex)
        return Response('Unknown Error Occured', status=status.HTTP_400_BAD_REQUEST)
         

@api_view(['GET'])
def settle_up(request):
    # ----- YAML below for Swagger -----
    """
    Fetch transaction details of the users who borrowed or lending details
    
    {"lender":"bob","borrower":"adam","amount":5.25, "expiration":"2022-11-10"}
    """ 
    try:
        payload = json.loads(request.query_params.get('payload'))

        
        #  ToDo: Following section can be improvide in better way
        # Fetch users from db as per requested list        
        users = User.objects.filter(username__in=[ user.lower() for user in payload.get("users")]).order_by('username')

        # Compute how many amount is owes the user  
        owes = [ { "name": user.username.title(), "owes":  {User.objects.get(pk=lender.get('lender')).username: lender.get('amount') \
                                                            for lender in \
                                                            Transaction.objects.filter(borrower__username=user.username).values( 'lender').annotate(amount=Sum('amount'))} }  \
                for user in users ]
        
        # Compute how many amount is owed_by the user 
        owedby = [ { "name": user.username.title(), "owed_by":  { User.objects.get(pk=borrower.get('borrower')).username: borrower.get('amount') \
                                                                 for borrower in Transaction.objects.filter(lender__username=user.username).values( 'borrower').annotate(amount=Sum('amount'))} }  \
                  for user in users ]
        
        
        # Balaance calculation 
        balance_owes = [   Transaction.objects.filter(borrower__username=user.username).aggregate(balance_owes=Coalesce(Sum('amount'), 0.0, output_field=DecimalField()))  for user in users]
        balance_owedby = [   Transaction.objects.filter(lender__username=user.username).aggregate(balance_owedby=Coalesce(Sum('amount'), 0.0, output_field=DecimalField()))  for user in users]
        balance = [ {'balance':item[1].get('balance_owedby') - item[0].get('balance_owes')} for item in list(zip( balance_owes, balance_owedby))]
        
        
        # Merging for final results
        results = [ {**owed, **owedby, **balance} for owed, owedby, balance in list(zip(owes,owedby,balance))]

        return Response(results, status=status.HTTP_201_CREATED)
    
    except ValueError as ex:
        print(ex)
        return Response("Bad incoming request", status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as ex:
        print(ex)
        return Response("Unkown error occured", status=status.HTTP_400_BAD_REQUEST)
    

