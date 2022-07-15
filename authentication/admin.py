############ Padrão do projeto/APP  #####################
# Obs:  afim de menos poluir o código apenas as views que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas no geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
# Obs2: Uma vez explicado o porquê do uso não foi repetido a explicação nas demais vezes em que se repetem, afim de evitar trabalho desnecessário e poluição visual.

# A tela de usuários nesse projeto foi alterada afim de melhor visualização e implementação dos campos constumizados, ler documentação para mais informação.
#
# Documentação para mais informações: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
# A tela de admin é um APP padrão do django que serve no momento de desenvolvimento, ou através de mais bibliotecas externas possivel a implementação e interação com usuários, como no caso do Jazzmin utilizado nesse projeto.
# Acesso: https://localhost:8000/admin/
# EX:
#   admin.site.register(Objeto)  # Objeto esse criado nas models.py.   
#            ###### (Author: Lucas Calado)  #############
#            #      https://github.com/Kosolov325       #
#            #      https://gitlab.com/Kosolov325       #          
#            #      Date: 06/07/2022                    #            
#########################################################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from .models import *

class UserCreationForm(ModelForm):                     # Formulário de ciração de usuário
   
    class Meta:
        model = Usuario
        fields = ('nome','matricula','usuario', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])                        # No momento do salvamento gerar uma nova senha encriptografada com hash, assim não permitindo a visualização das senhas e garantindo uma melhorar segurança dos usuários.
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm                            # Adicionar o form de criação de usuários
    list_display = ('matricula','usuario','nome','password', 'is_staff', 'is_active', 'is_superuser')
    ordering = list_display

    fieldsets = (
        ('Dados', {'fields': ('usuario', 'password', 'nome', 'matricula', 'is_staff')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'password', 'usuario', 'matricula', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    ######### Padrão de usuário django #########
    filter_horizontal = ()             
    list_filter = ()

    
admin.site.register(Usuario, CustomUserAdmin)         # Adicionar o usuario com o formulário de visualização de admin


# Register your models here.