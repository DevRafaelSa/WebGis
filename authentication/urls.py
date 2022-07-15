############ Padrão do projeto/APP ######################

# Obs: sempre lembrar de por uma vírgula ao final de cada linha para evitar possiveis erros.

# urlpatterns = [
#  path(1 parâmetro = String, 2 parâmetro = view, 3 parâmetro = String),
#             # Obs: o 3 parâmetro é utilizado para chamar essa view por meio do netódo redirect e em caso de ambientes externos, utilizar o nome do app + o nome da  url. 
#             # Ex: redirect('auth:login')

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 05/06/2022                    #   
#########################################################

from django.urls import path
from .views import *

app_name = 'auth'                # Dar nome ao APP para utilização das urls em ambientes externos a esse app.

urlpatterns=[
    path('auth/cadastro/',cadastro, name='cadastro'),                 # View de cadastro
    path('auth/login/', login, name='login'),                          # View de login
    path('auth/valida_cadastro/', valida_cadastro, name='valida_cadastro'),  # View de validação de cadastro
    path('auth/valida_login', valida_login, name='valida_login'),            # View de validação de login
    path('auth/sair/', sair, name = 'sair'),                                 # View de logout           

    path('admin/login/', admin_login, name='admin-login'),                 # Substituição da tela de login do app admin para a do nosso APP
]