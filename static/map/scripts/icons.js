//# Obs:  afim de menos poluir o código apenas os algoritmos que aprensentarem lógicas alternativas e/ou mais elaboradas serão comentadas. No geral a lógica a ser seguida será a mesma dos exemplos dados nesse cabeçalho.
//# Obs2: É recomendado a utilização de icones redondos de dimensão 16x16 e obrigatoriamente em formato svg.
//#
//#            ###### (Author: Lucas Calado)  #############
//#            #      https://github.com/Kosolov325       #
//#            #      https://gitlab.com/Kosolov325       #          
//#            #      Date: 07/07/2022                    #            
//#########################################################


// Varíavel para definir globalmente o tamanho padrão dos icones que serão usados nas categorias.
var Icon = L.Icon.extend({
    options: {
        iconSize: [16, 16], // Tamanho dos icones.
    }
});


// Função assincrona para carregar os icones.
async function loadIcons(){
        let url = endpoint + categorias;  // Preparando url.
        let data = await get(url);        
        for(let obj in data){     // Para cada categoria presente na data criar um icone.
            obj = data[obj];
            let icon = await createIcon(obj); // Chamar função que carrega o icone.
        };
        categoriaInput += "</datalist>";   // Finalizar a lista de categorias.
        progbar.style.background = 'linear-gradient(to right, #4cf24c 25%, #4cf24c 25%, #bcb9b9 0%)'  // Aumentar para 25% a tela de loading.
}


// Função que é responsável em sí por criar a categoria, o icone e carrego-los na lista.
async function createIcon(obj){
    return new Promise(resolve =>{
       setTimeout(() => {
        let icon = new Icon({    // Instanciar o icone.
            iconUrl: obj.icon,   // Definir o a imagem do icone.
            name: obj.name      // Dar nome ao icone igual ao da categoria.
        })
        Icons[obj.id] = icon;  // Carregar na lista de icones esse icone em especifico, passando seu id como meio de acesso.
        Icons[obj.name] = icon;  // Carregar na lista de icones esse icone em especifico, passando seu nome como meio de acesso.
        Icons[obj.name].id = obj.id; // No objeto que foi carregado pelo seu nome passar também sua id como atributo.
        categoriaInput += "<option value='" + [obj.name] + "'" + '>';  // Adicionar no input de categorias essa nova categoria.
        resolve(icon);
       }, loadingInterval);   // Fazer todo o processo com um intervalo de tempo definido no back settings.py.
    });
}