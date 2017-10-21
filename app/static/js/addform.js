var click_count = 0;
console.log(click_count);

function addInputForm(){
    if(click_count < 8){

        var div_element = document.createElement("div");
        div_element.innerHTML = '<div class="row"><div class="col-xs-3"><div class="form-group"><input class="form-control" placeholder="経由地を入力" size = "15"></div></div></div>';
        var parent_object = document.getElementById("way");
        parent_object.appendChild(div_element);
        click_count++;
        console.log(click_count);
    }
    else{
        alert("経由値は8個までです");
    }
}


