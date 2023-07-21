"""NCC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
import core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('postContest/', include('postContest.urls')),
]

from django.conf.urls import handler400, handler403, handler404, handler500
# 404 not found error
# handler404 = core.views.errors_404
# # 500 internal server error
# handler500 = core.views.errors_500
# # # 400 bad request error
# handler400 = core.views.errors_400
# # 403 permission denied error
# handler403 = 'core.views.error_403'

