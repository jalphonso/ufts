from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from ufts.settings import CLASSIFICATION_TEXT_SHORT


urlpatterns = [
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/img/favicon.ico')),
    path('', include('home.urls')),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    # All the password urls come from django.contrib.auth.urls so keep this line before others so the override works
    path('users/', include('django.contrib.auth.urls')),
    # The name param is used in the templates/base.html file so it needs to match here to complete the override
    path('password_reset/', auth_views.PasswordResetView.as_view(extra_email_context=dict(email_template_name="registration/password_reset_email.txt",
                                                                                          html_email_template_name="registration/password_reset_email.html",
                                                                                          classification=settings.CLASSIFICATION_TEXT,
                                                                                          classification_short=settings.CLASSIFICATION_TEXT_SHORT)),
         name='password_reset'),
    path('documentation/', include('documentation.urls')),
    path('downloads/', include('uploads.urls')),
    path('jsa/', include('jsa.urls')),
    path('503.html', TemplateView.as_view(template_name='503.html')),
    path('403.html', TemplateView.as_view(template_name='403.html')),
    path('404.html', TemplateView.as_view(template_name='404.html')),
    path('books/', include('dayone.urls')),
    path('misc/', include('misc.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "UFTS Admin"
admin.site.site_title = "UFTS Admin Portal"
admin.site.index_title = "Welcome to the UFTS Portal"
