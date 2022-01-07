<template>
    <div v-show="!loading" id='map' ref="mapRef" class="flex-grow-1">
      <div ref="start" class="route-marker">
        <div class="icon tt-icon -white -start"></div>
      </div>
      <div ref="finish" class="route-marker">
        <div class="icon tt-icon -white -finish"></div>
      </div>
    </div>
  <div v-if="loading" class="flex-grow-1 d-flex flex-column justify-content-center">
    <SwappingSquaresSpinner
        :animation-duration="1000"
        :size="150"
        color="#ff1d5e"
        class="align-self-center"
    />
  </div>
</template>

<script>
import { SwappingSquaresSpinner } from 'epic-spinners'
import { onMounted,  ref } from 'vue'
export default {
  name: 'MapPath',
  props: ['address'],
  components: {
    SwappingSquaresSpinner
  },
  setup(props) {
    const mapRef = ref(null)
    const start = ref(null)
    const finish = ref(null)
    const tt = window.tt;
    const messageBox = ref(null)
    const messageBoxContent = ref(null)
    const messageBoxClose = ref(null)
    const loading = ref(true)

    const getCoords = async () => {
      const pos = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });

      return `${pos.coords.longitude},${pos.coords.latitude}`
    }

    onMounted( async () => {
      const res = await tt.services.geocode({query: props.address, key: process.env.VUE_APP_TOTOM_APIKEY})
      const final = `${res.results[0].position.lng},${res.results[0].position.lat}`
      const start = await getCoords();
      let map = tt.map({
        key: process.env.VUE_APP_TOTOM_APIKEY,
        container: mapRef.value,
        dragPan: true,
      });
      map.addControl(new tt.FullscreenControl());
      map.addControl(new tt.NavigationControl());

      map.once('load', function () {
        tt.services.calculateRoute({
          key: process.env.VUE_APP_TOTOM_APIKEY,
          traffic: false,
          locations: `${start}:${final}`
        })
            .then(function (response) {
              let geojson = response.toGeoJson();
              map.addLayer({
                'id': 'route',
                'type': 'line',
                'source': {
                  'type': 'geojson',
                  'data': geojson
                },
                'paint': {
                  'line-color': '#4a90e2',
                  'line-width': 8
                }
              }, findFirstBuildingLayerId(map));
              addMarkers(geojson.features[0], map);
              let bounds = new tt.LngLatBounds();
              geojson.features[0].geometry.coordinates.forEach(function (point) {
                bounds.extend(tt.LngLat.convert(point));
              });
              map.fitBounds(bounds, {duration: 0, padding: 50});
            })
      })
      // Create plugin instance
      let geolocateControl = new tt.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: false
        }
      });

      map.addControl(geolocateControl);
      loading.value = false
    })

    function addMarkers(feature, map) {
      let startPoint, endPoint;
      if (feature.geometry.type === 'MultiLineString') {
        startPoint = feature.geometry.coordinates[0][0]; //get first point from first line
        endPoint = feature.geometry.coordinates.slice(-1)[0].slice(-1)[0]; //get last point from last line
      } else {
        startPoint = feature.geometry.coordinates[0];
        endPoint = feature.geometry.coordinates.slice(-1)[0];
      }
      new tt.Marker({ element: start.value }).setLngLat(startPoint).addTo(map);
      new tt.Marker({ element: finish.value }).setLngLat(endPoint).addTo(map);
    }
    function findFirstBuildingLayerId(map) {
      let layers = map.getStyle().layers;
      for (let index in layers) {
        if (layers[index].type === 'fill-extrusion') {
          return layers[index].id;
        }
      }
      throw new Error('Map style does not contain any layer with fill-extrusion type.');
    }

    return {
      mapRef, start, finish, messageBox, messageBoxContent, messageBoxClose, loading
    }
  }
}
</script>
<style>
.icon {
  background-size: cover;
  height: 30px;
  width: 30px;
}
.route-marker {
  align-items: center;
  background-color: #4a90e2;
  border: solid 3px #2faaff;
  border-radius: 50%;
  display: flex;
  height: 32px;
  justify-content: center;
  transition: width .1s, height .1s;
  width: 32px;
}

.tt-icon {
  background-position: 50%;
  background-repeat: no-repeat;
  display: inline-block;
}

.tt-icon.-finish {
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='17' viewBox='0 0 14 17'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath fill-rule='nonzero' stroke='%23E5E5E5' d='M-20.5-19.5h55v55h-55z'/%3E%3Cpath fill='%237A7E80' d='M5.811 2.194V0H8.02v2.28h1.765V0H14v16.406h-2.108V6.837H9.784V4.558H8.019v2.28H5.811v-2.28H7.92V2.28H5.933v2.193H3.946v2.194H2.108v9.74H0V0h3.946v2.194h1.865zm4.316 2.364h1.765V2.28h-1.765v2.278zM2.108 2.28v2.108h1.717V2.28H2.108z'/%3E%3C/g%3E%3C/svg%3E");
  height: 17px;
  width: 14px;
}

.tt-icon.-finish.-white {
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='17' viewBox='0 0 14 17'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath fill-rule='nonzero' stroke='white' d='M-20.5-19.5h55v55h-55z'/%3E%3Cpath fill='white' d='M5.811 2.194V0H8.02v2.28h1.765V0H14v16.406h-2.108V6.837H9.784V4.558H8.019v2.28H5.811v-2.28H7.92V2.28H5.933v2.193H3.946v2.194H2.108v9.74H0V0h3.946v2.194h1.865zm4.316 2.364h1.765V2.28h-1.765v2.278zM2.108 2.28v2.108h1.717V2.28H2.108z'/%3E%3C/g%3E%3C/svg%3E");
}

.tt-icon.-start {
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath fill-rule='nonzero' stroke='%23E5E5E5' d='M-19.5-19.5h55v55h-55z'/%3E%3Cpath fill='%237A7E80' d='M15.493.015a.4.4 0 0 1 .492.493L11.728 15.66a.4.4 0 0 1-.757.036l-2.914-7.55a.4.4 0 0 0-.23-.229L.257 5.015a.4.4 0 0 1 .035-.758l15.2-4.242z'/%3E%3C/g%3E%3C/svg%3E");
  height: 16px;
  width: 16px;
}

.tt-icon.-start.-white {
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath fill-rule='nonzero' stroke='white' d='M-19.5-19.5h55v55h-55z'/%3E%3Cpath fill='white' d='M15.493.015a.4.4 0 0 1 .492.493L11.728 15.66a.4.4 0 0 1-.757.036l-2.914-7.55a.4.4 0 0 0-.23-.229L.257 5.015a.4.4 0 0 1 .035-.758l15.2-4.242z'/%3E%3C/g%3E%3C/svg%3E");
}


</style>