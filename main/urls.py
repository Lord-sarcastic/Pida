from django.urls import path
from . import views, forms
app_name = 'main'
urlpatterns = [
    path('sign-in', views.SignInView.as_view(), name='signin'),
    path('', views.SignInView.as_view(), name='signin'),
    path('sign-up', views.SignUpView.as_view(), name='signup'),
    path('secure-digit/', views.MainView.as_view(), name='main'),
]