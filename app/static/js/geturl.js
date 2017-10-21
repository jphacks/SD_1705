console.log(getParameter());
console.log(setParameter(getParameter()));

//パラメータを設定したURLを返す
function setParameter( paramsArray ) {
  var resurl = location.href.replace(/\?.*$/,"");
  for ( key in paramsArray ) {
      resurl += (resurl.indexOf('?') == -1) ? '?':'&';
      resurl += key + '=' + paramsArray[key];
  }
  return resurl;
}

//パラメータを取得する
function getParameter(){
  var paramsArray = [];
  var url = location.href; 
  parameters = url.split("#");
  if( parameters.length > 1 ) {
    url = parameters[0];
  }
  parameters = url.split("?");
  if( parameters.length > 1 ) {
    var params   = parameters[1].split("&");
    for ( i = 0; i < params.length; i++ ) {
      var paramItem = params[i].split("=");
      paramsArray[paramItem[0]] = paramItem[1];
    }
  }
  return paramsArray;
};