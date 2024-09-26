<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <BaseMap
    ref="map"
    v-model="mapState"
    height-storage-key="site-overview"
    @click="resetSelection"
  >
    <l-control
      :position="'bottomright'"
    >
      <v-tooltip right>
        <template #activator="{ on }">
          <v-btn
            style="background: white"
            icon
            outlined
            large
            @click="fitToAllSites"
            v-on="on"
          >
            <v-icon>mdi-overscan</v-icon>
          </v-btn>
        </template>
        <span>Fit map to listed sites</span>
      </v-tooltip>
    </l-control>
    <l-control :position="'bottomright'">
      <v-tooltip right>
        <template #activator="{ on }">
          <v-btn
            style="background: white"
            icon
            outlined
            large
            :color="`${markerVisible? 'blue': ''}`"
            v-on="on"
            @click="markerVisible =! markerVisible"
          >
            <v-icon>
              mdi-map-marker-check
            </v-icon>
          </v-btn>
        </template>
        Toggle visibility of site marker
      </v-tooltip>
    </l-control>
    <l-control-layers
      v-if="visibleSortedSites.length > 0"
      position="topright"
      :sort-layers="true"
    />
    <l-layer-group
      v-for="(site,index) of visibleSortedSites"
      :key="index"
      layer-type="overlay"
      :name="site.label"
    >
      <l-polygon
        :lat-lngs="site.geometry"
        :color="site === selectedSite ? polygonColorSelected : polygonColor"
        :fill-color="site === selectedSite ? polygonFillColorSelected : polygonFillColor"
        :fill="true"
        @click="selectSite(site)"
      >
        <site-overview-map-popup
          :value="site"
        >
          <template #additonal-actions="{popupSite}">
            <slot name="popup-additonal-actions" :site="popupSite" />
          </template>
        </site-overview-map-popup>
      </l-polygon>
      <l-marker
        :lat-lng="calculateCentroid(site.geometry)"
        :visible="markerVisible"
        @click="selectSite(site)"
      >
        <site-overview-map-popup
          :value="site"
          @close-popup="closePopup"
        >
          <template #additonal-actions="{popupSite}">
            <slot name="popup-additonal-actions" :site="popupSite" />
          </template>
        </site-overview-map-popup>
      </l-marker>
    </l-layer-group>
  </BaseMap>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { LMap } from 'vue2-leaflet'
import { LatLng, latLngBounds, LatLngBoundsExpression, Polygon } from 'leaflet'
import { SitesState } from '@/store/sites'
import { ILatLng, Site } from '@/models/Site'
import BaseMap, { MapState } from '@/components/shared/BaseMap.vue'
import SiteOverviewMapPopup from '@/components/sites/SiteOverviewMapPopup.vue'
import { calculatePolygonArea } from '@/utils/mapHelpers'

@Component({
  components: {
    SiteOverviewMapPopup,
    BaseMap,
    LMap
  }
})
export default class SiteOverviewMap extends Vue {
  @Prop({
    default: () => [],
    type: Array
  })
  readonly value!: SitesState['sites']

  private mapState: MapState = {
    center: new LatLng(52, 12),
    zoom: 6
  }

  private markerVisible = true
  private selectedSite: Site | null = null
  private polygonColor: string = 'blue'
  private polygonColorSelected: string = 'red'
  private polygonFillColor: string = '#3388ff'
  private polygonFillColorSelected: string = '#ff8833'

  created () {
    this.mapState.bounds = this.boundingBox
  }

  toggleMarkerVisibility () {
    this.markerVisible = !this.markerVisible
  }

  get sitesWithGeometry () {
    return this.value
      .filter((site: Site) => {
        return site.geometry.length > 0
      })
  }

  get visibleSortedSites () {
    if (this.mapState.bounds) {
      return this.sitesWithGeometry
        .filter((site: Site) => {
          const polygon = new Polygon(site.geometry)
          return this.mapState.bounds!.intersects(polygon.getBounds())
        })
        .map((site: Site) => {
          const polygon = new Polygon(site.geometry)
          const latLngs = polygon.getLatLngs()

          // Check if latLngs is an array of arrays (LatLng[][]), flatten if necessary
          const firstLatLngArray = Array.isArray(latLngs[0])
            ? (latLngs[0] as LatLng[])
            : (latLngs as LatLng[])
          const area = calculatePolygonArea(firstLatLngArray)
          return { site, area }
        }).sort((a, b) => b.area - a.area).map(entry => entry.site)
    }

    return []
  }

  get boundingBox () {
    const sitegeometries = this.sitesWithGeometry.map((site: Site) => {
      return site.geometry.map((point: ILatLng) => {
        return new LatLng(point.lat, point.lng)
      })
    }).flat()

    return latLngBounds(sitegeometries)
  }

  public fitToAllSites () {
    this.showOnMap(this.boundingBox)
    this.updateMapSize()
  }

  public selectAndShowOnMap (site: Site): void {
    this.selectedSite = site
    const latLngTuples = site.geometry.map((latLng: ILatLng): [number, number] => {
      return [latLng.lat, latLng.lng]
    })
    this.showOnMap(latLngTuples)
  }

  showOnMap (geometry: LatLngBoundsExpression): void {
    setTimeout(() => {
      const mapComponent = this.$refs.map as BaseMap
      mapComponent.mapObject?.fitBounds(geometry)
    }, 200)
  }

  updateMapSize (): void {
    setTimeout(() => {
      const mapComponent = this.$refs.map as BaseMap
      mapComponent.mapObject?.invalidateSize()
    }, 100)
  }

  calculateCentroid (coords: ILatLng[]) { // made by chatgpt
    const bounda = latLngBounds(coords)
    return bounda.getCenter()
  }

  selectSite (site: Site) {
    this.selectedSite = site
    this.$emit('siteSelected', site)
  }

  resetSelection () {
    this.selectedSite = null
  }

  closePopup () {
    const mapComponent = this.$refs.map as BaseMap
    mapComponent.mapObject?.closePopup()
  }

  @Watch('value', { immediate: true })
  onValueChange (_newValue: SitesState['sites'], _oldValue: SitesState['sites']) {
    // Update the map if the value changed
    this.mapState.bounds = this.boundingBox
    this.updateMapSize()
  }
}
</script>

<style scoped>
.popup-card {
  width: 400px; /* Adjust this width to prevent text wrapping */
}
</style>
