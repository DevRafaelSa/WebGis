############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Maior parte das classes das views foram feitas utilizando API VIEWS, com exceção das categorias por se tratar de uma view sem tantas funcionalidades (até o presente momento).
# Obs3: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.

# Doc: https://docs.djangoproject.com/en/4.0/topics/http/views/
# Doc: https://docs.djangoproject.com/en/4.0/ref/request-response/

# A estrutura e lógica das views instanciadas de APIView.
# Ex:
# class NomeView(APIView):
#   def metodo(self, request):          # Metodos são os tipos de metodos dos requests que são os principais: GET, PUT, POST, DELETE.
#       try:
#               objetos = Objetos.objects.all()                      # A varíavel objetos irá salvar todos as instâncias da Model Objetos (models.py) que estão salvas no banco de dados.
#               serializer = ObjetoSerializer(objetos, many=True)    # A varíavel serializer está envolvendo todos os objetos do banco de daos em um serializer que serve como capsula que engloba e transforma as fields em formato JSON.
#           return Response(serializer.data)                         # O metódo Response será retornado juntamente com os dados do serializer que estão em formato JSON.
#       except:
#           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   # Em caso de algum erro no processo acima o algoritmo irá retornar um JSON com uma mensagem de erro mais um número de status code 500 ao request indicando erro.
   
# As classes de views que aprensentam mais parâmetros nos metódos são os parâmetros que serão recebidos da sua respectiva url.
#    Obs: ler urls.py.

#  Ex: 
#   class NomeViewDetail(APIView):        # Nesse caso iremos ver em especifico o GET de um objeto apenas, enquanto o exemplo interior eram de todos registrados no banco de dados.
#     def get(self, request, id):         #  O id que vai ser recebido pela barra de pesquisa do browser com seu respectivel caminho criado no (urls.py).
#         try:
#             if id == 0:                                                                                                               # Se o id for igual a 0 o código irá automaticamente retornar um erro devido a natureza do funcionamento: todos os objetos instanciados no banco de dados sempre iniciam com id 1.
#                  return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             objeto = Objeto.objects.get(pk=id)                                                                                        # A varíavel objeto irá salvar uma Model em especifica salva nos bancos de dados utilizando o parâmetro 'Primary Key' (pk) que foi passado pelo request (urls.py).
#             serializer = ObjetoSerializer(objeto)                                                                                     # O serializer irá envolver o objeto em especifico e transforma-lo em formato JSON.
#             return Response(serializer.data)      # O algoritmo retorna os dados do serializer que estão em formato JSON
#         except:
#             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     # Em caso de algum erro no processo acima o algoritmo irá retornar um JSON com uma mensagem de erro mais um número de status code ao request.
#

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *

#Pontos
class PontosView(APIView):
    permission_classes = [IsAuthenticated]    # Necessário ter algum tipo de autenticação
    def get(self, request):
        try:
         pontos = Ponto.objects.all()
         serializer = PontosSerializer(pontos, many=True)       # many=True serve como parâmetro para indicar que vários objetos serão puxados do banco de dados.
         return Response(serializer.data)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = PontosSerializer(data=request.data)   # A varíavel serializer está instanciando o serializer e passando os dados (data) como sendo aquela presente no request afim de instanciar um novo objeto no banco de dados.
            if serializer.is_valid():           # No caso do metódo post é necessário chegar a validade do serializer que envolveu os dados.
                serializer.save()               # Após a checagem o serializer faz o salvamento automático desse novo objeto.
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)        # Caso tudo ocorra alguém o request irá retornar com o novo objeto craido no banco de daos mais um status code 200 OK que confirma a criação.
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PontosViewDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id == 0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            ponto = Ponto.objects.get(pk=id)
            serializer = PontosSerializer(ponto)
            return Response(serializer.data)
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            ponto = Ponto.objects.get(pk=id)
            ponto.delete()                              # No caso do metódo delete após o instanciamento através da varíavel ponto é chamado o metódo delete para realizar a remoção do banco de dados.
            return Response()
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            if id == 0:
               return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            ponto = Ponto.objects.get(pk=id)                            # No metódo put para atualizar um objeto já existente no banco de dados primeiro é necessário encontra-lo através de sua 'Primary Key' que será passada pelo parâmetro (pk) mais o id que foi passado pela sua respectiva url (urls.py).
            serializer = PontosSerializer(ponto, data=request.data)        # O serializer irá envolver o ponto e passar os novos dados através do parâmetro data que irá receber os dados anexados ao request.
            if serializer.is_valid():                                      # Checar se os dados foram corretamente indicados
                serializer.save()                                          # Salvar/atualizar o objeto instanciado no banco de dados
                return Response(serializer.data)                        
            return Response()                                             # Caso o serializer não seja válido irá retornar nada, pois assim será possível uma nova tentativa.                           
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PontosViewLinhas(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            pontoSelf = Ponto.objects.get(pk=id)
            pontoSelf = pontoSelf.coordenadas         # a varíavel pontosSelf irá ser igual as coordenadas do objeto Ponto e será utilizada para interação com metódos do GIS/Geodjango que servem para interagir com coordenadas geográficas.  Doc: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/                              
            linhas = Linha.objects.all()              # A varíavel linhas irá salvar/receber todos os objetos Linha salvos no banco de dados.      
            pontoSelf = pontoSelf.buffer(0.00003)  # Aumentar um pouco o tamanho do ponto para melhor interação
            allserializers = []

            for linha in linhas:                     # Loop por todos os objetos linha salvo no banco de dados.
                line = linha.coordenadas             # Uma nova varíavel line irá receber as coordenadas de uma linha especifica afim de interagir com geodjango
                if line.crosses(pontoSelf) or line.intersects(pontoSelf) or line.touches(pontoSelf):     #Caso a linha toque, cruze ou interseccione o ponto o algoritmo dará continuidade. Obs: apenas toque não é o suficiente visto que o geodjango trabalha de maneiras que vão além da semântica e sim matemáticamnete falando. Doc: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/geoquerysets/
                    serializer = LinhasSerializer(linha)        
                    allserializers.append(serializer.data)   # Toda vez que uma linha atender os requisitos da condicional ela irá ser adicionada ao serializer que vai ser retornado.

            return Response(allserializers)
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PontosViewDistancia(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, id2):            # Mais de um parâmetro que vai ser recebido pelo request e endereçado em urls.py
        try:
            if id == 0 or id2 == 0:             # Os objetos são instanciados apartir do id 1 em caso de outra condição o código dará continuidade.
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            pontoA = Ponto.objects.get(pk=id)
            
            pontoA = pontoA.coordenadas
            pontoA.transform(3857)              # Como o objeto de retorno será a distância de dois pontos é necessário que a distância seja em valores de fácil leitura para humanos, por isso o ponto chama o metódo transform, a qual irá transformar em unidades de medidas relacionais a metros, para melhor compreensão. Doc: https://docs.djangoproject.com/en/4.0/ref/contrib/gis/geos/#django.contrib.gis.geos.GEOSGeometry.transform

            pontoB = Ponto.objects.get(pk=id2)

            pontoB = pontoB.coordenadas      
            pontoB.transform(3857)              # O mesmo vale para o segundo ponto, a qual será transformado em referências de metros, para melhor compreensão.

            dist = pontoA.distance(pontoB)      # O metódo distance() irá retornar a distância dos dois pontos em metros, após a transformação.

            return Response({'distance':dist})      # Um JSON será retornado com a distância em questão seguindo a lógica "distance": 'valor'.
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class PontosViewRaio(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, raio):   # Dois parâmetros, a qual um é um raio que será trazido como string. (urls.py)
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            pontoSelf = Ponto.objects.get(pk=id)
            pontos = Ponto.objects.all()
            raio = float(raio)      # É necessário a conversão para float, visto que raio irá ser recebido como tipo String.
    
            centro = pontoSelf.coordenadas         # A varíavel centro irá ser o ponto em questão para ser trabalhado em cima de sí.
            centro.transform(3857)                     
            circulo = centro.buffer(raio)         # A varíavel circulo irá guardar o centro e aumentar sua área utilizando o parâmetro raio como valor, a qual foi passado pelo request.
            
            allserializers = []

            for ponto in pontos:
                point = ponto.coordenadas
                point.transform(3857)
                if circulo.contains(point):      # Caso o círculo contenha o ponto
                    point = point.transform(4326)       # transformar o ponto para o formato padrão do geodjango, afim de ser mostrado nos valores padrões.
                    serializer = PontosSerializer(ponto)
                    allserializers.append(serializer.data)

            return Response(allserializers)             # Retorna todos os pontos inseridos no círculo
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Linhas
class LinhasView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
         linhas = Linha.objects.all()
         serializer = PontosSerializer(linhas, many=True)
         return Response(serializer.data)
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = LinhasSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LinhasViewDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id == 0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            linha = Linha.objects.get(pk=id)
            serializer = LinhasSerializer(linha)
            return Response(serializer.data)
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id == 0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            linha = Linha.objects.get(pk=id)
            linha.delete()
            return Response()
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            linha = Linha.objects.get(pk=id)
            serializer = LinhasSerializer(linha, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response()
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LinhasViewLinhas(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id==0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            linhaSelf = Linha.objects.get(pk=id)
            linhaSelf = linhaSelf.coordenadas
            linhas = Linha.objects.all()
            
            allserializers = []

            for linha in linhas:
                line = linha.coordenadas
                if linhaSelf.crosses(line) or linhaSelf.touches(line):
                    serializer = LinhasSerializer(linha)
                    allserializers.append(serializer.data)
            
            return Response(allserializers)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LinhasViewPoligonos(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id==0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            linha = Linha.objects.get(pk=id)
            linha = linha.coordenadas

            poligonos = Poligono.objects.all()
            
            allserializers = []

            for poligono in poligonos:
                poly = poligono.coordenadas
                if poly.contains(linha) or linha.crosses(poly) or linha.intersects(poly) or linha.touches(poly):
                    serializer = PoligonosSerializer(poligono)
                    allserializers.append(serializer.data)
                
            return Response(allserializers)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Poligonos
class PoligonosView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
         poligonos= Poligono.objects.all()
         serializer = PoligonosSerializer(poligonos, many=True)
         return Response(serializer.data)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = PoligonosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PoligonosViewDetail(APIView):
    def get(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            poligono = Poligono.objects.get(pk=id)
            serializer = PoligonosSerializer(poligono)
            return Response(serializer.data)
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            poligono = Poligono.objects.get(pk=id)
            poligono.delete()
            return Response()
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            poligono = Poligono.objects.get(pk=id)
            serializer = PontosSerializer(poligono, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response()
        except:
            return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PoligonosViewPontos(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            if id==0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            poligono = Poligono.objects.get(pk=id)
            poligono = poligono.coordenadas
            pontos = Ponto.objects.all()
            
            allserializers = []
            for ponto in pontos:
                point = ponto.coordenadas
                if poligono.contains(point):
                    serializer = PontosSerializer(ponto)
                    allserializers.append(serializer.data)

            return Response(allserializers)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PoligonosViewPoligonos(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, id2):
        try:
            if id==0 or id2 == 0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            poligonoA = Poligono.objects.get(pk=id)
            poligonoA = poligonoA.coordenadas
            
            poligonoB = Poligono.objects.get(pk=id2)
            poligonoB = poligonoB.coordenadas
            
            serializer = []

            poligonoA.transform(3857)
            poligonoB.transform(3857)
            dist = poligonoA.distance(poligonoB)

            if dist <= 100:          # Se a distância entre os dois pontos for menor ou igual X metros considerar os poligonos como vizinhos, esse valor é arbitrário e pode ser alterado sem prejudicar o funcionamento do algoritmo.
                serializer.append({'vizinhos': True})

            if poligonoA.contains(poligonoB):
                serializer.append({'contains': True})

            if poligonoA.intersects(poligonoB):
                serializer.append({'intersects': True})

                intersection = poligonoA.intersection(poligonoB)            # Retorna os pontos das áreas de intersecção dos dois poligonos.
                intersection.transform(4326)
                intersections = []
                for point in intersection:
                        for p in point:
                            intersections.append(p)

                serializer.append({'intersection_points': intersections})

            return Response(serializer)
        except:
             return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Categoria
class CategoriasViewSet(viewsets.ModelViewSet):     # View sets são mais diretas e apenas precisam especificar qual os objetos que serão interagidos e seu respectivel serializer.
    permission_classes = [IsAuthenticated]    
    queryset = Categoria.objects.all()            # A varíavel queryset é uma varíavel padrão do modelViewSet e deve informar quais objetos serão interagidos.
    serializer_class = CategoriasSerializer      # A varíavel serializer_class também é uma varíavel padrão e serve pra indicar qual serializer irá funcionar em cima do queryset. 
                                                # Para mais info relacionado acesse a DOC: https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
                                                
class CategoriasViewDetail(APIView):        #  Obs: Apesar disso o queryset não funciona com um objeto em especifico, apenas por todos, por isso foi optado a utilização de APIView nesse trecho do código. (ATENÇÃO: Até o presente momento em que o código foi escrito não sei se é possível)
    permission_classes = [IsAuthenticated]  
    def get(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            categoria = Categoria.objects.get(pk=id)
            serializer = CategoriasSerializer(categoria)
            return Response(serializer.data)
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            if id == 0:
                 return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            categoria = Categoria.objects.get(pk=id)
            categoria.delete()
            return Response()
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            if id == 0:
                return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            categoria = Categoria.objects.get(pk=id)
            serializer = CategoriasSerializer(categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response()
        except:
           return JsonResponse({'mensagem': "Ocorreu um erro no servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)