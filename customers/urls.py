from .views import RegisterAPI, UserAPI, ChangePasswordView, get_customer_profile, contact_us
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    path('signup/', RegisterAPI.as_view(), name='register'),
    path('signin/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('loaduser/', UserAPI.as_view(), name="user"),
    path('customer-profile/', get_customer_profile, name="user"),

    path('contact-us/', contact_us, name="contact-us"),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

