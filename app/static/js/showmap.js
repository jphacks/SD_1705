var marker = new Array();
var infoWindow = new Array();


function initMap(lat, lng, stores, waypoints, mode) {

  var opts = {
    zoom: 15,
    center: new google.maps.LatLng(lat, lng)
  };
  var map = new google.maps.Map(document.getElementById("map"), opts);

  //addRoute(origin, destination);

  //show fav_restaurants
  for(var i = 0; i < stores.length; i++){
      
    putMarker(i, stores, map);
  
    addInfo(i, stores);

    clickEvent(i);

  }

  var way_dict ={
    'walking': google.maps.DirectionsTravelMode.WALKING,
    'driving': google.maps.DirectionsTravelMode.DRIVING,
    'bicycling': google.maps.DirectionsTravelMode.BICYCLING,
    'transit':google.maps.DirectionsTravelMode.TRNASIT
  }

  way = way_dict[mode]
  console.log(way)

  addRoute(waypoints, map, way)


}

//routeは後
function addRoute(way_points, map, mode){

  var directionsService = new google.maps.DirectionsService;
  var waypts = [];


  for(var i = 0; i < way_points.length; i++){
    waypts.push({location: new google.maps.LatLng(way_points[i].lat, way_points[i].lng)})
  }

  var request = {
    origin: org,
    destination:  des,
    waypoints: waypts,
    travelMode: mode
  }

  directionsService.route(request, function(result, status){
    toRender(result, map);
  })

}

function toRender(result, map){
  directionsDisplay = new google.maps.DirectionsRenderer();
  directionsDisplay.setDirections(result); //取得した情報をset
  directionsDisplay.setMap(map); //マップに描画
}

function putMarker(i, stores, map){
  marker[i] = new google.maps.Marker({
    position: new google.maps.LatLng(stores[i].lat, stores[i].lng),
    map: map
  }); 
}

//show infomation
function addInfo(i, stores){
  infoWindow[i] = new google.maps.InfoWindow({
    content: stores[i].name 
  }); 
}

//show infomation on click 
function clickEvent(i) {
  marker[i].addListener('click', function() {
    infoWindow[i].open(map, marker[i]); 
  });
}