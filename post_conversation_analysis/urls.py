"""
URL configuration for post_conversation_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponse
from your_app import views


# ✅ Define the home view
def home(request):
    return HttpResponse("✅ Conversation Analyzer is running successfully on Render!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),  # replace 'your_app' with your actual app name
    path('', home),  # ✅ homepage route
]



    


