<template>
  <div id="map-wrap" style="height: 300px">
    <no-ssr>
      <l-map
        :zoom="10"
        :center="currentPosition"
        style="z-index:0"
        @click="setCoordinate"
        @ready="onReady"
        @locationfound="onLocationFound"
      >
        <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
        <l-marker v-if="location" :lat-lng="location" />
      </l-map>
    </no-ssr>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { LatLng, LeafletMouseEvent, LocationEvent, Map } from 'leaflet'

import { StationaryLocation } from '@/models/Location'

@Component
export default class LocationMap extends Vue {
  @Prop({ required: true, type: Object })
  readonly value!:StationaryLocation

  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean

  private currentPosition: LatLng = new LatLng(52, 12);

  created () {
    if (this.location !== null) {
      this.currentPosition = this.location
    }
  }

  setCoordinate (event: LeafletMouseEvent) {
    if (this.readonly) {
      return
    }

    const newValue = StationaryLocation.createFromObject({
      latitude: event.latlng.lat,
      longitude: event.latlng.lng,
      elevation: event.latlng.alt || null
    })
    this.$emit('input', newValue)
  }

  get location ():LatLng|null {
    if (!!this.value.latitude && !!this.value.longitude) {
      return new LatLng(this.value.latitude, this.value.longitude)
    }
    return null
  }

  onReady (mapObject:Map) {
    // Only locate when no coordinates were set
    if (!this.location) {
      mapObject.locate()
    }
  }

  onLocationFound (location: LocationEvent) {
    this.currentPosition = location.latlng
  }
}
</script>

<style scoped>
</style>
