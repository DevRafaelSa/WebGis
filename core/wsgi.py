############ Padrão do projeto/APP  #####################
# Obs: esse arquivo é uma configuração padrão do próprio django e não é recomendado a sua alteração sem conhecimentos prévios.

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
