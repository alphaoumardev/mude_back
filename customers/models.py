from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

SEX = (("Male", "Male"),
       ("Female", "Female"),
       ("Secret", "Secret"),)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(blank=True, max_length=11, null=True, unique=True)
    gender = models.CharField(max_length=10, null=True, choices=SEX)
    avatar = models.ImageField(upload_to="mudi", null=True, blank=True,
                               default="https://res.cloudinary.com/diallo/image/upload/v1647154137/8_fncc3c.jpg")

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=CustomerProfile)
# def user_profile_receiver(sender, instance=None, created=False, *args, **kwargs):
#     if created:
#         CustomerProfile.objects.create(user=instance)


# post_save.connect(user_profile_receiver, sender=CustomerProfile)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Devcom  password reset Notice"),
        # message:
        email_plaintext_message,
        # from:
        "devalphaoumar@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)

class ContactUs(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(blank=True, max_length=30, null=True)
    content = models.TextField()

    def __str__(self):
        return self.subject
