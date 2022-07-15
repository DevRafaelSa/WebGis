//# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//#
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 07/07/2022                    #            
//#########################################################

// Função assincrona para carregar as linhas.
async function loadPoints(){
    let url = endpoint + pontos; // Preparando url.
    let data = await get(url);  // Fazer o request na url.
    for(let obj in data){        // Para cada objeto presente.
        let Marker = await createMarker(data[obj]);  // Chamar a função que desenha o ponto em sí.
        };
    progbar.style.background = 'linear-gradient(to right, #4cf24c 50%, #4cf24c 50%, #bcb9b9 0%)'  // Aumentar para 50% a tela de carregamento.
}


// Funçõo assincrona responsável por desenhar os pontos em questão no mapa utilizando-se dados em json.
async function createMarker(data){
    return new Promise(resolve =>{
        setTimeout(() => {
            let lat = data.coordenadas.coordinates[1];
            let lng = data.coordenadas.coordinates[0];
            let pointName = data.name;
            let pointDesc = data.desc;
            let pointCategory = Icons[data.categoria].options.name;
            let pointCategory_id = data.categoria;
            let id = data.id;
            let m = L.marker([lat, lng], { icon:Icons[pointCategory_id], draggable: true }).addTo(map).bindPopup(nameLabel + pointName + editBtn + brLabel + descLabel + pointDesc + brLabel + categoriaLabel + pointCategory + brLabel + raioLabel + createCircleInput + checkBtn + brLabel +  selectBtn).on('click moveend', eventHandler);
            m.id = id;
            m.name = pointName;
            m.desc = pointDesc;
            m.categoria = pointCategory;
            m.categoria_id = pointCategory_id;
            m.coordinates = data.coordenadas.coordinates;
            m.options.alt = marker;
            Markers[m.id] = m;
            resolve(m);
        }, loadingInterval);    // Fazer todo o processo com um intervalo de tempo definido no back settings.py.
    });
}

// Função que serve para checar qual tipo de evento está ocorrendo no marker.
function eventHandler(e){
    let event = e.type;  // Pegar o tipo do evento;
    let popup = e.target._popup;

    if (event === 'moveend'){  // Caso seja ao final de arrastar o marker.
        popup.openOn(map);
        changeMarker(e);
        onMarkClick(e);
    }
    else if(event === 'click'){ // Caso seja um simples clique.
        onMarkClick(e);
    }
}

// Ao clicar em um marker não salvo no banco de dados.
function onUnSavedMarkClick(e){
    selectedObj = e.target;
    refreshCoords(selectedObj);
}

// Resetar os icones dos markers após algum processo.
function markersReset(){
    for(let marker in selectedObjs.markers){
        let icon = selectedObjs.markers[marker]._icon;
        icon.classList.remove('marker-selected');  // Retirar a classe css que é responsável por criar círculos amarelos.
        let popup = selectedObjs.markers[marker]._popup;
        let content = popup.getContent();
        content = content.replace(unSelectBtn, selectBtn);
        popup.setContent(content);
        delete(selectedObjs.markers[marker]);  // Deletar da lista de objetos selecionados o marker.
    }
}


// Função que é chamada após clicar no marker e gerir o popup.
function onMarkClick(e){
    selectedObj = e.target; 
    let content = selectedObj._popup.getContent();

    // Gestão do popup // 
    if (selectedCoords.length == 0){ // Caso nenhuma coordenada tenha sido selecionada.
        content = content.replace(createLineBtn, '');
        content = content.replace(createPolygonBtn, '');
        content = content.replace(unSelectBtn, '');
        content = content.replace(distanceBtn, '')
        firstObj = undefined;
        secondObj = undefined;
        if (!content.includes(selectBtn)){
            content += selectBtn;
        }
        if (!content.includes(deleteBtn)){
            content += deleteBtn;
        }
        if(!content.includes(linhasBtn)){
            content += linhasBtn;
        }
    }
    else if (selectedCoords.length == 1){ // Caso tenha uma coordenada selecionada.
        content = content.replace(createLineBtn, '');
        content = content.replace(createPolygonBtn, '');
        content = content.replace(deleteBtn, '')
        if (selectedObj !== firstObj && !content.includes(distanceBtn)){
            content += distanceBtn;
        }
    }
    else if (selectedCoords.length > 1){ // Caso mais de uma coordenada seja selecionada.
        if (content.includes(distanceBtn)){
            content.replace(distanceBtn, '');
        }
        if (selectedCoords.length >=3){ // Caso tenham mais ou apenas 3 coordenadas selecionadas.
            if(selectedObj === firstObj){
                if (!content.includes(createPolygonBtn)){
                    content += createPolygonBtn;
                }
            }
        }
    }
    selectedObj._popup.setContent(content);    // Definir o novo conteúdo do popup.
}

// Função responsável por salvar no banco de dados um ponto.
async function submitPoint(x, y){
    let lat = y;
    let lng = x;
    let name = document.querySelector('#nome').value;
    let desc = document.querySelector('#desc').value;
    let category = document.querySelector('#categoriasinput').value;
    category = Icons[category].id

    let url = endpoint + pontos;
    
    let bodyJson = {
        "name": name,
        "desc": desc,
        "categoria": category,
        "coordenadas": {
            "type": "Point",
            "coordinates": [
                lat,
                lng
            ]
        }
    };

    let data = await post(url, bodyJson);
    popup.close();
    alert("Criado com sucesso.")
    createMarker(data); // Desenhar o marker em questão.
    if(selectedObj){ // Caso tenha algum objeto selecionado mo mapa retirar ele, pois possivelmente ele será substituído por esse marker.
        map.removeLayer(selectedObj);
        selectedObj = undefined;
    }
}	

// Função que é chamada ao finalizar o arrasto de um ponto salvo no banco de dados.
async function changeMarker(e){
    selectedObj = e.target;
    let name = selectedObj.name;
    let desc = selectedObj.desc;
    let category = selectedObj.categoria_id;
    let id = selectedObj.id.toString() + '/';
    let url = endpoint + pontos + id;
    let x = selectedObj._latlng.lng;
    let y = selectedObj._latlng.lat;

    let bodyJson = {
        "name": name,
        "desc": desc,
        "categoria": category,
        "coordenadas": {
            "type": "Point",
            "coordinates": [
                x,
                y
            ]
        }
    };

    let dados = await put(url, bodyJson);
    selectedObj.coordinates = dados.coordenadas.coordinates; // Mudar as coordenadas para o novo local.
}