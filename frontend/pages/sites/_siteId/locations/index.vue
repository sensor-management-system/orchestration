<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <hint-card v-if="staticLocationActions.length === 0 && innerSites.length === 0">
    There are no locations for the associated configurations or related sites.
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
          @click="resetSelection"
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
          <l-polygon
            v-for="site in innerSites"
            :key="site.id"
            :lat-lngs="polygonOfSite(site)"
            :color="site === selectedSite ? innerSitePolygonColorSelected : innerSitePolygonColor"
            :fill-color="site === selectedSite ? innerSitePolygonFillColorSelected : innerSitePolygonFillColor"
            :fill="true"
            @click="selectSite(site)"
          />
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
    <v-card v-if="selectedSite">
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <label>Site</label>
            {{ selectedSite.label | orDefault }}
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <label>Usage</label>
            {{ selectedSite.siteUsageName | orDefault }}
          </v-col>
          <v-col cols="12" md="6">
            <label>Type</label>
            {{ selectedSite.siteTypeName | orDefault }}
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <label>Street</label>
            {{ [selectedSite.address.street, selectedSite.address.streetNumber] | sparseJoin(' ') | orDefault }}
          </v-col>
          <v-col cols="12" md="3">
            <label>City</label>
            {{ [selectedSite.address.zipCode, selectedSite.address.city] | sparseJoin(' ') | orDefault }}
          </v-col>
          <v-col cols="12" md="3">
            <label>Country</label>
            {{ selectedSite.address.country | orDefault }}
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="3">
            <label>Building - Room</label>
            {{ [selectedSite.address.building, selectedSite.address.room] | sparseJoin(' ') | orDefault }}
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          small
          color="primary"
          :to="'/sites/' + selectedSite.id + '/locations'"
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
import { SitesState, LoadSiteAction, LoadSiteConfigurationsAction, SearchSitesAction } from '@/store/sites'
import { Site } from '@/models/Site'

@Component({
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('sites', ['loadSite', 'loadSiteConfigurations', 'searchSites'])
  },
  computed: mapState('sites', ['site', 'siteConfigurations', 'sites']),
  components: {
    HintCard
  }
})
export default class SiteLocations extends Vue {
  private staticLocationActions: StaticLocationAction[] = []
  private polylineColor: string = 'green'
  private innerSitePolygonColor: string = 'blue'
  private innerSitePolygonColorSelected: string = 'red'
  private innerSitePolygonFillColor: string = '#3388ff'
  private innerSitePolygonFillColorSelected: string = '#ff8833'
  private zoomLevel = 10
  private showSitePolygon = true
  private clickedOnPolygon = false

  private currentPosition: LatLng = new LatLng(-52, -12)
  private bounds: LatLngBounds = latLngBounds([this.currentPosition])
  private selectedLocationAction: StaticLocationAction | null = null
  private selectedSite: Site | null = null

  // vuex definition for typescript check
  loadSite!: LoadSiteAction
  loadSiteConfigurations!: LoadSiteConfigurationsAction
  site!: SitesState['site']
  sites!: SitesState['sites']
  siteConfigurations!: SitesState['siteConfigurations']
  setLoading!: SetLoadingAction
  searchSites!: SearchSitesAction

  async fetch () {
    try {
      this.setLoading(true)
      await Promise.all(
        [
          this.loadSite({ siteId: this.siteId, includeImages: true }),
          this.loadSiteConfigurations(this.siteId),
          this.searchSites()
        ]
      )
      this.staticLocationActions = await this.$api.staticLocationActions.getRelatedActionsForSite(this.siteId)
      const locations = this.staticLocationActions.map((x: StaticLocationAction) => this.location(x)).filter(x => x !== null) as LatLng[]
      let boundsSetByData = false
      if (locations) {
        this.bounds = latLngBounds(locations)
        boundsSetByData = true
      }
      for (const innerSite of this.innerSites) {
        const polygonOfSite = this.polygonOfSite(innerSite)
        if (polygonOfSite) {
          if (!boundsSetByData) {
            this.bounds = latLngBounds(polygonOfSite)
            boundsSetByData = true
          } else {
            this.bounds.extend(latLngBounds(polygonOfSite))
          }
        }
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
    return this.polygonOfSite(this.site)
  }

  polygonOfSite (site: Site | null) {
    if (!site) {
      return null
    }
    return site.geometry
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
    this.selectedSite = null
  }

  selectSite (site: Site) {
    this.selectedSite = site
    this.selectedLocationAction = null
    this.clickedOnPolygon = true
  }

  get innerSites () {
    return this.sites.filter(x => x.outerSiteId === this.site?.id).filter(s => this.polygonOfSite(s) !== null)
  }

  resetSelection () {
    // Here we need to have a workaround in order to not unselect the site.
    // Background here is that on a click on a polygon we also trigger the
    // click on the map.
    // Without this additional handling we would unselect the site all the time
    // (even directly after a click on a site).
    if (!this.clickedOnPolygon) {
      this.selectedSite = null
    }
    this.selectedLocationAction = null
    this.clickedOnPolygon = false
  }
}
</script>
