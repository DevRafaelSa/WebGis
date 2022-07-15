############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não foi repetido a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.



# Documentação para mais informações: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
# A tela de admin é um APP padrão do django que serve no momento de desenvolvimento, ou através de mais bibliotecas externas possivel a implementação e interação com usuários, como no caso do Jazzmin utilizado nesse projeto.
# Acesso: https://localhost:8000/admin/
# EX:
#   admin.site.register(Objeto)  # Objeto esse criado nas models.py.   
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Ponto)
admin.site.register(Linha)
admin.site.register(Poligono)
admin.site.register(Categoria)

