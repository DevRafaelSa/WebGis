############ Padrão do projeto #####################
# Obs:  Afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.
# Obs3: Não esquecer as vírgulas ao final de cada linha.


# Documentação para mais informações: https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Esse arquivo irá incluir todas as urls de cada app do projeto e para isso será utilizado as funções path, include do próprio django.
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# App de documentação Swagger. 

schema_view = get_schema_view(       # Criação de uma view constumizada
   openapi.Info(
      title="wEBGIS API",
      default_version='v3',
      description="Api Webgis",
   ),
   public=False,
   permission_classes=[permissions.IsAdminUser], 
)

urlpatterns = [
    path('api/', include('api.urls')),     # Essa url irá cuidar do endereçamento das urls do backend e irá incluí-las no projeto (app API).
    path('', include('map.urls')),     # Essa url irá cuidar do endereçamento das urls do frontend e irá incluí-las no projeto (APP map).
    path('', include('authentication.urls')),  # Essa url irá cuidar do endereçamento de autenticação de usuário
    path('admin/', admin.site.urls),   # Essa url é padrão do próprio django e serve para listar onde o app 'admin' (também padrão do django) estará funcionando, afim de realização de testes no desenvolvimento é interessante a sua implementação.

    #Urls documentação
    re_path(r'^doc/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^doc/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

    # Geração de novos tokens por usuário
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
