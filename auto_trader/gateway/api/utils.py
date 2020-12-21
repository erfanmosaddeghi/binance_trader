
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import smtplib
from gateway.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes
"""
Genrating User Verification Token To send into the Email
"""
class emailVerifi(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active) +text_type(user.pk) +text_type(timestamp))

    def send_mail(request):
        try:
            # Sending Email Part
            username = request.POST.get('username')
            user = User.objects.get(username__exact=username)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            sending_userGmail_address = 'erfan.mosaddeghi@gmail.com'
            gmail_password = ''
            server.login(sending_userGmail_address,gmail_password)
            # Validation link Create
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('gateway:verification_account',kwargs={'uid':uid,'token':email_token.make_token(user)})

            active_url = 'http://'+ domain + link
            # Email Title and body to Send
            subject = 'Email verification'
            body = 'Hi Please use this link to activate your account\n'+active_url

            Massage = f'Subject:{subject}\n\n{body}'

            server.sendmail(
                f'{sending_userGmail_address}',
                f'{user.email}',
                Massage
            )
            server.quit()
        except smtplib.SMTPResponseException as e:
            return False, e


email_token = emailVerifi()


