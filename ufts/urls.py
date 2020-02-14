from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dayone.views import upload_dayone, book_list, delete_book, upload_book

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('consent/', include('consent.urls')),
    path('documentation/', include('documentation.urls')),
    path('downloads/', include('uploads.urls')),
    path('upload_software', TemplateView.as_view(template_name='uploads/upload_software.html'), name='upload_software'),
    path('verify_software', TemplateView.as_view(template_name='uploads/verify_software.html'),name='verify_software'),
    path('jsa/', include('jsa.urls')),
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html')),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html')),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html')),
    path('reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')),
    path('dayone/', upload_dayone, name='dayone'),
    path('books/', book_list, name='book_list'),
    path('books/dayone/', upload_book, name='upload_book'),
    path('books/<int:pk>/', delete_book, name='delete_book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "UFTS Admin"
admin.site.site_title = "UFTS Admin Portal"
admin.site.index_title = "Welcome to the UFTS Portal"
