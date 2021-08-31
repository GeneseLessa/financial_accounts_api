# -*- coding: utf-8 -*-
import logging
from django.core.mail import send_mail
from django.conf import settings
import decimal

legends = {
    'debit': u'Débito',
    'credit': u'Crédito'
}


def mail_sender(data):
    value = round(decimal.Decimal(data["value"]), 2)

    message = f'Operação de {legends[data["operation"]]} realizada no valor '
    message += f'de R$ {value} por {data["user_name"]}'

    subject = u'Movimentação em sua conta'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data['user_email']]

    send_mail(subject, message, email_from,
              recipient_list, fail_silently=False)

    str_log = f'{data["when"]}: {data["operation"]} '
    str_log += f'for {data["user_name"]} - R$ {data["value"]} - email sent'

    logging.warning(str_log)
