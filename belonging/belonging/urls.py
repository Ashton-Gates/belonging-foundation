from django.contrib import admin
from django.urls import path
from .views import register_view, login_view
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registration/', register_view, name='registration'),]
