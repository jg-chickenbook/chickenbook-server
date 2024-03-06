from django.contrib import admin
from django.urls import path, include
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/login/', accounts.views.login, name='login'),
    path('api/accounts/', include('accounts.urls')),
]
