var click_count = 0;
console.log(click_count);

function addInputForm(){
    if(click_count < 8){
        var way = "way" + click_count;
        var div_element = document.createElement("div");
        div_element.style.textAlign = 'center';
        div_element.innerHTML = '<div class="row" ><div class="form-group"><input class="form-control" name =' + way + ' value ="" placeholder="経由地を入力" size = "15"></div></div>';
        var parent_object = document.getElementById("way");
        parent_object.appendChild(div_element);
        click_count++;
    }
    else{
        alert("経由値は8個までです");
    }
}


