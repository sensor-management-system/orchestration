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
    <BaseMap
      ref="map"
      v-model="mapState"
      height-storage-key="site"
      @click="addMarker"
      @ready="onReady"
    >
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
    </BaseMap>
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
import { LatLng, latLngBounds, LocationEvent } from 'leaflet'
import VGeosearch from '@/components/shared/Vue2LeafletGeosearch.vue'
import BaseMap, { MapState } from '@/components/shared/BaseMap.vue'

@Component({
  components: {
    BaseMap,
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

  private markers: LatLng[] = []
  private polygon: LatLng[] = []
  private polylineColor: string = 'green'

  private mapState: MapState = {
    bounds: latLngBounds([new LatLng(52, 12)])
  }

  mounted () {
    this.markers = this.value
    this.polygon = this.markers
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
    this.mapState.bounds = bounds
  }

  onReady () {
    if (this.value.length > 0) {
      this.fitPolyline()
    } else {
      (this.$refs.map as BaseMap).locate()
    }
  }

  @Watch('value', { immediate: true })
  onValueChange (newValue: LatLng[], _oldValue: LatLng[]) {
    this.markers = newValue
    this.$emit('updateCoords', this.polyline.latlngs)
  }
}
</script>
