import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.exceptions import ObjectDoesNotExist
import decimal
from datetime import datetime

from ..serializers import FinancialAccountSerializer
from ..models import FinancialAccount, MovementRegister
from applications.users.models import User
from ..helpers.call_sender import sender


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
            done = False

            def debit(value):
                if account.balance - value >= 0:
                    account.balance -= value
                    return True
                else:
                    return False

            def credit(value):
                account.balance += value if value > 0 else 0
                return value > 0

            if operation == 'debit':
                done = debit(value)
                if not done:
                    return Response({
                        'message': 'Not enough money',
                        'account': FinancialAccountSerializer(account).data
                    })
            if operation == 'credit':
                done = credit(value)

            if done:
                account.save()

                # registering account movement
                MovementRegister.objects.create(
                    account=account,
                    movement_kind=operation,
                    who=User.objects.get(pk=request.user.id),
                    value=value
                )

                # passing the external call for sender helper
                sender(account, data)

            # logging operation
            log_str = '{}: user {} realized a {} of R$ {}'.format(
                datetime.now(),
                request.user,
                operation,
                round(value, 2)
            )
            logging.warning(log_str)

            return Response(FinancialAccountSerializer(account).data)

        except ObjectDoesNotExist:
            logging.warning(f'User {request.user} has no financial account')
            return Response({'message': 'User has no financial account'})
