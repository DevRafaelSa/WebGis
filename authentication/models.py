############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não será repetida a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.



# Documentação para mais informações: https://docs.djangoproject.com/en/4.0/topics/db/models/
# Models são templates dos objetos que serão salvos no banco de dados que serão instanciadas e interagidas pelas views.
# A linha de raciocinio utilizada aqui é a seguinte:
# Ex:
# class Objeto(models.Model):        
#     nome=models.CharField(max_length=30)                   # Uma field que irá receber valores do tipo String de no máximo 30 caracteres.
#     usuario=models.CharField(max_length=30)                         
#               
#
#     def __str__(self):                                        # Quando a interação ocorrer com esse objeto ele irá fazer uma rotina de algoritmos.
#         return self.nome                                      # A rotina de algoritmos será retornar o nome de sí mesmo, ou seja ao utilizar print(objeto) ele sempre irá retornar seu próprio nome. (Obs: isso serve para interações relacionais como na tela de admin do próprio django)
# 
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 06/07/2022                    #            
#########################################################


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken


class MyUserManager(BaseUserManager):           # O código irá pegar a classe de base de usuário para substituir o padrão do Django e para tal é necessária a substituição dos metódos padrões.  Doc: https://docs.djangoproject.com/en/4.0/topics/auth/customizing/
    ######### Padrão de usuário django #########
    def create_user(self, nome, matricula, usuario, password):
        user = self.model(nome=nome, matricula=matricula, usuario=usuario)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, nome, usuario, matricula, password):        # Metódo utilizado com o comando python manage.py createsuperuser
        user = self.create_user(nome, matricula, usuario, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def get_by_natural_key(self, matricula):                             # Metódo utilizado no momento de autenticação, afim de utilizar matrícula como valor para login.
        return self.get(matricula=matricula)

class Usuario(AbstractBaseUser):
    nome=models.CharField(max_length=30)
    usuario=models.CharField(max_length=30)
    matricula=models.IntegerField(unique=True)
    password = models.CharField(('password'), max_length=128)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()                   # indicar que irá utilizar a classe MyUserManager() como gerenciador de usuário.
    USERNAME_FIELD = 'matricula'                # indicar qual field será utilizado como Login 
    REQUIRED_FIELDS = ['nome', 'usuario']       # Demais fields que são obrigatórios na criação de um usuário

    def __str__(self) -> str:
        return self.nome

    
    def get_tokens_for_user(user):             # Tal metodo irá gerar um novo token e retornar seu access e seu refresh
        refresh = RefreshToken.for_user(user)  

        return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }                                     

    @property
    def token(self):                                    # Essa propriedade permite acessar e retornar através do metodo .token() do usuário um novo token para utilização.  Obs: uso mais utilizado pelo frontend.
        token = self.get_tokens_for_user()
        return  token['access']
        
    

    ######### Padrão de usuário django #########
    def get_short_name(self):   
        return self.usuario

    def get_full_name(self):
        return  self.nome

    def has_perm(self, perm, ob=None):
        return self.is_staff
    
    def get_all_permissions(self):
        return []

    def has_module_perms(self, app_label):
        return self.is_staff

    def natural_key(self):
        return self.matricula

# Create your models here.