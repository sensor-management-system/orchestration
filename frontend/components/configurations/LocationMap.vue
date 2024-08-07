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
  <BaseMap
    ref="map"
    v-model="mapState"
    height-storage-key="location"
    :localization-button="!readonly"
    @click="setCoordinatesByMapClick"
    @update="setMapState"
    @locationchange="setCoordinatesByLocation"
  >
    <l-marker v-if="location" :lat-lng="location" />
  </BaseMap>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import { LatLng, LeafletMouseEvent } from 'leaflet'

import { LControl } from 'vue2-leaflet'
import { StationaryLocation } from '@/models/Location'
import BaseMap, { MapState } from '@/components/shared/BaseMap.vue'

@Component({
  components: { BaseMap, LControl }
})
export default class LocationMap extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: StationaryLocation

  @Prop({
    default: false,
    type: Boolean
  }) readonly readonly!: boolean

  private mapState: MapState = {
    center: this.location ?? new LatLng(52, 12)
  }

  get location (): LatLng | null {
    if (!!this.value.latitude && !!this.value.longitude) {
      return new LatLng(this.value.latitude, this.value.longitude)
    }
    return null
  }

  @Watch('location', { deep: true })
  setMapCenter (latlng: LatLng) {
    this.mapState.center = latlng
  }

  setCoordinates (latlng: LatLng) {
    const newValue = StationaryLocation.createFromObject({
      latitude: latlng.lat,
      longitude: latlng.lng,
      elevation: latlng.alt || null
    })

    this.$emit('input', newValue)
  }

  setCoordinatesByLocation (latlng: LatLng) {
    this.setCoordinates(latlng)
  }

  setCoordinatesByMapClick (event: LeafletMouseEvent) {
    if (this.readonly) {
      return
    }
    const latlng = event.latlng
    this.setCoordinates(latlng)
  }

  setMapState (mapState: MapState) {
    this.mapState = mapState
  }
}
</script>
