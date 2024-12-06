"""
URL configuration for library1_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from main import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/stored', views.books_stored, name='books_stored'),
    path('books/borrowed', views.books_borrowed, name='books_borrowed'),
    path('books/fined', views.books_fined, name='books_fined'),
    path('books/provided', views.books_provided, name='books_provided'),
    path('distribute/<int:id>', views.distribute_book, name='distribute_book'),
    path('return/<int:id>', views.return_book, name='return_book'),
    path('admin/', admin.site.urls),
]
