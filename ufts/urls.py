from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/img/favicon.ico')),
    path('', include('home.urls')),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('documentation/', include('documentation.urls')),
    path('downloads/', include('uploads.urls')),
    path('jsa/', include('jsa.urls')),
    path('503.html', TemplateView.as_view(template_name='503.html')),
    path('403.html', TemplateView.as_view(template_name='403.html')),
    path('404.html', TemplateView.as_view(template_name='404.html')),
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html')),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html')),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html')),
    path('reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')),
    path('books/', include('dayone.urls')),
    path('misc/', include('misc.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "UFTS Admin"
admin.site.site_title = "UFTS Admin Portal"
admin.site.index_title = "Welcome to the UFTS Portal"
