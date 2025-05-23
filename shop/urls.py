"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.messages import api
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from media import images
from django.conf import settings
import account.views
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from home import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('celery/', include('home.views.task')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),        # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('signup/', account.views.RegisterView.as_view(), name='signup'),
    path('signin/', account.views.SigninUser.as_view(), name='signin'),
    path('signout/', account.views.SignoutUser.as_view(), name='signout'),
    # path('signup/', home.views.signup_user, name='signup'),
    path('product/', include('home.urls'), name='product'),
    path('contact-us/', include('contact_module.urls'), name='contact-us'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # path('api/', include('api.urls')),
    # path('best_product/', views.BestProductSlider.as_view(), name='best_product'),
    path('', include('main.urls')),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', account.views.RefreshTokenView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
