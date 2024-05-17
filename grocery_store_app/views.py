from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core import paginator as django_paginator, exceptions
from rest_framework import viewsets, permissions, authentication
from django.contrib.auth import decorators, mixins

from .serializers import CategorySerializer, ProductSerializer, PromotionSerializer, ReviewSerializer
from .models import Category, Product, Promotion, Review, Client
from .forms import RegistrationForm

from typing import List
from .models import CategoryToCategory


class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [MyPermission]
    return ViewSet

CategoryViewSet = create_viewset(Category, CategorySerializer)
ProductViewSet = create_viewset(Product, ProductSerializer)
PromotionViewSet = create_viewset(Promotion, PromotionSerializer)
ReviewViewSet = create_viewset(Review, ReviewSerializer)

def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('homepage')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors},
    )