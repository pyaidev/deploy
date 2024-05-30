function mapMultyPointMaker() {
    // Make map window from map field with markers with special coordinates

}

function infoSpotMaker(item, infoSpotData) {
    // Prepare infoSpot data for panorama
    const currentInfoSpot = infoSpotData
    const title_text = currentInfoSpot['title'];
    const description = currentInfoSpot['description'];
    const figures_3d_id = currentInfoSpot['figure_3d_id'];
    const figures_thin_section_id = currentInfoSpot['figure_thin_section_id'];
    const preview = currentInfoSpot['preview'];
    const youtube = currentInfoSpot['youtube_for_iframe'];
    const figures_thin_section_preview = currentInfoSpot['figure_thin_section_preview'];
    const figures_3d_link_for_iframe = currentInfoSpot['figure_3d_link_for_iframe'];

    let infoSpot = new PANOLENS.Infospot(200, customInfoSpotIcon);
    infoSpot.position.set(item['coord_X'], item['coord_Y'], item['coord_Z']);

    if (description || figures_3d_id || figures_thin_section_id || preview || youtube) {
        // Getting a reference to DOM elements
        let container = document.getElementById('desc-container').cloneNode(true);
        let figures_3d = container.querySelector('#desc-container .wrapper');
        let figures_thin_section = container.querySelector('#desc-container .md_image-container_for_window');
        let image = container.querySelector('#desc-container .preview_image');
        let iframe = container.querySelector('#desc-container .youtube_iframe');
        let title = container.querySelector('#desc-container .title');
        let text = container.querySelector('#desc-container .text');
        let thin_section_link = container.querySelector('#figures_thin_section_window .md_image-container_href');
        let thin_section_img = container.querySelector('#figures_thin_section_window .md_image');
        let figures_3d_iframe = container.querySelector('#desc-container .figure_3d_iframe_class');

        // Adding text to tags with the title and text classes
        if (figures_3d_id) {
            figures_3d_iframe.src = figures_3d_link_for_iframe + '+spin+bg-2b3035ff+dl,share,link,border-hidden';
        } else {
            figures_3d.style.display = 'none';
        }
        // Adding figures_thin_section
        if (figures_thin_section_id) {
            thin_section_link.href = `/applications/virtual_microscope/${figures_thin_section_id}/`;
            thin_section_img.src = '/media/' + figures_thin_section_preview;
        } else {
            figures_thin_section.style.display = 'none';
        }
        // Changing the src of the img tag
        if (preview) {
            image.src = '/media/' + preview;
        } else {
            image.style.display = 'none';
        }
        // Changing the src of the iframe tag
        if (youtube) {
            iframe.src = youtube;
            iframe.title = title;
        } else {
            iframe.style.display = 'none';
        }
        // Adding text to tags with the title and text classes
        title.textContent = title_text;
        if (description) {
            text.textContent = description;
        } else {
            text.style.display = 'none';
        }
        infoSpot.addHoverElement(container, 270);
    } else {
        infoSpot.addHoverText(title_text);
    }
    return infoSpot;
}

function panoramaMaker(imagePath, panoramaId, infoSpotCoordList, infoSpotDict, linkSpotCoordList = null) {
    // Prepare panorama for Viewer
    let panorama = new PANOLENS.ImagePanorama(imagePath);
    let linkSpotsIdDict = {};
    if (infoSpotCoordList) {
        for (let item of infoSpotCoordList) {
            if (item['panorama_id'] == panoramaId) {
                let infoSpotData = infoSpotDict[item['info_spot_id']];
                let infoSpot = infoSpotMaker(item, infoSpotData);
                panorama.add(infoSpot);
            }
        }
    }
    if (linkSpotCoordList) {
        for (let linkSpot of linkSpotCoordList) {
            if (linkSpot['panorama_from_id'] == panoramaId) {
                linkSpotsIdDict[linkSpot['panorama_to_id']] = {
                    'id': linkSpot['panorama_to_id'],
                    'coord_X': linkSpot['coord_X'],
                    'coord_Y': linkSpot['coord_Y'],
                    'coord_Z': linkSpot['coord_Z'],
                }

            }
        }
    }
    return {
        panorama: panorama,
        linkSpotsIdDict: linkSpotsIdDict,
        linkSpotsIdList: Object.values(linkSpotsIdDict)
    };
}

const customAirPanoIcon = 'data:image/png;base64,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';
const customGroundPanoIcon = 'data:image/png;base64,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';
const customOtherPanoIcon = undefined;
const customInfoSpotIcon = 'data:image/png;base64,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';
let viewerPanoDict = {};
let viewersList = [];

if (panoramaDict) {
    // Situation for MaterialDetailView
    const panoramaWindows = document.querySelectorAll('.pano-image');
    panoramaWindows.forEach((panoramaWindow) => {

        const currentFigureId = panoramaWindow.id.split('_')[1];
        let mainPanoramaId;


        for (let item of material_photos_list) {
            if (item.pk == currentFigureId) {
                mainPanoramaId = item.fields.pano_view;
            }
        }

        const mainPanoramaPath = panoramaDict[mainPanoramaId].view
        for (let item of panoramaList) {
            let panoramaId = item['pk'];
            let panoramaPath = item['view'];
            viewerPanoDict[panoramaId] = panoramaMaker(panoramaPath, panoramaId, infoSpotCoordList, infoSpotDict, linkSpotCoordList)
        }

        let viewerPanoList2 = Object.values(viewerPanoDict);
        for (let panoFrom of viewerPanoList2) {
            if (panoFrom.linkSpotsIdList) {
                for (let panorama_to of panoFrom.linkSpotsIdList) {
                    let logo_path;
                    if (panoramaDict[panorama_to.id].pano_type === 'air') {
                        logo_path = customAirPanoIcon;
                    } else if (panoramaDict[panorama_to.id].pano_type === 'ground') {
                        logo_path = customGroundPanoIcon;
                    } else {
                        logo_path = customOtherPanoIcon;
                    }
                    panoFrom.panorama.link(viewerPanoDict[panorama_to.id].panorama, new THREE.Vector3(panorama_to.coord_X, panorama_to.coord_Y, panorama_to.coord_Z), 350, logo_path);
                }
            }
        }

        let viewer = new PANOLENS.Viewer({
            container: panoramaWindow, // A Element container
            autoRotate: true,
            autoRotateSpeed: 0.2,
            controlBar: true, // Vsibility of bottom control bar
            controlButtons: ['fullscreen', 'video'], // Buttons array in the control bar. Default to ['fullscreen', 'setting', 'video']
            autoHideControlBar: false, // Auto hide control bar
            autoHideInfospot: true, // Auto hide infospots
            horizontalView: false, // Allow only horizontal camera control
            cameraFov: 70, // Camera field of view in degree
            reverseDragging: false, // Reverse orbit control direction
            enableReticle: false, // Enable reticle for mouseless interaction
            dwellTime: 1500, // Dwell time for reticle selection in millisecond
            autoReticleSelect: true, // Auto select a clickable target after dwellTime
            viewIndicator: true, // Adds an angle view indicator in upper left corner
            indicatorSize: 60, // Size of View Indicator
            output: 'console' // Whether and where to output infospot position. Could be 'console' or 'overlay'
        });

        let finalPanoramas = [];
        let viewerPanoList = Object.values(viewerPanoDict);
        for (let obj of viewerPanoList) {
            const panorama = obj.panorama; // Получаем значение по ключу panorama
            finalPanoramas.push(panorama); // Собираем все панорамы в массив
        }
        // We rebuild the list so that the initial panorama is at the end and thus is ordered by default
        let finalPanoramasSwapped = [];
        let temp;
        for (let item of finalPanoramas) {
            if (item.src === mainPanoramaPath) {
                temp = item;
            } else {
                finalPanoramasSwapped.push(item);
            }
        }
        finalPanoramasSwapped.unshift(temp)
        viewer.add(...finalPanoramasSwapped);
        viewersList.push(viewer);
    });


} else {
    // Situation for 360viewDetailView
    let viewerPanoDict = {};
    viewerPanoDict[imgId] = panoramaMaker(imgPath, imgId, infoSpotCoordList, infoSpotDict);
    const mapForm = document.getElementById('map_iframe')
    if (mapForm) {
        mapMaker(infoPointLatitude, infoPointLongitude)
    }

    const panoramaWindow = document.querySelector('.pano-image');
    const viewer = new PANOLENS.Viewer({
        container: panoramaWindow, // A Element container
        autoRotate: true,
        autoRotateSpeed: 0.2,
        controlBar: true, // Vsibility of bottom control bar
        controlButtons: ['fullscreen', 'video'], // Buttons array in the control bar. Default to ['fullscreen', 'setting', 'video']
        autoHideControlBar: false, // Auto hide control bar
        autoHideInfospot: true, // Auto hide infospots
        horizontalView: false, // Allow only horizontal camera control
        cameraFov: 70, // Camera field of view in degree
        reverseDragging: false, // Reverse orbit control direction
        enableReticle: false, // Enable reticle for mouseless interaction
        dwellTime: 1500, // Dwell time for reticle selection in millisecond
        autoReticleSelect: true, // Auto select a clickable target after dwellTime
        viewIndicator: true, // Adds an angle view indicator in upper left corner
        indicatorSize: 60, // Size of View Indicator
        output: 'console' // Whether and where to output infospot position. Could be 'console' or 'overlay'
    });

    let finalPanoramas = [];
    let viewerPanoList = Object.values(viewerPanoDict);
    for (let obj of viewerPanoList) {
        const panorama = obj.panorama; // Получаем значение по ключу panorama
        finalPanoramas.push(panorama); // Собираем все панорамы в массив
    }

    viewer.add(...finalPanoramas);
    viewersList.push(viewer);

}

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 3,
        center: {lat: -28.024, lng: 140.887},
        mapTypeId: 'satellite',
    });
    const infoWindow = new google.maps.InfoWindow({
        content: "",
        disableAutoPan: true,
    });
    // Add some markers to the map.
    const markers = my_markers.map((my_marker, i) => {
        const position = my_marker.coords;
        const title = my_marker.title;
        const type = my_marker.type;
        let icon_path;
        let icon_scale;
        let icon_anchor;
        switch (type) {
            case 'air':
                icon_path = 'M256.115,255.272c-7.784,0.01-14.438,2.782-19.96,8.321      c-5.539,5.521-8.315,12.175-8.322,19.959c0.007,7.802,2.783,14.475,8.322,20.017c5.522,5.519,12.176,8.273,19.96,8.262      c7.806,0.012,14.478-2.743,20.021-8.262c5.519-5.542,8.274-12.215,8.263-20.017c0.012-7.784-2.744-14.438-8.263-19.959      C270.593,258.055,263.921,255.282,256.115,255.272z M278.986,189.171h1.339c10.268,0.242,19.211,1.89,26.828,4.946      c7.759,3.14,14.14,7.756,19.146,13.848h90.086v-26.067c-11.027-0.209-21.211-0.714-30.552-1.513      c-6.636-0.569-12.842-1.287-18.623-2.154c-16.513-2.431-24.775-5.359-24.792-8.786c0.017-3.409,8.279-6.338,24.792-8.786      c13.956-2.02,30.349-3.184,49.175-3.491v-1.222c-0.018-1.436,0.196-2.773,0.64-4.016c0.565-1.758,1.536-3.349,2.909-4.771      c2.41-2.394,5.319-3.578,8.729-3.55c3.451-0.028,6.401,1.156,8.848,3.55c2.323,2.355,3.544,5.167,3.664,8.437      c0,0.116,0,0.232,0,0.351v1.222c6.393,0.179,12.503,0.47,18.331,0.873c9.955,0.558,19.053,1.431,27.295,2.618      c0.474,0.089,0.939,0.186,1.396,0.291c15.626,2.372,23.462,5.203,23.512,8.495c-0.05,3.33-7.886,6.181-23.512,8.554      c-0.457,0.085-0.923,0.162-1.396,0.232c-13.051,1.961-28.259,3.144-45.626,3.55v26.185H452c3.431,0.012,6.36,1.233,8.788,3.666      c2.433,2.408,3.655,5.318,3.665,8.729c-0.007,2.427-0.628,4.599-1.862,6.517c-2.114,2.812-5.181,4.789-9.195,5.935      c-33.984,8.146-67.97,16.293-101.957,24.439l38.934,81.582c0.226,0.402,0.439,0.812,0.639,1.221      c9.332,26.235,2.833,47.242-19.495,63.019c-2.808,2.014-5.89,2.753-9.252,2.212c-3.325-0.616-5.965-2.341-7.915-5.181      c-2.017-2.798-2.756-5.882-2.212-9.251c0.584-3.343,2.273-6,5.064-7.971c12.017-8.617,15.49-20.062,10.416-34.331      l-40.911-85.362l-10.65,2.618v42.534c0.005,3.035-0.753,5.867-2.269,8.497v0.057c-1.534,2.613-3.61,4.669-6.227,6.169      l-42.948,24.729v0.06c-2.655,1.509-5.487,2.267-8.497,2.269c-3.023-0.025-5.856-0.8-8.495-2.328l-42.89-24.789l-0.118-0.057      c-2.585-1.536-4.621-3.611-6.11-6.226c-1.519-2.63-2.273-5.444-2.269-8.438v-42.478l-10.707-2.618l-40.912,85.362      c-5.073,14.27-1.603,25.714,10.416,34.331c2.792,1.971,4.48,4.628,5.063,7.971c0.546,3.369-0.193,6.453-2.209,9.251      c-1.951,2.84-4.59,4.564-7.916,5.181c-3.362,0.541-6.446-0.198-9.252-2.212c-22.328-15.776-28.827-36.783-19.495-63.019      c0.2-0.409,0.414-0.818,0.639-1.221l38.934-81.582c-33.987-8.146-67.972-16.293-101.959-24.439      c-4.015-1.146-7.079-3.123-9.193-5.935c-1.234-1.918-1.855-4.09-1.864-6.517c0.011-3.41,1.232-6.32,3.667-8.729      c2.428-2.433,5.358-3.654,8.789-3.666h10.823V181.78c-17.368-0.406-32.576-1.589-45.624-3.55      c-0.473-0.07-0.939-0.147-1.396-0.232c-15.626-2.373-23.462-5.224-23.512-8.554c0.05-3.292,7.886-6.123,23.512-8.495      c0.457-0.105,0.923-0.202,1.396-0.291c8.243-1.188,17.34-2.061,27.292-2.618c5.831-0.403,11.941-0.694,18.332-0.873v-1.222      c0-0.118,0-0.234,0-0.351c0.123-3.27,1.344-6.081,3.667-8.437c2.446-2.394,5.394-3.578,8.845-3.55      c3.413-0.028,6.322,1.156,8.729,3.55c1.375,1.423,2.346,3.014,2.91,4.771c0.446,1.242,0.659,2.58,0.641,4.016v1.222      c18.827,0.308,35.22,1.472,49.175,3.491c16.513,2.448,24.776,5.377,24.792,8.786c-0.016,3.427-8.279,6.355-24.792,8.786      c-5.781,0.867-11.989,1.585-18.622,2.154c-9.344,0.799-19.527,1.304-30.553,1.513v26.067h90.086      c5.004-6.092,11.387-10.708,19.146-13.848c7.618-3.057,16.561-4.704,26.829-4.946h1.339c1.173-0.039,2.373-0.039,3.607,0h38.524      C276.61,189.132,277.813,189.132,278.986,189.171z M256.058,269.413c3.901,0.014,7.238,1.411,10.01,4.188      c2.76,2.751,4.137,6.069,4.133,9.951c0.004,3.901-1.373,7.237-4.133,10.009c-2.771,2.759-6.108,4.137-10.01,4.13      c-3.883,0.007-7.199-1.371-9.952-4.13c-2.78-2.771-4.176-6.107-4.189-10.009c0.014-3.882,1.409-7.2,4.189-9.951      C248.858,270.824,252.175,269.427,256.058,269.413z';
                icon_scale = 0.08;
                icon_anchor = new google.maps.Point(256, 256);
                break;
            case 'ground':
                icon_path = 'M73.428,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211s10.211-4.581,10.211-10.211\n' +
                    '\t\tC83.639,268.592,79.058,264.011,73.428,264.011z M286.789,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211\n' +
                    '\t\tc5.63,0,10.211-4.581,10.211-10.211C297,268.592,292.419,264.011,286.789,264.011z M179.84,264.011c-5.63,0-10.211,4.581-10.211,10.211c0,5.63,4.581,10.211,10.211,10.211c5.63,0,10.211-4.581,10.211-10.211\n' +
                    '\t\tC190.051,268.592,185.47,264.011,179.84,264.011z M94.103,111.86c0.356-2.829-0.427-5.682-2.177-7.933l-4.649-5.984l42.611-28.407h103.158\n' +
                    '\t\tc5.936,0,10.749-4.813,10.749-10.749V23.315c0-5.936-4.813-10.749-10.749-10.749H126.634c-5.936,0-10.749,4.813-10.749,10.749\n' +
                    '\t\tv29.718L74.054,80.921l-3.89-5.008c-3.64-4.688-10.394-5.536-15.081-1.895L4.156,113.574c-2.252,1.749-3.717,4.32-4.072,7.149\n' +
                    '\t\tc-0.356,2.829,0.427,5.682,2.177,7.933l21.763,28.013c2.118,2.728,5.289,4.155,8.495,4.155c2.304,0,4.626-0.737,6.586-2.26\n' +
                    '\t\tl50.927-39.555C92.283,117.26,93.749,114.688,94.103,111.86z M204.951,117.829h-50.222L75.972,249.091c7.668,0.77,14.336,4.985,18.428,11.069l17.037-28.395h57.654v19.605\n' +
                    '\t\tc3.264-1.541,6.906-2.407,10.749-2.407s7.485,0.866,10.749,2.407v-19.605h57.654l17.297,28.828\n' +
                    '\t\tc3.977-6.18,10.571-10.518,18.206-11.44L204.951,117.829z M169.091,210.268h-44.755l44.755-74.592V210.268z M190.588,210.268\n' +
                    '\t\tv-74.592l44.755,74.592H190.588z M226.059,94.257v-6.898c0-2.75-2.25-5-5-5H138.62c-2.75,0-5,2.25-5,5v6.898c0,5.936,4.813,10.749,10.749,10.749h70.941\n' +
                    '\t\tC221.246,105.005,226.059,100.192,226.059,94.257z';
                icon_scale = 0.1;
                icon_anchor = new google.maps.Point(150, 100);
                break;
            case 'info_spot':
                icon_path = 'm48,9c-21.54,0-39,17.46-39,39s17.46,39 39,39 39-17.46 39-39-17.46-39-39-39zm6.117,53.349c-2.943,4.419-5.937,7.824-10.974,7.824-3.438-.561-4.851-3.024-4.107-5.535l6.48-21.462c.159-.525-.105-1.086-.585-1.257-.477-.168-1.413,.453-2.223,1.341l-3.918,4.713c-.105-.792-.012-2.1-.012-2.628 2.943-4.419 7.779-7.905 11.058-7.905 3.117,.318 4.593,2.811 4.05,5.55l-6.525,21.567c-.087,.486 .171,.981 .612,1.137 .48,.168 1.488-.453 2.301-1.341l3.915-4.71c.105,.792-.072,2.178-.072,2.706zm-.873-28.032c-2.478,0-4.488-1.806-4.488-4.464s2.01-4.461 4.488-4.461 4.488,1.806 4.488,4.461c0,2.661-2.01,4.464-4.488,4.464z';
                icon_scale = 0.3;
                icon_anchor = new google.maps.Point(48, 48);
                break;
            // other
            default:
                break;
        }

        const svgMarker = {
            path: icon_path,
            fillColor: "rgb(96,7,7)",
            fillOpacity: 0.85,
            strokeWeight: 0,
            rotation: 0,
            scale: icon_scale,
            anchor: icon_anchor,
        };

        const marker = new google.maps.Marker({
            position: position,
            title: title,
            icon: svgMarker,
        });
        // markers can only be keyboard focusable when they have click listeners
        // open info window when marker is clicked
        marker.addListener("mouseover", () => {
            const contentString = `<div style="color: black;">${title}</div>`;
            infoWindow.setContent(contentString);
            infoWindow.open(map, marker);
        });
        marker.addListener("mouseout", () => {
            infoWindow.close();
        });
        if (my_marker.panoramaPk) {
            marker.addListener("click", function () {
                // Получить идентификатор панорамы, связанной с этим маркером
                const panoramaId = my_marker.panoramaPk;
                // Сменить панораму во viewer
                viewersList[0].setPanorama(viewerPanoDict[panoramaId].panorama);
            });
        }
        return marker;
    });

    // Add a marker clusterer to manage the markers.
    //new MarkerClusterer({markers, map});
    const markerCluster = new markerClusterer.MarkerClusterer({map, markers});

    // Create a new instance of google.maps.LatLngBounds() to represent a rectangular geographical area.
    let bounds = new google.maps.LatLngBounds();

    // Iterate over each position in the locations array.
    locations.forEach(position => {
        // Extend the bounds to include the current position.
        bounds.extend(position);
    });

    // Adjust the map viewport to fit the bounds, ensuring that all included positions are visible.
    map.fitBounds(bounds);
}

let my_markers = [];
let locations = [];

if (panoramaList.length === 0) {
    panoramaList.push({
        'latitude': Number(infoPointLatitude),
        'longitude': Number(infoPointLongitude),
        'title': infoPointTitle,
        'pano_type': infoPointPanoType,
        'pk': imgId,
    });
}

for (let item of panoramaList) {
    locations.push({
        lat: item.latitude,
        lng: item.longitude
    });
    my_markers.push({
        title: item.title,
        type: item.pano_type,
        panoramaPk: item.pk,
        infoSpotPk: null,
        coords: {
            lat: item.latitude,
            lng: item.longitude
        }
    });
}
if (Object.keys(infoSpotDict).length > 0) {
    for (let item of Object.values(infoSpotDict)) {
        locations.push({
            lat: item.latitude,
            lng: item.longitude
        });
        my_markers.push({
            title: item.title,
            type: 'info_spot',
            panorama_pk: null,
            infoSpotPk: item.id,
            coords: {
                lat: item.latitude,
                lng: item.longitude
            }
        })
    }

}


window.initMap = initMap;