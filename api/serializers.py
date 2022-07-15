############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.

# Serializers servem para envolver objetos criados no banco de dados e formata-los em formato JSON.
# Doc: https://www.django-rest-framework.org/api-guide/serializers/

# A lógica utilizada nos algoritmos aqui presentes segue essa linha de raciocinio:
# Ex:
# class ObjetoSerializer(serializers.ModelSerializer):             
#     class Meta:                                   # A class Meta serve para indicar o meta (também conhecido como etiqueta, informações.. etc) do serializer, logo o seu corpo.
#         model = Objeto                            # O corpo do serializer irá estar trabalhando com uma model chamada Objeto (models.py).
#         fields = "__all__"                        # Os campos que serão pegos pelo serializer serão todos.
#         read_only_fields = ("id",)                # Como o banco de dados cria objetos sempre incrimentando a 'Primary Key' e essa se relacionara com o id, é preciso especificar que é apenas um campo de leitura, pois caso você tente alterar um objeto com o id 1 e outro com o id 2 e deixe ambos com o mesmo id, seria um problema para interagir com eles, pois há dois objetos com o mesmo id.
# 
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from rest_framework import serializers
from .models import *

class PontosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponto
        fields = "__all__"
        read_only_fields = ("id",)
        
class LinhasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linha
        fields = "__all__"
        read_only_fields = ("id",)

class PoligonosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poligono
        fields = "__all__"
        read_only_fields = ("id",)

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        read_only_fields = ("id",)

