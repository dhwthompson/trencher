"""trencher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from dish import views as dish_views
from plan import views as plan_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('', plan_views.index, name='index'),
    path('dates', plan_views.dates, name='dates'),
    path('shop', plan_views.shop, name='shop'),
    path('order', plan_views.order, name='order'),
    path('dishes/new', dish_views.new, name='new_dish'),
    path('meals/<int:pk>/complete', plan_views.complete, name='complete'),
    path('meals/<int:pk>/cancel', plan_views.cancel, name='cancel'),
    path('meals/<int:pk>/delete', plan_views.delete, name='delete'),
]
