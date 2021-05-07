"""suitetool URL Configuration

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
from django.urls import path
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('loginuser',views.loginuser,name='login'),
    path('signupuser',views.signupuser,name='signup'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('logoutuser',views.logoutuser,name='logout'),
    path('import_doc_csv',views.import_doc_csv,name='import_doc_csv'),
    path('analysis',views.analysis,name='analysis'),
    path('Audioupload',views.Audioupload,name='Audioupload'),
    path('test',views.test,name='test')
]
