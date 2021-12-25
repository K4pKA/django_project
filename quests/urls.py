from django.urls import path, include
from . import views
import django.contrib.auth
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginUser, logout_user, RegisterUser, Quest1ListView, AboutView, CommDeleteView, ResultView
from .views import IsTestProcessed, TestsView, IndexView

urlpatterns = [
                  path('', IndexView.as_view(), name="home"),
                  path('about', AboutView.as_view(), name="about"),
                  path('help', views.help, name='help'),
                  path('quests', TestsView.as_view(), name='quests'),
                  path(r'view/<int:pk>', Quest1ListView.as_view(), name='view'),
                  path('login/', LoginUser.as_view(), name='login'),
                  path('logout/', logout_user, name='logout'),
                  path('register/', RegisterUser.as_view(), name='register'),
                  path(r'captcha/', include('captcha.urls')),
                  path('<int:pk>/delete', CommDeleteView.as_view(), name='delete'),
                  path('<int:pk>/redirect_to_result', IsTestProcessed.as_view(), name='redirect_to_result'),
                  path('result/test<int:pk>/view', ResultView.as_view(), name="result")
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
