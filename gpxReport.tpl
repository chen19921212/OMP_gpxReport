
menu-position: 4
---

#$Title

###$StartPoint - $EndPoint
###$StartDate - $EndDate


$NameKeys


<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style> html, body, #map {height:100%; width:100%; padding:0px; margin:0px;}</style>
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.2/leaflet.css" />
<!--[if lte IE 8]><link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.2/leaflet.ie.css" /><![endif]-->

<link rel="stylesheet" href="Res/js/LfElevation/dist/Leaflet.Elevation-0.0.1.css" />

<script type="text/javascript" src="http://cdn.leafletjs.com/leaflet-0.6.2/leaflet.js"></script>
<script type="text/javascript" src="Res/js/LfElevation/dist/Leaflet.Elevation-0.0.1.min.js"></script>
<script type="text/javascript" src="Res/js/LfElevation/lib/leaflet-gpx/gpx.js"></script>

<div id="map" style="width: 100%; height: 600px"></div>

<script type="text/javascript">
var map = new L.Map('map').setView([50.242656, 16.736217], 13);

var url = 'http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', attr ='Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>', service = new L.TileLayer(url, {subdomains:"1234",attribution: attr});

var el = L.control.elevation();
el.addTo(map);
var g=new L.GPX("$GpxFile", {
    async: true,
        marker_options: {
        startIconUrl: 'Res/js/LfElevation/lib/leaflet-gpx/pin-icon-start.png',
        endIconUrl: 'Res/js/LfElevation/lib/leaflet-gpx/pin-icon-end.png',
        shadowUrl: 'Res/js/LfElevation/lib/leaflet-gpx/pin-shadow.png'
        }
});
g.on('loaded', function(e) {map.fitBounds(e.target.getBounds());});
g.on("addline",function(e) {el.addData(e.line);});
g.addTo(map);
map.addLayer(service);
</script>

<br>

$Stat

[<img src="$RasterMap" width="" height="100"/>]($RasterMap "64pixels")


**[Raster Map]($RasterMap) (large file).**
