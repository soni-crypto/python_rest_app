
"use strict";

function initProgram (){
    var mapStyle = [
        {
            featureType: 'poi',
            elementType: 'labels',
            stylers: [{ visibility: 'off' }]  // Oculta los lugares de interés (marcadores predeterminados)
        },
        {
            featureType: 'transit.station',
            elementType: 'labels.icon',
            stylers: [{ visibility: 'off' }]  // Oculta las estaciones de carros
        },
        {
            featureType: 'road',
            elementType: 'labels',
            stylers: [{ visibility: 'off' }]  // Oculta las etiquetas de las carreteras
        }
    ];
    const CONFIGURATION = {
        "ctaTitle": "Checkout",
        "mapOptions": {"center":{"lat":-13.1602594,"lng":-74.2258714},"fullscreenControl":false,"mapTypeControl":false,"streetViewControl":false,"zoom":15,"zoomControl":false,"maxZoom":22,"mapId":"roadmap"},
        "mapsApiKey": "AIzaSyCZlR0aMbjBDDfwQB32r-wtDal2K0ebwlQ",
        "capabilities": {"addressAutocompleteControl":true,"mapDisplayControl":true,"ctaControl":true}
    };
    const componentForm = [
        'location',
        'postal_code',
        
    ];
    const coordinates_input = document.getElementById("company_location_coord");
    let value_center = CONFIGURATION.mapOptions.center;
    if (coordinates_input.value.length > 0){
        let value_c = coordinates_input.value;
        value_c = value_c.split(",");
        let lat_db = parseFloat(value_c[0]);
        let lng_db = parseFloat(value_c[1]);
        value_center = { lat: lat_db, lng: lng_db };
    }
    
    const getFormInputElement = (component) => document.getElementById(component+'-input');
    const map = new google.maps.Map(document.querySelector("#gmp-map"), {
        zoom: CONFIGURATION.mapOptions.zoom,
        center: value_center,
        mapTypeControl: false,
        fullscreenControl: CONFIGURATION.mapOptions.fullscreenControl,
        zoomControl: CONFIGURATION.mapOptions.zoomControl,  
        streetViewControl: CONFIGURATION.mapOptions.streetViewControl,
        mapTypeId: CONFIGURATION.mapOptions.mapId,
        styles: mapStyle,
    });
    if (document.getElementById("location_coord_restaurant")){
        if (document.getElementById("location_coord_restaurant").value.length > 0){
            let value_c = document.getElementById("location_coord_restaurant").value;
            value_c = value_c.split(",");
            let lat_db = parseFloat(value_c[0]);
            let lng_db = parseFloat(value_c[1]);
            value_center = { lat: lat_db, lng: lng_db };
            const marker = new google.maps.Marker({map: map, position: value_center, draggable: false, icon:{url : "/static/images/userapp/images_default/restaurant-3d-neeva.min.png",scaledSize: new google.maps.Size(50, 39),}});
        }
    }
    map.addListener('idle', function() {
        var newCenter = map.getCenter();
        coordinates_input.value = String(newCenter.lat())+","+String(newCenter.lng());
        let event = new Event("new_coordinate");
        coordinates_input.dispatchEvent(event); 
    });
    const autocompleteInput = getFormInputElement('location');
    const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
        fields: ["address_components", "geometry", "name"],
        types: ["address"],
        componentRestrictions: {
            country: "PE"
            },
    });
    autocomplete.addListener('place_changed', function () {
        marker.setVisible(false);
        const place = autocomplete.getPlace();
        if (!place.geometry) {
        
        window.alert('No details available for input: \'' + place.name + '\'');
        return;
        }
        renderAddress(place);
        fillInAddress(place);
    });

    function fillInAddress(place) {  // optional parameter
        const addressNameFormat = {
            'street_number': 'short_name',
            'route': 'long_name',
            'postal_code':'short_name',
        };
        const getAddressComp = function (type) {
        for (const component of place.address_components) {
            if (component.types[0] === type) {
            return component[addressNameFormat[type]];
            }
        }
        return '';
        };
        // getFormInputElement('location').value = getAddressComp('street_number') + ' '
        //         + getAddressComp('route');
        for (const component of componentForm) {
            // Location field is handled separately above as it has different logic.
            if (component !== 'location') {
                
                getFormInputElement(component).value = getAddressComp(component);
            }
        }
    }

    function renderAddress(place) {
        const latGoogle =place.geometry.location.lat();
        const lngGoogle =place.geometry.location.lng();
        coordinates_input.value = String(latGoogle)+","+String(lngGoogle);
        let event = new Event("new_coordinate")
        coordinates_input.dispatchEvent(event);

        map.setCenter(place.geometry.location);
        marker.setPosition(place.geometry.location);
        marker.setVisible(true);
        
    }
}
