<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div id="map-wrap" style="height: 300px">
    <no-ssr>
      <l-map
        ref="map"
        :zoom="10"
        :center="currentMapCenter"
        style="z-index:0"
        @click="setCoordinatesByMapClick"
        @ready="onReady"
        @locationfound="onLocationFound"
      >
        <l-tile-layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
        <l-control-scale position="bottomleft" :imperial="true" :metric="true" :max-width="150" />
        <l-marker v-if="location" :lat-lng="location" />
        <v-btn
          v-if="!readonly"
          id="set-current-location-button"
          fab
          small
          color="white"
          :disabled="isLocating"
          @click.stop="setCoordinatesByCurrentLocation"
        >
          <v-icon v-if="!isLocating">
            mdi-map-marker-account
          </v-icon>
          <v-progress-circular v-else indeterminate />
        </v-btn>
      </l-map>
    </no-ssr>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import { LatLng, LeafletMouseEvent, LocationEvent, Map } from 'leaflet'

import { StationaryLocation } from '@/models/Location'

@Component
export default class LocationMap extends Vue {
  @Prop({ required: true, type: Object })
  readonly value!: StationaryLocation

  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean

  private currentPosition: LatLng|null = null
  private isLocating: Boolean = false
  private defaultMapCenter: LatLng = new LatLng(52, 12)
  private currentMapCenter: LatLng = this.location ?? this.defaultMapCenter
  private currentMapCenterInitializedByLocation = false

  created () {
    if (this.location !== null) {
      this.currentPosition = this.location
      this.currentMapCenterInitializedByLocation = true
    }
  }

  setCoordinatesByMapClick (event: LeafletMouseEvent) {
    if (this.readonly) {
      return
    }

    this.setCoordinates(event.latlng)
  }

  setCoordinatesByCurrentLocation () {
    if (!this.currentPosition) {
      if (!this.mapObject) { return }
      this.mapObject.locate()
      this.isLocating = true
      return
    }

    this.setCoordinates(this.currentPosition)
  }

  setCoordinates (latlng: LatLng) {
    const newValue = StationaryLocation.createFromObject({
      latitude: latlng.lat,
      longitude: latlng.lng,
      elevation: latlng.alt || null
    })
    this.$emit('input', newValue)

    this.currentMapCenter = latlng
  }

  get location (): LatLng|null {
    if (!!this.value.latitude && !!this.value.longitude) {
      return new LatLng(this.value.latitude, this.value.longitude)
    }
    return null
  }

  get mapObject (): Map|null {
    const mapRef: any|null = this.$refs.map
    const mapObject: Map|null = mapRef?.mapObject ?? null
    return mapObject
  }

  locatePosition () {
    if (!this.mapObject) { return }
    this.mapObject.locate()
  }

  onReady (mapObject: Map) {
    mapObject.on('locationerror', this.onLocationError)
    mapObject.on('locationfound', this.onLocationFound)
  }

  onLocationFound (location: LocationEvent) {
    this.isLocating = false

    if (this.currentPosition === null) {
      this.currentPosition = location.latlng
      this.setCoordinatesByCurrentLocation()
    }

    // Only recenter when no marker is set
    if (this.location === null) {
      this.currentMapCenter = location.latlng
    }
  }

  onLocationError () {
    this.isLocating = false
    this.$store.commit('snackbar/setError', 'Location could not be determined.')
  }

  @Watch('location')
  onLocationChange (location: LatLng|null) {
    // It can happen that the location is loaded after the creation of the component
    // was done.
    // In this case the location was not considered for the startup
    // and the code for the geoapi was used with the onLocationFound event.
    // However, if we still have a change from the value property (& the
    // location getter) then we still want to focus on this given location.
    //
    // But we don't want to focus on every new change of the location, so that
    // is why we check if the initialization was already done.
    //
    // However, if we use the component just to look at the location (readonly mode),
    // then an updated location means that we should show another static location.
    // In this case we want to update the current position by the given location.
    if (location !== null && (!this.currentMapCenterInitializedByLocation || this.readonly)) {
      this.currentMapCenter = location
      this.currentMapCenterInitializedByLocation = true
    }
  }
}
</script>

<style scoped>
#set-current-location-button {
  z-index: 500;
  position: absolute;
  right: 0;
  bottom: 1.5em;
  margin: 1em;
}
</style>
