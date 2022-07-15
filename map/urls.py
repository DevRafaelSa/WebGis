############ Padrão do projeto/APP ######################
# Obs: sempre lembrar de por uma vírgula ao final de cada linha para evitar possiveis erros.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.


# Nesse arquivo serão utilizadas urls para endereçar as respectivas views.

# urlpatterns = [
#  path(1 parâmetro = String, 2 parâmetro = view, 3 parâmetro = dar nome desse endereçamento),

#]

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 05/06/2022                    #   
#########################################################

from django.urls import path

from .views import *

app_name = 'map'

urlpatterns = [
    path('', home, name='home'),         # Essa url serve para qualquer tentativa de acesso sem um endereço especificado ser redirecionado para home.
    path('map/index/', index, name='index'),   # View em que será utilizada como padrão do app.

]

