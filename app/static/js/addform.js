addInputForm()

function addInputForm()
{
    var div_element = document.createElement("div");
    div_element.innerHTML = '<form class="form-inline"><div class="form-group"><label class="control-label" for="focusedInput">経由地</label><input class="form-control" id="focusedInput" type="text"></div></form> ';
    var parent_object = document.getElementById("piyo");
    parent_object.appendChild(div_element);
}


