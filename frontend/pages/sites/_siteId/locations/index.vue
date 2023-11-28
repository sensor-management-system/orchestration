<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
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
  <hint-card v-if="staticLocationActions.length === 0">
    There are no locations for the associated configurations.
  </hint-card>
  <div v-else>
    <v-alert
      dense
      type="info"
    >
      <p class="mb-0">
        Select a marker on the map to show information about the location.
      </p>
    </v-alert>
    <v-card id="map-wrap" style="height: 300px" class="mb-4">
      <no-ssr>
        <l-map
          ref="map"
          :zoom="zoomLevel"
          :center="currentPosition"
          style="z-index:0"
          :bounds="bounds"
          @click="selectedLocationAction = null"
        >
          <l-tile-layer layer url="https://{s}.tile.osm.org/{z}/{x}/{y}.png" />
          <l-polygon
            v-if="showSitePolygon && polygon"
            ref="polygon"
            :lat-lngs="polygon"
            :color="polylineColor"
            :fill="true"
          />
          <l-marker
            v-for="locationAction in staticLocationActions"
            :key="locationAction.id"
            :lat-lng="location(locationAction)"
            @click="select(locationAction)"
          >
            <l-icon
              :icon-url="locationAction === selectedLocationAction ? require(`~/assets/marker-icon-red.png`) : require(`~/assets/marker-icon.png`)"
            />
          </l-marker>
        </l-map>
      </no-ssr>
    </v-card>
    <v-card v-if="selectedLocationAction">
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <label>Configuration</label>
            {{ configurationLabel | orDefault }}
          </v-col>
          <v-col cols="12" md="6">
            <label>Label</label>
            {{ selectedLocationAction.label | orDefault }}
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <label>Begin date</label>
            {{ selectedLocationAction.beginDate | toUtcDateTimeStringHHMM }}
            <span class="text-caption text--secondary">(UTC)</span>
          </v-col>
          <v-col cols="12" md="6">
            <label>End date</label>
            {{ selectedLocationAction.endDate | toUtcDateTimeStringHHMM | orDefault }}
            <span v-if="selectedLocationAction.endDate" class="text-caption text--secondary">(UTC)</span>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          small
          color="primary"
          :to="'/configurations/' + selectedLocationAction.configurationId + '/locations/static-location-actions/' + selectedLocationAction.id"
        >
          View
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { LatLng, LatLngBounds, latLngBounds } from 'leaflet'

import { Configuration } from '@/models/Configuration'
import { StaticLocationAction } from '@/models/StaticLocationAction'

import HintCard from '@/components/HintCard.vue'

import { SetLoadingAction } from '@/store/progressindicator'
import { SitesState, LoadSiteAction, LoadSiteConfigurationsAction } from '@/store/sites'

@Component({
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('sites', ['loadSite', 'loadSiteConfigurations'])
  },
  computed: mapState('sites', ['site', 'siteConfigurations']),
  components: {
    HintCard
  }
})
export default class SiteLocations extends Vue {
  private staticLocationActions: StaticLocationAction[] = []
  private polylineColor: string = 'green'
  private zoomLevel = 10
  private showSitePolygon = true

  private currentPosition: LatLng = new LatLng(52, 12)
  private bounds: LatLngBounds = latLngBounds([this.currentPosition])
  private selectedLocationAction: StaticLocationAction | null = null

  // vuex definition for typescript check
  loadSite!: LoadSiteAction
  loadSiteConfigurations!: LoadSiteConfigurationsAction
  site!: SitesState['site']
  siteConfigurations!: SitesState['siteConfigurations']
  setLoading!: SetLoadingAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all(
        [
          this.loadSite({ siteId: this.siteId }),
          this.loadSiteConfigurations(this.siteId)
        ]
      )
      this.staticLocationActions = await this.$api.staticLocationActions.getRelatedActionsForSite(this.siteId)
      const locations = this.staticLocationActions.map((x: StaticLocationAction) => this.location(x)).filter(x => x !== null) as LatLng[]
      if (locations) {
        this.bounds = latLngBounds(locations)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch locations')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId (): string {
    return this.$route.params.siteId
  }

  get polygon () {
    if (!this.site) {
      return null
    }
    return this.site.geometry
  }

  get configurationLabel (): string | null {
    if (this.selectedLocationAction === null) {
      return null
    }
    if (!this.siteConfigurations) {
      return this.selectedLocationAction.configurationId
    }
    const found = this.siteConfigurations.filter((x: Configuration) => x.id === this.selectedLocationAction?.configurationId)
    if (found) {
      return found[0].label
    }
    return null
  }

  location (locationAction: StaticLocationAction): LatLng | null {
    if (locationAction.x === null || locationAction.y === null) {
      return null
    }
    const result = new LatLng(locationAction!.y, locationAction!.x)
    return result
  }

  select (locationAction: StaticLocationAction) {
    this.selectedLocationAction = locationAction
  }
}
</script>
