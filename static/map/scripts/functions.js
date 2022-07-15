//# Obs:  Afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//# Obs2: Nem tudo fora explicado detalhadamnete, pois o repetimento de informações faz-se desnecessário. Recomenda-SE entendimento do que está fazendo.
//#
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 07/07/2022                    #            
//#########################################################
// Função responsável por gerir todos os loadings dos objetos do mapa
async function loading(){
    await loadIcons();
    await loadPoints();
    await loadPolygons();
    await loadLines();
    await renderMap();
}


// Função responsável por retirar a tela de loading e mostrar o mapa.
async function renderMap(){
    return new Promise(resolve => {
        setTimeout(() => {
            let loading = document.getElementById('loading')
            loading.remove() // Remover a tela em sí.
        }, loadingInterval); // Fazer todo o processo com um intervalo de tempo definido no back settings.py.
    })
}


// Função que é chamada após clicar no botão editar.
function editar(){
    let type = selectedObj.options.alt; // Pegar o tipo do objeto.
    if (type === marker){  // Caso seja um marker.
        popup.setLatLng(selectedObj._latlng);  // Criar um novo popup global baseado no popup do marker.
        selectedObj._popup.close(); // Fechar o popup do marker.
        popup.openOn(map); // Abrir o novo popup.
        
        url = endpoint + pontos + selectedObj.id + '/'
    }
    else if(type === line){
        url = endpoint + linhas + selectedObj.id + '/'
        
    }
    else if(type === polygon){
        url = endpoint + poligonos + selectedObj.id + '/'
    }

    let content = popup.getContent(); // Pegar o conteúdo do popup global.
    content = editLabel + brLabel + nameLabel + nameInput + brLabel + descLabel + descInput + brLabel + categoriaLabel + categoriaInput + alterarBtn; // Adicionar o conteúdo de edição.
    selectedObj.endpoint = url;  // Salvar no objeto o endpoint para edição.
    popup.setContent(content); // Setar o conteúdo do popup.
}


// Função que é chamada após o clique no botão Alterar dentro do popup de edição.
async function alterar(){
    let name = document.querySelector('#nome').value;
    let desc = document.querySelector('#desc').value;
    let categoria = document.querySelector('#categoriasinput').value;
    let type = selectedObj.options.alt;
    let id = Icons[categoria].id;
    let coordinates = selectedObj.coordinates; // Pegar as coordenadas do objeto já invertidas pelo seu atributo.
    let bodyJson = {
        "name": name,
        "desc": desc,
        "categoria": id,
        "coordenadas": {
            "type": type,
            "coordinates": coordinates
        }
    };
    let data = await put(selectedObj.endpoint, bodyJson);
    if (selectedObj._popup){ // Caso o objeto tenha um popup interno.
        delete[Markers[selectedObj.id]];
        let m = await createMarker(data) // Desenhar um novo popup apartir dessa edição.
        map.removeLayer(selectedObj); // Remover o antigo objeto.
    }
    selectedObj.name = name;
    selectedObj.desc = desc;
    selectedObj.categoria = categoria;
    selectedObj.categoria_id = id;
    alert('Alterado com sucesso.');
    popup.close();
    selectedObj = [];
}

// Função que é chamada após o clique com o botão direito no mouse em qualquer canto do mapa.
function onMapClick(e) {
    let zoom = map.getZoom().toString();
    refreshCoords(e);
    popup.setLatLng(coord);
    popup.setContent("Você clicou no mapa em " + brLabel + coord.toString() + brLabel + " Zoom: " + zoom + '<br>' + nameInput + descInput + categoriaInput + savePointBtn);
    popup.openOn(map);
    selectedObj = [];
}


// Função repsonsável por gerir as coordenadas globais.
// Obs: Essa é uma das funções que primeiramente foi feita pensada de determinada forma, contudo conforme a aplicação escalou ela sofreu mudanças, mas em um futuro recomenda-se o completo refatoramento dessa função.
// Obs2: A função toGeoJson() do proprio leaflet já consegue gerir esse inversamento de coordenadas para outro formato, logo essa função é totalmente depreciada e pode causar futuros atrasos!
function refreshCoords(Click, obj){  // Passar parâmetros de clique no mapa ou não (True or False: boolean), e o tipo de objeto que você clicou.

    if(selectedObj){ // Caso exista um objeto clickado.
        if (obj == LineString){ // Caso a função tenha o parâmetro para indicar que é uma linha.
            for (let obj in selectedObj._latlngs){
                  let x = selectedObj._latlngs[obj].lng;
                  let y = selectedObj._latlngs[obj].lat;
                  let coordinates = new Array();
                coordinates.push(x,y);
                selectedCoords.push(coordinates);
            };
        } 
        else if (obj == Polygon){ // Caso tratar-se de um poligono.
                let geoJsonObj = selectedObj.toGeoJSON(); // Chamar a função que já faz o invertimento das coordenadas para lnglat. 
                selectedCoords = geoJsonObj.geometry;
        } 
    }

    // Caso seja um clique no mapa.
    if (Click){
        coord = Click.latlng;
        if(!coord){
            coord = Click._latlng;
        }
        x = coord.lat;
        y = coord.lng;
    }
    
}


// Função que é utilizada no selecionamento constumizados e possível ser utilizado em futuras features, sendo ela escalavel e separada do select de Markers.
function customSelect(){
    let type = selectedObj.options.alt; // Pegar o tipo do objeto selecioando.
    if (type === polygon){  // Caso um poligono.
        if (selectedObjs.polys.length == 0){
            selectedObjs.polys[selectedObj.id] = selectedObj;
            selectedObjs.polys.length += 1;
            selectedObj.setStyle({color :'green'});
            firstObjCustom = selectedObj; // Primeiro objeto clickado. (escalável)
            popup.close();
        }
    }
}


// Função que gere o deselecionamento constumizado utilizado em objetos que não sejam markers.
function customUnSelect(){
    let type = selectedObj.options.alt;
    if (type === polygon){
        if (selectedObjs.polys[selectedObj.id]){
            delete(selectedObjs.polys[selectedObj.id]);
            selectedObj.resetStyle();
            selectedObjs.polys.length -= 1;
            popup.close();
        }
    } 
}


// Função que é chamada após clicar no botão selecionar em popups.
function selectCoord(){
    let coordinates = new Array();
    let x = selectedObj._latlng.lat;
    let y = selectedObj._latlng.lng;
    let icon = selectedObj._icon;
   
    coordinates.push(x,y);
    selectedCoords.push(coordinates);

    let content = selectedObj._popup.getContent(); // Gerir o popup do marker.
    if (selectedCoords.length == 1){ // Caso apenas um marker seja selecionado.
        if(!content.includes(unSelectBtn)){
            content = content.replace(selectBtn, unSelectBtn);
            firstObj = selectedObj;
        }
        if (content.includes(deleteBtn)){
            content = content.replace(deleteBtn, '');
        }
        if (content.includes(linhasBtn)){
            content = content.replace(linhasBtn, '');
        }
    }
    else if(selectedCoords.length > 1){ // Caso mais de um seja selecionado.
        if (!content.includes(unSelectBtn)){
            content = content.replace(selectBtn, unSelectBtn);
        }
        if(!content.includes(createLineBtn)){
            content += createLineBtn;
        }
        if (content.includes(deleteBtn)){
            content = content.replace(deleteBtn, '');
        }
        if (content.includes(distanceBtn)){
            content = content.replace(distanceBtn, '');
        }
    }
    selectedObj._popup.setContent(content);
    icon.classList.add('marker-selected'); // Adicionar a classe css que gera uma borda amarela.
    selectedObjs.markers[selectedObj.id] = selectedObj;
}


// Função que gere o deselecionamento de markers após clicar no botão deselecionar dos popups.
function unSelect(){
    let lat = selectedObj._latlng.lat;
    let lng = selectedObj._latlng.lng;
    let icon = selectedObj._icon;
    let content = selectedObj._popup.getContent();
    for (let coord in selectedCoords){ // Procura as coordendas do objeto nas coordenadas selecionadas globalmente e remove-las.
        if (selectedCoords[coord].includes(lat) && selectedCoords[coord].includes(lng)){ // Caso seja encontrada.
            selectedCoords.splice(coord, 1);
            content = content.replace(unSelectBtn, selectBtn);
            selectedObj._popup.close();
            selectedObj._popup.setContent(content);
            break; // Parar o looping, pois foi encontrada.
        }
    };
    icon.classList.remove('marker-selected');
    delete(selectedObjs.markers[selectedObj.id]);
}


// Função que é chamada após o clique no botão deletar dos popups de todos os objetos.
async function deleteObj(){
    let confirmation = confirm("Você tem certeza?");
    if (!confirmation){
        return;
    }
    let id = selectedObj.id;
    let url;
    if (id){
        let type = selectedObj.options.alt;
        if (type === marker){
            delete(Markers[id])
            url = endpoint + pontos + id + '/';
        }
        else if(type === line){
            url = endpoint + linhas + id + '/';
        }
        else if(type === polygon){
            url = endpoint + poligonos + id + '/'; 
        }
    }
    await deleteFromDatabase(url);
    alert('Objeto deletado com sucesso.');
    popup.close();
    map.removeLayer(selectedObj);
}


// Função que é chamada após clicar no botão gerar dos markers.
async function check(){
    let id = selectedObj.id.toString();
    let radius = document.querySelector('#raio').value;
    let raio = '/raio=';
    let url = endpoint + pontos + id + raio + radius;
    let data = await get(url);
    let circle = L.circle(selectedObj._latlng);
    circle.setRadius(Number(radius));
    circle.inside = new Object;
    circle.categorias = new Array;
    let length = 0;
    for (let obj in data){
        length += 1
        let id = data[obj].id;
        circle.inside[id] = Markers[id];
        circle.categorias.push(Markers[id].categoria);
    }
    circle.length = length;
    circle.on('click', radiusClick);
    circle.addTo(map);
    selectedObj._popup.close();
}


// Função que é chamada após o clique no círculo que é formado após clicar no botão gerar.
function radiusClick(e){
    selectedObj = e.target;
    let zoom = map.getZoom().toString();
    let length = selectedObj.length;
    let radius = selectedObj._mRadius;
    let content = "Há apenas um ponto em um raio de " + radius + " metros" + brLabel;
    if (length > 1){
        content = "Há cerca de " + length.toString() + " pontos" + " em um raio de " + radius + " metros" + brLabel;
    }
    content += categoriaLabel + selectedObj.categorias;
    refreshCoords(e);
    popup.setLatLng(coord);
    popup.setContent("Você clicou em um círculo em " + brLabel + coord.toString() + brLabel + "Zoom:" + zoom + brLabel + content + brLabel + deleteBtn);
    popup.openOn(map);
}


// Função que é chamda após o clique no botão distância dos popup dos markers.
async function distance(){
    let firstId = firstObj.id + '/'
    let secondId = selectedObj.id + '/'
    let url = endpoint + pontos + firstId + secondId
    let data = await get(url);
    let distance = data.distance
    distance = Math.round(distance)
    selectedObj._popup.close()
    alert('Os pontos estão a ' + distance + " metros de distância");
}


// Função que checa os tipos do objeto e em seguida mescla mensagens conforme o seu tipo.
function checkObjType(obj){
    var msg;
    var msg2;
    var target;
    
    if (obj.options.alt === marker){
        target = pontos;
        msg = "Esse ponto está sob influência de ";
    }
    else if (obj.options.alt === line){
        target = linhas;
        msg = "Essa linha está sendo tocada ou cruzada por ";
        msg2 = "Essa linha está inserida ou cruzando "
    }
    else if (obj.options.alt === polygon){
        target = poligonos;
        msg = "Esse poligono contem ";
    }
    return [target, msg, msg2]; // retorno de uma array com as mensagens.
}


// Função utilizada para checar a mensagem e concatenar os dados recebidos do request.
async function objChecker(url, msg){
    let data = await get(url);
    if (!data || data.length === 0){
        if (popup){
            popup.close();
        }
        else{
            selectedObj._popup.close();
        }
        alert('Não há dados para mostrar.')
        return;
    }
    let count = 1;
    for (let obj in data){
        obj = data[obj];
        if (count >1){
            msg += ",";
        }
        msg += obj.name
        if (count == data.length){
            msg += '.';
        }
        else{
            count += 1;
        }
    }
    alert(msg);
}

// Função feita exclusivamente na análise de poligonos.
async function analysisPoly(){
    let id1 = firstObjCustom.id + '/';
    let id2 = selectedObj.id + '/';
    let url = endpoint + poligonos + id1 + id2;
    let data = await get(url);
    let msg;
    if (!data || data.length === 0){
        popup.close();
        alert('Não há dados para mostrar.')
        return;
    }
    else if(data && data.length >= 0){
        msg = firstObjCustom.name + ' e ' + selectedObj.name + ' são ';
        for(let obj in data){
            if(data[obj].vizinhos){
                msg += "vizinhos.";
            }
            if(data[obj].contains){
                msg += ' Um está inserido no outro.';
            }
            if (data[obj].intersects){
                msg += ' As áreas apresentam intersecção e serão gerados no mapa.';
            }
            if (data[obj].intersection_points){
                var coordinates = data[obj].intersection_points;
            }
        };
        alert(msg);

        popup.close();
        selectedObjs.polys = new Object;
        selectedObjs.polys.length = new Number;
        selectedObj = undefined;
        firstObjCustom.setStyle({color: 'blue'});
        let generate = await generateUnSavedMakers(coordinates);
    }
}

// Função que é chamada após a análise de poligonos e existência de pontos de intersecção.
function generateUnSavedMarker(point){
    let lat = point[1];
    let lng = point[0];
    let marker = L.marker([lat, lng]).addTo(map).bindPopup("Você clicou em um ponto" + brLabel + nameInput + descInput + categoriaInput + savePointBtn + deleteBtn).on('click', onUnSavedMarkClick);
}

// Função que recebe as coordendas e em seguida individualmente gera os pontos.
async function generateUnSavedMakers(coordinates){
    for(let obj in coordinates){
        let point = coordinates[obj];
        generateUnSavedMarker(point);
    };
}

// Função que é chamada após clicar no botão Consultar poligonos.
async function poligonosCheck(){
    let id = selectedObj.id + '/';
    let checker = checkObjType(selectedObj);
    let target = checker[0];
    let url = endpoint + target + id + poligonos;
    let msg = checker[2];
    objChecker(url, msg);
}

// Função que é chamada após o clique no botão consultar linahs.
async function linhasCheck(){
    let id = selectedObj.id + '/';
    let checker = checkObjType(selectedObj);
    let target = checker[0];
    let url = endpoint + target + id + linhas;
    let msg = checker[1];
    objChecker(url, msg);
}

//Função que é chamada após o clique em consultar pontos.
async function pontosCheck(){
    let id = selectedObj.id + '/';
    let checker = checkObjType(selectedObj);
    let target = checker[0];
    let url = endpoint + target + id + pontos;
    let msg = checker[1];
    objChecker(url, msg);
}

///  REQUESTS HANDLERS ///

// Obs: Aqui ficam gereciamento dos requests que recebem a url e o body e apenas pega da varíavel global o header.
// CRUD
// C
async function post(url, bodyJson) {
    var response = await fetch(url, {
      method: "post",
      headers: header,

      body: JSON.stringify(bodyJson)
        }
    )
    var data = await response.json();
    return data;
}

// R 
async function get(url) {
    var response = await fetch(url, {
      method: "get",
      headers: header
        }
    )
   
    var data = await response.json();
    return data;
}


// U 
async function put(url, bodyJson) {
    var response = await fetch(url, {
      method: "put",
      headers: header,

      body: JSON.stringify(bodyJson)
    }
    )
    var data = await response.json();
    return data;
}


// D

async function deleteFromDatabase(url){
    let response = await fetch(url, {
        method: "delete",
        headers: header
          }
      )
    return response;
}