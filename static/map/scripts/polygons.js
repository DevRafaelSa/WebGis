//# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 06/07/2022                    #            
//#########################################################

// Função assincrona que carrega os poligonos
async function loadPolygons(){
    let url = endpoint + poligonos;    // Salvar a url para ser utilizado em um request.
    let data = await get(url);       // Fazer um request do tipo get na url.
    for (let obj in data){
        let poylgon = await drawPolygon(data[obj]); // Desenhar o objeto (Poligono) que foi recebido do request.
    };
    progbar.style.background = 'linear-gradient(to right, #4cf24c 75%, #4cf24c 75%, #bcb9b9 0%)' // Após a conclusão aumentar para 75% o carregamento da tela de loading.
}


// Essa função desenha em sí um objeto que foi recebido de um request, ou passando um JSON com as informações.
async function drawPolygon(data){
    return new Promise(resolve => {
        setTimeout(() =>{
            let poly = L.geoJSON(data.coordenadas, {color: 'blue'}).addTo(map).on('click', onSavedPolygonClick); // Desenhar no formato geoJSON, pois já inverte as coordenadas.
            poly.name = data.name;
            poly.desc = data.desc;
            poly.categoria = Icons[data.categoria].options.name;
            poly.categoria_id = data.categoria;
            poly.coordinates = data.coordenadas.coordinates;
            poly.id = data.id;
            poly.options.alt = polygon;
            resolve(poly)
        }, loadingInterval);      // Fazer todo o processo com um intervalo de tempo definido no back settings.py.
    });
}


// Função que cria poligonos a partir dos pontos selecionados, mas não salva no banco de dados.
function createPolygon(){
    let polygon = L.polygon(selectedCoords, {color: 'blue'}).addTo(map).on('click', onPolygonClick);  
    let popup = selectedObj._popup;
    let content = popup.getContent();
    popup.setContent(content.replace(createPolygonBtn, ''));
    popup.close();
    // resetar ambiente 
    selectedObj = [];
    selectedCoords = [];
    markersReset(); 
}


// Função que é chamado após clicar em poligonos não salvos no banco de dados.
// Obs: Por se tratar de um poligono é necessário criar o popup no mapa e não no objeto, ou seja no local em que o mouse clicou, pois o objeto não guarda todos os pontos em que ele está desenhado, apenas alguns pontos das suas arestas. Ler Observação 3 no tópico importante do map.js.
function onPolygonClick(e){
    let popupPolygon = L.popup();
    let zoom = map.getZoom().toString() 
    selectedObj = e.target;        // Ler observação
    popupPolygon.setLatLng(e.latlng);   // Ler observação
    popupPolygon.setContent("Você clicou em um poligono" + "Zoom:" + zoom + brLabel + nameInput + descInput + categoriaInput + savePolygonBtn + deleteBtn);
    popupPolygon.openOn(map);
    popup = popupPolygon;   // Definir globalmente que o poligono clickado é esse
}


// Função que é chamada após clicar no botão Salvar do popup do poligono não salvo no banco de dados.
async function submitPolygon(){
    let name = document.querySelector('#nome').value;          // Pegar nome do input.
    let desc = document.querySelector('#desc').value;            // Pegar descrição do input.
    let category = document.querySelector('#categoriasinput').value;     // Pegar descrição do input.
    category = Icons[category].id                   // Pegar o id da categória através do nome que foi dado.

    refreshCoords(false, Polygon);                  // Atualizar as coordenadas passando o parâmetro de clique no mapa como falso e que será um poligono o objeto.
    let coordenadas = selectedCoords;               // As coordenadas será igual as coordenadas selecionadas.
    let url = endpoint + poligonos;
    let bodyJson = {
        "name": name,
        "desc": desc,
        "categoria": category,
        coordenadas
    };

    let data = await post(url, bodyJson);
    // Alterar o objeto que já está no mapa para os dados do poligono que foi salvo no banco de dados.
    selectedObj.name = data.name;      
    selectedObj.desc = data.desc;
    selectedObj.categoria_id = data.categoria;
    selectedObj.categoria = Icons[data.categoria].options.name;
    selectedObj.coordinates =  coordenadas.coordinates;
    selectedObj.options.alt = polygon;
    selectedObj.id = data.id;
    selectedObj.on('click', onSavedPolygonClick);    
    popup.close();
    selectedCoords = [];
    alert("Criado com sucesso.");

}


// Função que é chamada ao clicar em um poligono salvo no banco de dados.
function onSavedPolygonClick(e){
    refreshCoords(e);         // Mudar as coordenadas para o clique do mouse na tela assim será possível criar um popup no local e referenciar o poligono ao mesmo tempo.
    let popupPolygon = L.popup();
    let zoom = map.getZoom().toString();
    selectedObj = e.target;           // O popup é criado onde o mouse clicou, contudo o objeto a ser selecionado é o poligono em sí.
    popupPolygon.setLatLng(e.latlng);  
    content = "Você clicou em um poligono" + "Zoom:" + zoom + brLabel + nameLabel + selectedObj.name + editBtn + brLabel + descLabel + selectedObj.desc + brLabel + categoriaLabel + selectedObj.categoria + brLabel;
    content = polyContentCheck(content);  // Checar conteúdo para filtragem necessária.
    popupPolygon.setContent(content);
    popupPolygon.openOn(map);
    popup = popupPolygon;
}


// Essa função é chamada toda vez que um poligono salvo no banco de dados é clickado e é utilizada nos popups afim de constumizar conforme a necessidade.
function polyContentCheck(content){
    if (selectedObjs.polys.length == 0){           // Se não há nenhum poligono selecionado
        content += customSelectBtn + deleteBtn + pontosBtn;
    }
    else if(selectedObjs.polys.length == 1){      // Se há pelo menos um poligono selecionado
        if(selectedObjs.polys[selectedObj.id]){
            content += customUnSelectBtn + deleteBtn + pontosBtn;
        }
        if (firstObjCustom !== selectedObj){
            content += intersectionBtn;
        }
    }
    else{   // Caso seja maior que um ou menor que 0 (até o presente momento  que essa documentação foi escrita é impossível isso ocorrer).
        content += deleteBtn + pontosBtn;
    }
    return content;
}