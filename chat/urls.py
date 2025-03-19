from django.urls import include, path

from chat import admin
from .views import chatbot_view, get_response

urlpatterns = [
    path("", chatbot_view, name="chatbot"),
    path("get_response/", get_response, name="get_response"),
    path('admin/', admin.site.urls),
    path('chat/', include('chatbot.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'), # type: ignore
]
