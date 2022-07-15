# Webgis

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://gitlab.com/repositoriodafabrica/ex2022_1_webgis_viviano/-/tree/Calado-Tasks/task1)

Requisitos:

  - PostgreSQL
  - Postgis
  - GeoDjango
  - etc
  
### Como usar
Tutorial:
https://youtu.be/TlrWduZC4Ko

É necessário primeiramente a instalação dos requisitos e seus requisitos internos consultando a documentação do geodjango.
(https://docs.djangoproject.com/en/4.0/ref/contrib/gis/tutorial/)

``` python
#Git setup up
git clone https://gitlab.com/repositoriodafabrica/ex2022_1_webgis_viviano.git
git switch Calado-Tasks

python -m venv venv  #Inicializa o ambiente virtual
cd /venv/Scripts
activate # ou .\activate caso esteja utilizando o powershell
cd ../..
pip install -r requirements.txt

#Obs: Acesse o settings.py do projeto e ligue com seu banco de dados PostgreSQL com a extensão do postgis funcional e em seguida continue
#Obs2: Lembrar de setar a variável debug como False no arquivo settings.py no momento do deploy

py manage.py makemigrations
py manage.py migrate
py manage.py runserver

#enjoyyyy
```
