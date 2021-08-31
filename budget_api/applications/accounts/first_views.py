from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.exceptions import ObjectDoesNotExist
import decimal

from .serializers import FinancialAccountSerializer
from .models import FinancialAccount


class AccountView(APIView):
    """This view only open an account for some user"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        """User only can open an account if there's no other for that user"""
        serializer = FinancialAccountSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            return Response(FinancialAccountSerializer(account).data)
        else:
            return Response(data=serializer.errors)

    def get(self, request, id=None):
        """Only returns an account if the user hasn't one"""
        try:
            account = FinancialAccount.objects.get(owner=request.user.id)
            return Response(FinancialAccountSerializer(account).data)
        except ObjectDoesNotExist:
            return Response({'message': 'User has no account'})


class AccountMovement(APIView):
    """This CBV just manage the user account movements"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        data = request.data

        try:
            account = FinancialAccount.objects.get(owner=request.user.id)
            value = decimal.Decimal(data['value'])
            operation = data['operation']

            def debit(value):
                if account.balance - value >= 0:
                    account.balance -= value
                    return True
                else:
                    return False

            def credit(value):
                account.balance += value if value > 0 else 0

            if operation == 'debit':
                debit_result = debit(value)
                if not debit_result:
                    return Response({
                        'message': 'Not enough money',
                        'account': FinancialAccountSerializer(account).data
                    })
            else:
                credit(value)

            account.save()
            return Response(FinancialAccountSerializer(account).data)

        except ObjectDoesNotExist:
            return Response({'message': 'User has no financial account'})
