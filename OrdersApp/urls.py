"""OrdersApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from Orders_App import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    path('admin/', admin.site.urls),
    path('order/', views.OrderList.as_view(), name="order-list"),
    path('order/<int:pk>', views.OrderDetail.as_view(), name="order-detail"),
    path('order/<int:pk>/cancel', views.OrderCancel.as_view(), name="order-cancel"),
    path('review/<int:pk>', views.ReviewDetails.as_view(), name="review-detail"),
    path('order/verifyotp/<int:pk>', views.VerifyOTP.as_view(), name="OTP-verification")
]

urlpatterns = format_suffix_patterns(urlpatterns)
