//############ Padrão do projeto/APP  #####################
//# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//#    
//#   IMPORTANTE:
//#    1º O geojson trabalha com longitude, latitude, enquanto o leaflet trabalha com latitude, longitude, logo é crucial que ao pegar os atributos latlngs ou latlng dos seguintes objetos: Marker, PolyLine, Polygon é necessário fazer a inversão dos valores antes de enviar para o back, logo  x = objeto.lng, y = objeto.lat. 
//#    2º O leaflet permite a criação de objetos geojson, sendo assim não há a necessidade de inverter os valores do objeto, contudo eu (desenvolvedor) só fui perceber essa funcionalidade após de já ter quase encerrado a criação da aplicação... sendo assim optei por apenas os poligonos trabalharem dessa forma, pois não seria necessario um looping e isso causaria um uso de hardware desnecessário da máquina host.
//#    3º Objetos como Polylines e Polygons guardam determinados valores e não necessariamente todos os pontos em um plano, apenas alguns vetores para o backend através de calculos matemáticos internos realizar as operações.
//#
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 06/07/2022                    #            
//#########################################################

var Markers = new Object;                           // Objeto que irá guardar todos os objetos Pontos.
var Icons = new Object;                             // Objeto que irá guardar todos os objetos icones.
var selectedCoords = new Array();                   // Array que irá guardar as coordenadas.
var selectedObj;                                    // Varíavel que irá guardar o objeto que foi clickado até então.
var selectedObjs = new Object;                      // Objeto que irá guardar todos os objetos que foram selecionados.

var popup = L.popup({ maxWidth: 1000 });                              // Objeto que irá ser utilizado para checar popups em determinados casos.
var coord;                                          // Varíavel que irá guardar o atributo .latlng ao clicar no mapa.
var x;                                              // Varíavel que irá guardar a coordenada .lat ao clickar no mapa.
var y;                                              // Varíavel que irá guardar a coordenada .lng ao clickar no mapa.

var firstObj;                                       // Varíavel que irá guardar o primeiro objeto interagido em determinados casos.
var firstObjCustom;                                 // Varíavel que irá guardar o segundo objeto interagido em determinados casos.

const LineString = 1;                               // Salvar em varíavel global o número 1 como LineString.
const Polygon = 2;                                  // Salvar em varíavel global o número 2 como Polygon.

// Todos os objetos inputs e labels + as funções que chamam //
const savePointBtn = "<input value='Salvar' type='submit' OnClick='submitPoint(x,y)'>";
const saveLineBtn = "<input value='Salvar' type='submit' OnClick='submitLine()'>";
const savePolygonBtn = "<input value='Salvar' type='submit' OnClick='submitPolygon()'>";
const editBtn = "<input value='Editar' type='submit' id='editar' OnClick='editar()'>";
const alterarBtn = "<input value='Alterar' type='submit' id='editar' OnClick='alterar()'>";
const nameInput = "<input placeholder='nome' value='' type='text' id='nome'>";
const descInput = "<input placeholder='descrição' value='' type='text' id='desc'>";
const selectBtn = "<input value='Selecionar' type='submit' OnClick='selectCoord()'>";
const deleteBtn = "<input value='Deletar' type='submit' OnClick='deleteObj()'>";
const unSelectBtn = "<input value='Desmarcar' type='submit' OnClick='unSelect()'>";
const createLineBtn = "<input value='Criar linha' type='submit' OnClick='createLine()'>";
const createPolygonBtn = "<input value='Criar Poligono' type='submit' OnClick='createPolygon()'>";
const createCircleInput = "<input placeholder='0.00' value='' type='text' id='raio'>";
const checkBtn = "<input value='Gerar' type='submit' OnClick='check()'>";
const distanceBtn = "<input value='Distância' type='submit' OnClick='distance()'>";
const linhasBtn = "<input value='Consultar Linhas' type='submit' OnClick='linhasCheck()'>";
const poligonosBtn = "<input value='Consultar Poligonos' type='submit' OnClick='poligonosCheck()'>";
const pontosBtn = "<input value='Consultar Pontos' type='submit' OnClick='pontosCheck()'>";
const customSelectBtn = "<input value='Interagir' type='submit' OnClick='customSelect()'>";
const customUnSelectBtn = "<input value='Refazer' type='submit' OnClick='customUnSelect()'>";
const intersectionBtn = "<input value='Analisar' type='submit' OnClick='analysisPoly()'>";
const createMarkerBtn = "<input value='Criar Ponto' type='submit' OnClick='createPonto()'>";
const progbar = document.getElementById('progressbar')

var categoriaInput = "<input list='categorias' id='categoriasinput' placeholder='categoria'><datalist id='categorias'>";
var nameLabel = '<strong>Nome:</strong>';
var descLabel = '<strong>Descrição:</strong>';
var categoriaLabel = '<strong>Categoria:</strong>';
var raioLabel = "<strong>Raio:</strong>";
var editLabel = '<strong>Editar:</strong>'
var brLabel = '<br>';


// Pegar da varíavel global settings algumas configurações globais: ver settings.py
const endpoint = settings['ENDPOINT'];
const loadingInterval = settings['LOADING_INTERVAL'] // intervalo em Milisegundos de diferença para desenhar cada objeto no mapa.

// Header utilizado em todas as requisições que serão feitas.
const header = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    "Authorization" : "Bearer " + token 
}

// Demais endpoints 
const pontos = "pontos/";
const poligonos = "poligonos/";
const linhas = "linhas/";
const categorias = "categorias/"


// Definindo varíavels para comparação de tipos por meio do atributo .options.alt dos objetos.
const marker = "Point";
const polygon = "Polygon";
const line = "LineString";


// Por padrão definir alguns objetos iniciais para interação nas listas de objetos selecionados.
selectedObjs.polys = new Object;
selectedObjs.polys.length = new Number;
selectedObjs.markers = new Object;

const map = L.map('map').setView([-7.158689, -34.855069], 15);            // Definir o mapa nas coordenadas iniciais e zoom inicial
map.on('contextmenu', onMapClick);                                       // Abrir menu context com o botão direito do mouse.

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{       // Definir qual template de mapa será utilizado.
    maxZoom: 19,                                                         // Zoom máximo permitido.
    minZoom: 7,                                                          // Zoom mínimo permitido.
    attribution: '© OpenStreetMap'                                       // Footer.
}).addTo(map);                                                           // Adicionar ao mapa.


loading();       // Chamar a função de loading