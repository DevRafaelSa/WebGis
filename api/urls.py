############ Routers funcionamento  #####################
# Por se tratar de algo mais direto sem tanta necessidade de alterações nos seus metódos (até o presente momento que esse código foi escrito)
# foi optado a utilização de ViewSets ao invés de APIViews nas categorias, diferente das demais models desse APP.

# variavel = routers.SimpleRouter() #ou outro tipo de router.
# variavel.Register(1 parâmetro = String,  2 parâmetro = View)
#   Doc: https://www.django-rest-framework.org/api-guide/routers/

# A variável router irá instanciar e salvar um novo objeto SimpleRouter() da biblioteca routers do rest_framework 
# A classe SimpleRouter() consta com o metódo register() para registrar novos endereços.
                                          
# As urls patterns são o conjunto de endereços existentes nesse APP (city), a qual são necessários a utilização de caminhos
# que irão indicar onde determinado tipo de view irá funcionar.

############ Padrão do projeto/APP ######################

# Obs: sempre lembrar de por uma vírgula ao final de cada linha para evitar possiveis erros.
# Obs2: o metódo as_view() serve para instanciar com o tipo certo e a não utilização dele accaretará em erro.
# Obs3: é possível no momento da importação utilizar esse metódo diretamente, assim não sendo necessário a chamada do metódo durante a criação dos endereços.
#     Doc: https://docs.djangoproject.com/en/4.0/topics/class-based-views/

# Obs4: a utilização do metódo re_path() serve para indiciar um funcionamento de um regex, este necessário em casos em que valores dinâmicos serão informados juntamente ao endereço.
#     Doc: https://docs.djangoproject.com/en/4.0/ref/urls/

# urlpatterns = [
#  path(1 parâmetro = String, 2 parâmetro = View.as_view()),

#  re_path(1 parâmetro = String , 2 parâmetro = View.as_view()),
#   # doc: https://docs.djangoproject.com/en/4.0/ref/urls/#re-path
#   # ex: re_path('^usuários/(?P<id>[^\d+$])/$'),    
#   # Obs: nesse exemplo irá funcionar um regex que irá receber valores inteiros. Geralmente regex são implementados em slugs. 
#   # Obs2: o django já conta com regex pre-feitos como no caso de números inteiros e strings, contudo em certos casos a utilização de regex mais elaborados são necessários. 
# 
#  path('',include(variavel.urls)), utilizado para pegar as urls de um router como no caso mostrado em algumas linhas acima.
# ]

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 05/06/2022                    #   
#########################################################

from django.urls import path, re_path, include      # importar path() = Urls normais sem  regex trabalhosos, re_path() regex elaborados, include() usado para incluir as urls criadas no router
from .views import *                                # importar todas as classes do arquivo views.py desse app de maneira rápida.
from rest_framework import routers                  # importar do rest_framework a biblioteca routers.

router = routers.SimpleRouter()                     # instanciar SimpleRouter().
router.register('categorias', CategoriasViewSet)    # incluir no objeto um novo endereço.

regex = '(?P<raio>\d+\.\d{2})'   # salvar o regex que irá ser utilizado mais para frente.
     # Obs: esse regex pega valores do tipo float com 2 casas decimais em metros.
     # Ex: http://127.0.0.1:8000/pontos/1/raio=10.50/

urlpatterns = [
   #Pontos views
   path('pontos/', PontosView.as_view()),     # Endpoint para todos os pontos
   path('pontos/<int:id>/', PontosViewDetail.as_view()), # Endpoint para um ponto especifico passando a Primary Key como parâmetro
   path('pontos/<int:id>/<int:id2>/', PontosViewDistancia.as_view()), # Endpoint para distância de dois pontos em metros passando duas Primary Keys como parâmetros
   re_path('^pontos/(?P<id>[^/.]+)/raio=' + regex + '/$' , PontosViewRaio.as_view()),   # Endpoint para checar pontos em um raio a partir de uma Primary Key e um Raio como parâmetro
   path('pontos/<int:id>/linhas/', PontosViewLinhas.as_view()),   # Endpoint para checar se um ponto está inserido en alguma linha a partir de uma Primary Key como parâmetro
  

   #Linhas views  
   path('linhas/', LinhasView.as_view()),     # Endpoint para todas as linhas
   path('linhas/<int:id>/', LinhasViewDetail.as_view()), # Endpoint para uma ponto linha especifica passando a Primary Key como parâmetro
   path('linhas/<int:id>/linhas/', LinhasViewLinhas.as_view()), # Endpoint para checar se linhas se tocam ou cruzam a partir de uma Primary Key como parâmetro
   path('linhas/<int:id>/poligonos/', LinhasViewPoligonos.as_view()), # Endpoint para checar se alguma linha cruza algum poligono

   #Poligonos views
   path('poligonos/', PoligonosView.as_view()), # Endpoint para todos os poligonos
   path('poligonos/<int:id>/', PoligonosViewDetail.as_view()), # Endpoint para um poligono em especifico passando a Primary Key como parâmetro
   path('poligonos/<int:id>/<int:id2>/', PoligonosViewPoligonos.as_view()),   # Endpoint para checar se dois poligonos se intersectão ou são vizinhos passando duas primary keys como parâmetros
   path('poligonos/<int:id>/pontos/', PoligonosViewPontos.as_view()),   # Endpoint para checar se existem pontos dentro do poligono
  

   #Categorias views
   path('',include(router.urls)), #Categorias viewset
   path('categorias/<int:id>/', CategoriasViewDetail.as_view()),
]