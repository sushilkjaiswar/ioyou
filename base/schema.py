import graphene
from graphene_django import DjangoObjectType
from base.models import Transaction
from django.contrib.auth.models import User
from datetime import datetime


class UserType(DjangoObjectType):
    class Meta:
        model = User

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("id", "borrower", "lender", 'amount', 'expiry')


class Query(graphene.ObjectType):
    expired_iou = graphene.List(TransactionType)


    def resolve_expired_iou(root, info):
        return Transaction.objects.filter(expiry__lt=datetime.today())


schema = graphene.Schema(query=Query)