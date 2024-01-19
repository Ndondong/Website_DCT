from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
#now import the views.py file into this code

from . import views
from .forms import UserLoginForm

urlpatterns=[
    path('', views.Dashboard, name='dashboard'),
    path('penyisipan/', views.Penyisipan, name='penyisipan'),
    path('penyisipan/detail/<slug:embed_id>/', views.DetailPenyisipan, name='detail-penyisipan'),
    path('pengekstrakan/', views.Pengekstrakan, name='pengekstrakan'),
    path('aktivitas/<str:aktivitas>/', views.Aktivitas, name='aktivitas'),
    path('download/<slug:embed_id>/', views.DownloadImage, name='download-image'),
    path('download/h/<slug:embed_id>/', views.DownloadHost, name='download-host'),
    path('download/w/<slug:embed_id>/', views.DownloadWatermark, name='download-watermark'),
    path('download/e/<slug:extract_id>/', views.DownloadExtractWatermark, name='download-extracted'),
    path('register/', views.Register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/login.html'), name='logout'),
    # path('register/', views.Register, name='register'),
    # path('history-embed/', views.HistoryEmbed, name='history-embed'),
    # path('history-extract/', views.HistoryExtract, name='history-extract'),
    # path('history-embed/<slug:slug>/', views.HistoryEmbedImage, name='history-embed-image'),
    # path('history-extract/<slug:slug>/', views.HistoryExtractImage, name='history-extract-image'),
    # path('embed/process/', views.EmbedProcess, name='embed-process'),
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', authentication_form=UserLoginForm), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='auth/login.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)