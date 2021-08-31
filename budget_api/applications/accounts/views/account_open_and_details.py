import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from ..serializers import FinancialAccountSerializer
from ..models import FinancialAccount


class AccountView(APIView):
    """This view only open an account for some user"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        """User can create an account only if is there no other for that
        user. This endpoint needs a DRF Token.

        Args:
            request (request): HTTP Request with request.user

        Returns:
            Account: If there's no error, a new account is returned
            Errors: If is there somo validation errors, they are returned
        """
        serializer = FinancialAccountSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            account.status = True
            account.save()
            log_str = '{}: User {} have created an financial account'.format(
                datetime.now(),
                request.user
            )
            logging.warning(log_str)
            return Response(FinancialAccountSerializer(account).data)
        else:
            return Response(data=serializer.errors)

    def get(self, request):
        """Only returns an account if authenticated user has one.
        Need to pass a DRF Token in Authorization header.

        Args:
            request (request): HTTP Request with request.user

        Returns:
            Account: Authenticated user account
        """
        try:
            account = FinancialAccount.objects.get(owner=request.user.id)
            return Response(FinancialAccountSerializer(account).data)
        except ObjectDoesNotExist:
            log_str = f'{datetime.now()}: User {request.user} requested '
            log_str += 'account but there\'s no one yet'

            logging.warning(log_str)
            return Response({'message': 'User has no account'})
