<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <div
      id="mapContainer"
      :style="{ height: mapHeight + 'px'}"
      :class="{mapHover: mapHovered, draggerHover: draggerHovered}"
    >
      <l-map
        id="site-map"
        ref="siteMap"
        :zoom="zoomLevel"
        :center="currentPosition"
        :bounds="bounds"
        @click="addMarker"
        @ready="onReady"
        @locationfound="onLocationFound"
        @mouseenter="onMapHoverBegin"
        @mouseleave="onMapHoverEnd"
      >
        <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
        <l-control-scale position="bottomleft" :imperial="true" :metric="true" :max-width="150" />
        <template v-if="!readonly">
          <l-marker
            v-for="(marker, index) in markers"
            :key="index"
            :draggable="!readonly"
            :lat-lng="marker"
            @update:latLng="updateMarker($event, index)"
            @click="removeMarker(index)"
          />
        </template>
        <l-polygon
          ref="polygon"
          :lat-lngs="polygon"
          :color="polylineColor"
          :fill="true"
        />
        <l-polygon
          :lat-lngs="outer"
          color="black"
          dash-array="10"
          :fill="false"
          :stroke="true"
        />
        <v-geosearch
          :options="geosearchOptions"
        />
      </l-map>
      <div
        id="rezise-dragger"
        @mousedown="initResize"
        @mouseup="stopResize"
        @mouseenter="onDraggerHoverBegin"
        @mouseleave="onDraggerHoverEnd"
      />
    </div>
    <h4>Coordinates (WGS84)</h4>
    <div v-if="markers.length != 0 && markers.length < 3" class="text-subtitle-1 error--text">
      Please draw at least 3 markers.
    </div>
    <v-row v-for="(position, index) in markers" :key="index" no-gutters class="mt-4">
      <v-col
        cols="12"
        sm="6"
        md="4"
      >
        <v-text-field
          dense
          label="Latitude"
          :readonly="readonly"
          :value="position.lat"
          type="number"
          step="0.0001"
          @change="updateLatitude($event, index)"
        />
      </v-col>
      <v-col
        cols="12"
        sm="6"
        md="4"
      >
        <v-text-field
          dense
          label="Longitude"
          :readonly="readonly"
          :value="position.lng"
          type="number"
          step="0.0001"
          @change="updateLongitude($event, index)"
        >
          <template v-if="!readonly" #append-outer>
            <v-icon @click="removeMarker(index)">
              mdi-delete
            </v-icon>
          </template>
        </v-text-field>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import { LMap, LMarker, LTileLayer, LPolygon, LControl } from 'vue2-leaflet'
import { LatLng, LatLngBounds, latLngBounds, LocationEvent } from 'leaflet'
import { OpenStreetMapProvider } from 'leaflet-geosearch'
import VGeosearch from '@/components/shared/Vue2LeafletGeosearch.vue'

@Component({
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolygon,
    LControl,
    VGeosearch
  }
})
export default class SiteMap extends Vue {
  @Prop({
    default: () => [],
    type: Array
  }) readonly value!: LatLng[]

  @Prop({
    default: () => [],
    type: Array
  }) readonly outer!: LatLng[]

  @Prop({
    default: false,
    type: Boolean
  }) readonly readonly!: boolean

  private currentPosition: LatLng = new LatLng(52, 12)
  private zoomLevel = 10
  private markers: LatLng[] = []
  private polygon: LatLng[] = []
  private polylineColor: string = 'green'
  private bounds: LatLngBounds = latLngBounds([this.currentPosition])
  private provider = new OpenStreetMapProvider()

  private geosearchOptions = {
    ref: 'searchControl',
    provider: this.provider,
    style: 'button',
    autoComplete: true,
    showMarker: false
  }

  private minHeight: number = 200
  private maxHeight: number = 800
  private mapHeight: number = 300
  private isResizing: Boolean = false

  private mapHovered: Boolean = false
  private draggerHovered: Boolean = false

  private localStorageMapHeightKey = 'site-map-height'

  created () {
    // This needs to be in the created hook as the map didn't resize correctly when this was in mounted()
    const storedMapHeight = localStorage.getItem(this.localStorageMapHeightKey)
    if (storedMapHeight) {
      this.mapHeight = parseInt(storedMapHeight)
    }
  }

  mounted () {
    if (this.location !== null) {
      this.currentPosition = this.location
    }
    this.markers = this.value
    this.polygon = this.markers

    window.addEventListener('mousemove', this.doMapResize)
    window.addEventListener('mouseup', this.stopResize)
  }

  destroyed () {
    window.removeEventListener('mousemove', this.doMapResize)
    window.removeEventListener('mouseup', this.stopResize)
  }

  get location (): LatLng | null {
    if (this.value.length > 0) {
      return new LatLng(52, 10)
    }
    return null
  }

  removeMarker (index: number) {
    if (this.readonly) {
      return
    }
    this.markers.splice(index, 1)
    this.polygon = this.markers
  }

  updateMarker (value: LatLng, index: number) {
    this.markers[index] = value
    const copyArray = this.markers.slice()
    this.polygon = copyArray
  }

  addMarker (event: LocationEvent) {
    if (this.readonly) {
      return
    }
    this.markers.push(event.latlng)
    this.polygon = this.markers
  }

  get polyline () {
    const latlngs = this.markers
    const color = this.polylineColor
    return {
      latlngs,
      color
    }
  }

  updateLatitude (value: number, index: number) {
    const latLng = new LatLng(value, this.markers[index].lng)
    this.updateMarker(
      latLng,
      index
    )
  }

  updateLongitude (value: number, index: number) {
    const latLng = new LatLng(this.markers[index].lat, value)
    this.updateMarker(
      latLng,
      index
    )
  }

  fitPolyline () {
    const bounds = latLngBounds(this.markers)
    this.bounds = bounds
  }

  onReady (mapObject: any) {
    if (this.value.length > 0) {
      this.fitPolyline()
    } else {
      mapObject.locate()
    }
  }

  onLocationFound (location: LocationEvent) {
    this.currentPosition = location.latlng
  }

  initResize () {
    this.isResizing = true
    document.body.style.userSelect = 'none'
  }

  async doMapResize (event: MouseEvent) {
    if (!this.isResizing || !this.$refs.siteMap) { return }

    const mapElement = this.$refs.siteMap as Vue & {
          mapObject: {
            invalidateSize: () => void;
          },
          $el: HTMLElement
        }
    const newHeight = event.clientY - mapElement.$el.getBoundingClientRect().top

    if (newHeight >= this.minHeight && newHeight <= this.maxHeight) {
      this.mapHeight = newHeight
      await mapElement.mapObject.invalidateSize()
    }
  }

  stopResize () {
    this.isResizing = false
    document.body.style.userSelect = 'auto'
    localStorage.setItem(this.localStorageMapHeightKey, String(this.mapHeight))
  }

  onMapHoverBegin () {
    this.mapHovered = true
  }

  onMapHoverEnd () {
    this.mapHovered = false
  }

  onDraggerHoverBegin () {
    this.draggerHovered = true
  }

  onDraggerHoverEnd () {
    this.draggerHovered = false
  }

  @Watch('value', { immediate: true })
  onValueChange (newValue: LatLng[], _oldValue: LatLng[]) {
    this.markers = newValue
    this.$emit('updateCoords', this.polyline.latlngs)
  }
}
</script>

<style scoped>
@import '~/assets/leaflet-geosearch@2.6.0.css';

#rezise-dragger {
  height: 20px;
  cursor: ns-resize;
  width: 100%;
  z-index: 1000;
  position: relative;
  bottom: 10px;
}
#mapContainer {
  border-bottom: 2px solid transparent;
  transition: border .3s;
  padding-bottom: 4px;
}

#site-map {
  z-index: 0;
}

#mapContainer.mapHover {
  border-bottom: 2px solid #bbb;
  transition: border .3s;
}

#mapContainer.draggerHover {
  border-bottom: 2px solid black;
  transition: border .3s;
}

</style>
