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
        document.write(store[i].type);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].cost);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].time);
        document.write("</td>"); 

        document.write("<td>");
        document.write(store[i].park);
        document.write("</td>"); 

        document.write("</tr>");
    }
}