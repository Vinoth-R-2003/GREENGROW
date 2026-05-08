"""
URL configuration for app_core project.

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

from django.conf import settings
from django.conf.urls.static import static

# -- Auto-compile translations on server reload --
import sys
import os
try:
    locale_dir = os.path.join(settings.BASE_DIR, 'locale', 'ta', 'LC_MESSAGES')
    po_file = os.path.join(locale_dir, 'django.po')
    mo_file = os.path.join(locale_dir, 'django.mo')
    
    if os.path.exists(po_file) and not os.path.exists(mo_file):
        print("Compiling django.mo using built-in pure Python msgfmt...")
        import urllib.request
        msgfmt_url = "https://raw.githubusercontent.com/python/cpython/main/Tools/i18n/msgfmt.py"
        msgfmt_path = os.path.join(settings.BASE_DIR, 'msgfmt.py')
        
        if not os.path.exists(msgfmt_path):
            urllib.request.urlretrieve(msgfmt_url, msgfmt_path)
            
        # Add BASE_DIR to sys.path temporarily to import msgfmt
        if str(settings.BASE_DIR) not in sys.path:
            sys.path.insert(0, str(settings.BASE_DIR))
            
        import msgfmt
        msgfmt.make(po_file, mo_file)
        print("Successfully generated django.mo!")
except Exception as e:
    print(f"Failed to generate django.mo: {e}")
# ------------------------------------------------

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('market/', include('market.urls')),
    path('messages/', include('chat.urls')),
    path('garden/', include('garden.urls')),
    path('checks/', include('checks.urls')),
    path('', include('feed.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
