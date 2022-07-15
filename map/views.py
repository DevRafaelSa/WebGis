############ Padrão do projeto/APP ######################
# Obs: sempre lembrar de por uma vírgula ao final de cada linha para evitar possiveis erros.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.
# Obs3: Automaticamente devido a configuração do ambiente em core/settings.py os arquivos htmls estarão sendo automaticamente acessados através da pasta templates inserido nesse diretório.


# Aqui serão utilizadas views baseadas em metódos que pelo padrão do projeto serão implementadas apenas para telas mais especificas ficando o resto do trabalho pelo front.
# Doc: https://docs.djangoproject.com/en/4.0/topics/http/views/

#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 05/06/2022                    #   
#########################################################

import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required   # Necessário estar logado para o acesso
def home(request):
    return redirect('map:index')     # Redirect irá redirecionar a url que tiver o name como parâmetro.

@login_required
def index(request):
    context = {
        'settings': json.dumps(settings.MAP_SETTINGS),
    }
    return render(request, 'map/index.html', context)      # Render serve para renderizar na tela do usuário o html de quem fez o request a determinada tela.
                                                  # Arquivos htmls estão dentro da pasta templates de cada APP, devido a configuração do projeto.