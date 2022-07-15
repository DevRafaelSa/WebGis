############ Padrão do projeto/APP  #####################
# Obs: esse arquivo é uma configuração padrão do próprio django e não é recomendado a sua alteração sem conhecimentos prévios.

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from django.apps import AppConfig


class MapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map'
