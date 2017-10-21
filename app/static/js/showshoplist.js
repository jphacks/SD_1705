addShopList(store);

function addShopList(store){
    for(var i = 0; i < store.length; i++){
        document.write("<tr>");
        document.write("<td>");
        document.write(i+1);
        document.write("</td>");
        
        document.write("<td>");
        document.write(store[i].name);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].budget);
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