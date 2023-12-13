<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <div v-if="value" style="height: 300px" class="mb-4">
      <l-map
        ref="siteMap"
        :zoom="zoomLevel"
        :center="currentPosition"
        style="z-index:0"
        :bounds="bounds"
        @click="addMarker"
        @ready="onReady"
        @locationfound="onLocationFound"
      >
        <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
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
          :options="
            geosearchOptions"
        />
      </l-map>
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

  mounted () {
    if (this.location !== null) {
      this.currentPosition = this.location
    }
    this.markers = this.value
    this.polygon = this.markers
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

  @Watch('value', { immediate: true })
  onValueChange (newValue: LatLng[], _oldValue: LatLng[]) {
    this.markers = newValue
    this.$emit('updateCoords', this.polyline.latlngs)
  }
}
</script>

<style scoped>
@import '~/assets/leaflet-geosearch@2.6.0.css';
</style>
