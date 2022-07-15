//# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//#
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 07/07/2022                    #            
//#########################################################

// Função assincrona para carregar as linhas.
async function loadLines(){
    let url = endpoint + linhas; // Preparando url.
    let data = await get(url);   // Fazer o request na url.
    for (let obj in data){       // Para cada objeto presente.
        let polyline = await drawPolyLine(data[obj]);           // Chamar a função que desenha a linha em sí.
    };
    progbar.style.background = 'linear-gradient(to right, #4cf24c 100%, #4cf24c 100%, #bcb9b9 0%)'  // Aumentar para 100% o carregamento após a finalização.
}


// Função responsável por desenhar no mapa as linhas em sí.
// Obs: Ler Observação 3 no tópico importante do map.js.
async function drawPolyLine(data){
    return new Promise(resolve =>{
        setTimeout(() => {
        // Preparar inversão de lnglat para latlng no formato leaflet.
        let coords = data.coordenadas.coordinates;
        let coordinates = new Array(); // Array que será responsável por guardar as coordenadas em latlng.
        for (let coord in coords){
            let lat = coords[coord][1];  // Pegar o segundo valor das coordenadas na data.
            let lng = coords[coord][0];  // Pegar o primeiro valor das coordenadas na data.
            coord = new Array();
            coord.push(lat, lng)
            coordinates.push(coord);   // Por na array essa coordenada latlng.
        };

        var lineName = data.name;
        var lineDesc = data.desc;
        var lineCategoria = data.categoria;
        var id = data.id;

        let polyline = L.polyline(coordinates, {color: 'red'}).addTo(map).on('click', onSavedLineClick);
        polyline.name = lineName;
        polyline.desc = lineDesc;
        polyline.categoria_id = lineCategoria;
        polyline.categoria = Icons[lineCategoria].options.name;
        polyline.coordinates = data.coordenadas.coordinates;
        polyline.id = id;
        polyline.options.alt = line;
        resolve(polyline);
        }, loadingInterval) // Fazer todo o processo com um intervalo de tempo definido no back settings.py.
    });
}


// Função responsável por criar uma linha não salva no banco de dados.
function createLine(){
    let polyline = L.polyline(selectedCoords, {color: 'red'}).addTo(map).on('click', onLineClick);
    let popup = selectedObj._popup; // Pegar o popup ainda em exibição na tela do usuário.
    let content = selectedObj._popup.getContent();
    popup.setContent(content.replace(createLineBtn, '')); // Retirar o botão de criar linha do popup ainda em exibição.
    popup.close(); // Fechar popup
    selectedObj = [];
    selectedCoords = [];
    markersReset();
}


// Função responsável por criar o popup após ser clicado em uma linha.
// Obs: Por se tratar de uma linha é necessário criar o popup no mapa e não no objeto, ou seja no local em que o mouse clicou, pois o objeto não guarda todos os pontos em que ele está desenhado, apenas alguns pontos das suas arestas. Ler Observação 3 no tópico importante do map.js.
function onLineClick(e){
    selectedObj = e.target;
    let zoom = map.getZoom().toString();
    let popupLine = L.popup();
    popupLine.setLatLng(e.latlng); // Setar o popup no local em que o mouse clicou e não no objeto em sí.
    popupLine.setContent("Você clicou em uma linha " + "Zoom:" + zoom + brLabel + nameInput + descInput + categoriaInput + saveLineBtn + deleteBtn);
    popupLine.openOn(map);
    popup = popupLine
    popupLine.options.alt = line;
}


// Função responsável por salvar no banco de dados uma linha.
async function submitLine(){
    let name = document.querySelector('#nome').value;
    let desc = document.querySelector('#desc').value;
    let category = document.querySelector('#categoriasinput').value;
    category = Icons[category].id


    // Realizar a atualização dos coordenadas passando false para clique na tela e que é uma linha como parâmetros.
    refreshCoords(false, LineString);
    let url = endpoint + linhas
    let bodyJson = {
        "name": name,
        "desc": desc,
        "categoria": category,
        "coordenadas": {
            "type": "LineString",
            "coordinates": 
                selectedCoords
        }
    }

    let data = await post(url, bodyJson);

    selectedObj.name = data.name;
    selectedObj.desc = data.desc;
    selectedObj.categoria_id = data.categoria;
    selectedObj.categoria = Icons[data.categoria].options.name;
    selectedObj.coordinates = selectedCoords;
    selectedObj.id = data.id;
    selectedObj.options.alt = line;
    selectedObj.on('click', onSavedLineClick);

    popup.close();
    selectedCoords = [];
    alert('criado com sucesso.');
}


// Função responsável por criar o popup quando se é clicado em uma região dentro da linha.
// Obs: Por se tratar de uma linha é necessário criar o popup no mapa e não no objeto, ou seja no local em que o mouse clicou, pois o objeto não guarda todos os pontos em que ele está desenhado, apenas alguns pontos das suas arestas. Ler Observação 3 no tópico importante do map.js.
function onSavedLineClick(e){
    refreshCoords(e);
    selectedObj = e.target;  
    let zoom = map.getZoom().toString();
    let popupLine = L.popup();
    popupLine.setLatLng(e.latlng); // Setar as coordenadas no local do clique do mouse e não na linha em sí. 
    popupLine.setContent("Você clicou em uma linha " + "Zoom:" + zoom + brLabel + nameLabel + selectedObj.name + editBtn + brLabel + descLabel + selectedObj.desc + brLabel + categoriaLabel + selectedObj.categoria + brLabel + deleteBtn + linhasBtn + poligonosBtn);
    popupLine.openOn(map);
    popup = popupLine;
}