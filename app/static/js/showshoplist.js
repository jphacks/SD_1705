addShopList(store);

function addShopList(store){
    for(var i = 0; i < store.length; i++){
        document.write("<tr>");
        
        document.write("<td><a style=width:100%; height:100%; display:block; href=" + store[i].url + ">");
        document.write(store[i].name);
        document.write("</a></td>"); 

        document.write("<td>");
        document.write(store[i].budget);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].genre);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].open);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].parking);
        document.write("</td>"); 

        document.write("</tr>");
    }
}