# -*- coding: utf-8 -*-
import logging
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SenderSerializer
from .helpers.mail_sender import mail_sender


class SendView(APIView):
    """This view is responsible for send email when operations are executed
    in neighborhood accout API.

    This view should receive some content by JSON format in
    request.data (POST):

    » user_id: positive integer field
    » user_name: the name os user
    » user_email: user email (nullable)
    » account: the user account id
    » value: value of operation
    » operation: debit or credit
    » message: a simple message that will sent in email body
    """

    def post(self, request, format=None):
        serializer = SenderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # logging the register
            data = serializer.data

            str_log = f'{data["when"]}: {data["operation"]} in account '
            str_log += f'by {data["user_name"]} - R$ {data["value"]}'

            logging.warning(str_log)

            # sending an email message after save register
            if request.data['user_email']:
                mail_sender(serializer.data)

        return Response(serializer.data)
