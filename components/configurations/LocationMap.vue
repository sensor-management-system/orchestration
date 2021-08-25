<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
