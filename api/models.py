############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.



# Documentação para mais informações: https://docs.djangoproject.com/en/4.0/topics/db/models/
# Models são templates dos objetos que serão salvos no banco de dados que serão instanciadas e interagidas pelas views.
# A linha de raciocinio utilizada aqui é a seguinte:
# Ex:
# class Objeto(models.Model):                               
#     name = models.CharField(max_length=100, default="")       # Uma field que irá receber valores do tipo String de no máximo 100 caracteres.
#     desc = models.TextField(max_length=100)                   # uma field que irá receber valores do tipo String, contudo mais utilizados para memorandos/descrições, por isso utilizado o tipo TextField.
#
#     def __str__(self):                                        # Quando a interação ocorrer com esse objeto ele irá fazer uma rotina de algoritmos.
#         return self.name                                      # A rotina de algoritmos será retornar o nome de sí mesmo, ou seja ao utilizar print(objeto) ele sempre irá retornar seu próprio nome. (Obs: isso serve para interações relacionais como na tela de admin do próprio django)
# 
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
import re
# Create your models here.

class Categoria(models.Model):
     def is_svg(file):
        SVG_R = r'(?:<\?xml\b[^>]*>[^<]*)?(?:<!--.*?-->[^<]*)*(?:<svg|<!DOCTYPE svg)\b'
        SVG_RE = re.compile(SVG_R, re.DOTALL)

        f = file
        file_contents = f.read().decode('latin_1')  # avoid any conversion exception
        svg = SVG_RE.match(file_contents)

        if(svg is None or svg is False):
            raise ValidationError('O arquivo não é um svg válido.')

     name = models.CharField(max_length=50,  default="")      
     icon = models.FileField(upload_to='static/categorias', validators=[is_svg]) # Um field do tipo imagem (Biblioteca Pillow: https://docs.djangoproject.com/en/4.0/topics/files/) serão salvos na pasta de arquivos estaticos que se encontra em static e no seu diretóroio categorias.
     
     def __str__(self):
        return self.name

class Ponto(models.Model):
    name = models.CharField(max_length=100, default="")
    desc = models.TextField(max_length=100,  default="")
    coordenadas = models.PointField(srid=4326)           # As models das coordenadas irão utilizar fields geográficas do próprio geodjango, a qual irá ser utilizado a referência espacial padrão (srid) como 4326, em caso de troca para valores de metros é necessário fazer a alteração nas views. 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)    

    def __str__(self):
        return self.name

class Linha(models.Model):
    name = models.CharField(max_length=100, default="")
    desc = models.TextField(max_length=100)
    coordenadas = models.LineStringField(srid=4326)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) 


    def __str__(self):
        return self.name

class Poligono(models.Model):
    name = models.CharField(max_length=100, default="")
    desc = models.TextField(max_length=100)
    coordenadas = models.PolygonField(srid=4326)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) 


    def __str__(self):
        return self.name