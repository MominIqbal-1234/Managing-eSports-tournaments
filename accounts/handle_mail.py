from django.core.mail import send_mail
import random
class HandleMail:
    def generateRandomNumber(self):
        return random.randint(0, 151214)
    def sendVerifyMail(request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username,domain = email.split("@")
        request.session["full_name"] = full_name
        request.session["email"] = email
        request.session["password"] = password
        request.session["username"] = username
        request.session["otp"] = random.randint(0, 151214)
        subject = 'shortURL Team Verification Mail'
        message = f'Your Verification Code is : {request.session["otp"]}'
        email_from = "writeflix@mefiz.com"
        send_mail(subject, message, email_from,
                  [email], fail_silently=False)