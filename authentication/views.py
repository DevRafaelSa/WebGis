############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.

# Nesse app, diferente do app 'API' as views são feitas utilizados metodos e são de maneira geral mais simples.
# Ex:  def nome_view(request):
#        *algoritmo*
#         return redirect() ou render()
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 26/06/2022                    #            
#########################################################

from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

def cadastro(request):                   # View para a área de cadastro.
    status=request.GET.get('status')      # Caso haja um status devido a um erro no momento de login renderizar a view com esse status code.
    return render(request, 'cadastro.html', {'status': status})         # Renderizar o arquivo cadastro.html + o status code a lógica irá acontecer no html.

def valida_cadastro(request):               
    nome= request.POST.get('nome')
    matricula=request.POST.get('matricula')
    senha=request.POST.get('senha')
    user = request.POST.get('usuário')
    
     ############## Tratamento de erros Inicio ##############
    if matricula.isnumeric() != True:            # Caso a matrícula não seja númerica renderizar um erro.
        return redirect('/auth/cadastro/?status=5')
    
    usuario = Usuario.objects.filter(matricula=matricula)         # Procurar a existência de um usuário por meio da matricula.
   
   
    if len(nome.strip()) == 0 or (matricula==0):                  # Caso a matrícula ou o nome não tenham valores.
        return redirect('/auth/cadastro/?status=1')                

    if len(senha) < 8:                                          # Caso a senha seja menor que 8 caracteres.
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:                                       # Caso haja a existência de um usuário já cadastrado.
        return redirect('/auth/cadastro/?status=3')
    ############## Tratamento de erros Fim ##############
    
    try:
        usuario = Usuario(nome = nome,
                          usuario=user,
                          matricula=matricula)
        usuario.set_password(senha)
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:                                                  # Mesmo se algum erro ocorrer após o tratamento de erro retornar um aviso de erro interno no sistema.
        return redirect('/auth/cadastro/?status=4')                  

def admin_login(request):                                 
    return redirect('/auth/login/?next=/admin/')

def login(request):
    status=request.GET.get('status')
    next=request.GET.get('next')
    return render(request, 'login.html', {'status': status, 'next':next})


def valida_login(request):
    matricula=request.POST.get('matricula')
    senha=request.POST.get('senha')
    next=request.GET.get('next')

     ############## Tratamento de erros ##############
    if matricula.isnumeric() != True:
        if(next):
            return render(request, 'login.html', {'status': '1', 'next':next})
        else:
            return redirect('/auth/login/?status=1')

    user = authenticate(request, matricula=matricula, password=senha)           # Tentar autenticar com a matrícula e a senha.

    if user is None:             # Caso não seja possível o login
        if (next):
            return render(request, 'login.html', {'status': '2', 'next':next})
        else:
            return redirect('/auth/login/?status=2')
    ############## Tratamento de erros ##############

    elif user is not None:                        # Caso a autenticação tenha sido um sucesso. 
        auth_login(request, user)                # Anexar usuário ao request
        if (next):
            return redirect(next)
        else:
            return redirect('map:index')           # Redirecionar para o mapa


def sair(request):                            # Tela para deslogar
    request.session.flush()                  # Limpar a sessão do request
    return redirect('/auth/login/')         
   



# Create your views here.
