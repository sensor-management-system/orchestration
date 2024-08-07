<!--
SPDX-FileCopyrightText: 2020 - 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <div
      class="mapContainer my-2"
      :style="{ height: mapState.height + 'px'}"
      :class="{ mapHover: mapHovered, draggerHover: draggerHovered }"
    >
      <l-map
        ref="map"
        class="map"
        :zoom="mapState.zoom"
        :center="mapState.center"
        :bounds="mapState.bounds"
        @update:zoom="updateZoom"
        @update:center="updateCenter"
        @update:bounds="updateBounds"
        @click="onClick"
        @ready="onReady"
        @locationfound="onLocationFound"
        @mouseenter="onMapHoverBegin"
        @mouseleave="onMapHoverEnd"
      >
        <l-tile-layer
          url="https://{s}.tile.osm.org/{z}/{x}/{y}.png"
        />
        <slot
          name="default"
        >
          <!-- Include components like markers or polygons here -->
        </slot>
        <v-geosearch
          v-if="!disableGeosearch"
          :options="geosearchOptions"
        />
        <l-control-scale
          v-if="!disableScale"
          position="bottomleft"
          :imperial="true"
          :metric="true"
          :max-width="150"
        />
        <l-control
          v-if="localizationButton"
          position="bottomright"
        >
          <v-btn
            fab
            small
            :disabled="isLocating"
            @click.stop="locate"
          >
            <v-icon v-if="!isLocating">
              mdi-map-marker-account
            </v-icon>
            <v-progress-circular v-else indeterminate />
          </v-btn>
        </l-control>
      </l-map>
      <div
        v-if="resizable"
        class="reziseDragger"
        @mousedown="initResize"
        @mouseup="stopResize"
        @mouseenter="onDraggerHoverBegin"
        @mouseleave="onDraggerHoverEnd"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch, Emit } from 'nuxt-property-decorator'

import { LMap, LMarker, LTileLayer, LPolygon, LControl } from 'vue2-leaflet'
import { LatLng, LatLngBounds, LeafletMouseEvent, LocationEvent, Map } from 'leaflet'
import { OpenStreetMapProvider } from 'leaflet-geosearch'
import VGeosearch from '@/components/shared/Vue2LeafletGeosearch.vue'

export interface MapState {
  center?: LatLng | null
  height?: number | null
  zoom?: number | null
  bounds?: LatLngBounds | null
}

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
export default class BaseMap extends Vue {
  @Prop({
    required: false,
    type: Object
  })
  /**
   * Controls the map state.
   * Use with v-model.
   */
  readonly value!: MapState

  // Map components

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  /**
   * Hides the map's geosearch.
   */
  readonly disableGeosearch!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  /**
   * Hides the map's scale control.
   */
  readonly disableScale!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  /**
   * Shows a button for locating the user's current position in the bottom right corner.
   */
  readonly localizationButton!: boolean

  // Localization behaviour

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  /**
   * Performs an initial localization.
   */
  readonly initialLocalization!: boolean

  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  /**
   * Sets the map center to the user's current position after localization changed.
   */
  readonly recenterOnLocalization!: boolean

  // Map height

  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  /**
   * Enables dynamic resizing by dragging the map bottom.
   */
  readonly resizable!: boolean

  @Prop({
    default: 200,
    required: false,
    type: Number
  })
  /**
   * The minimum height for dynamic resizing.
   */
  readonly resizingMinHeight!: number

  @Prop({
    default: 800,
    required: false,
    type: Number
  })
  /**
   * The maximum height for dynamic resizing.
   */
  readonly resizingMaxHeight!: number

  @Prop({
    default: 'default',
    required: false,
    type: String
  })
  /**
   * The key for storing the dynamic size in the user's local storage.
   * Initial size is set to the respective stored value.
   */
  readonly heightStorageKey!: string

  private mapState: MapState = {
    height: 300,
    center: new LatLng(52, 12),
    zoom: 10,
    bounds: null
  }

  private provider = new OpenStreetMapProvider()
  private geosearchOptions: Object = {
    ref: 'searchControl',
    provider: this.provider,
    style: 'button',
    autoComplete: true,
    showMarker: false
  }

  private location: LatLng | null = null
  private isLocating: Boolean = false

  private mapHovered: Boolean = false
  private draggerHovered: Boolean = false
  private isResizing: Boolean = false

  @Watch('value', { immediate: true, deep: true })
  input (newValue: MapState) {
    if (!newValue) {
      return
    }
    this.mapState.height = newValue.height ?? this.mapState.height
    this.mapState.zoom = newValue.zoom ?? this.mapState.zoom
    this.mapState.bounds = newValue.bounds ?? this.mapState.bounds
    this.mapState.center = newValue.center ?? this.mapState.center
  }

  updateZoom (zoom: number | null) {
    this.mapState.zoom = zoom
  }

  updateBounds (bounds: LatLngBounds | null) {
    this.mapState.bounds = bounds
  }

  updateCenter (center: LatLng | null) {
    this.mapState.center = center
  }

  @Emit('input')
  @Watch('mapState', { deep: true })
  update () {
    return this.mapState
  }

  created () {
    if (!this.resizable) {
      return
    }
    const storedMapHeight = localStorage.getItem(this.localStorageMapHeightKey)
    if (storedMapHeight) {
      this.mapState.height = parseInt(storedMapHeight)
    }
  }

  mounted () {
    if (this.resizable) {
      window.addEventListener('mousemove', this.doMapResize)
      window.addEventListener('mouseup', this.stopResize)
    }
  }

  destroyed () {
    window.removeEventListener('mousemove', this.doMapResize)
    window.removeEventListener('mouseup', this.stopResize)
  }

  get mapObject (): Map | null {
    const mapRef: any | null = this.$refs.map
    const mapObject: Map | null = mapRef?.mapObject ?? null
    return mapObject
  }

  @Emit('ready')
  onReady (mapObject: Map) {
    mapObject.on('locationerror', this.onLocationError)
    mapObject.on('locationfound', this.onLocationFound)

    if (this.initialLocalization) {
      this.locate()
    }
  }

  // Localization

  locate () {
    if (!this.mapObject) {
      return
    }
    this.mapObject.locate()
    this.isLocating = true
  }

  @Emit('locationfound')
  onLocationFound (location: LocationEvent) {
    this.isLocating = false
    this.location = location.latlng
    return location
  }

  @Emit('locationerror')
  onLocationError () {
    this.isLocating = false
    this.$store.commit('snackbar/setError', 'Location could not be determined.')
  }

  @Emit('locationchange')
  @Watch('location', { deep: true })
  onLocationChange (location: LatLng | null) {
    if (this.recenterOnLocalization) {
      this.mapState.center = location
    }
    return location
  }

  @Emit('click')
  onClick (event: LeafletMouseEvent) {
    return event
  }

  get localStorageMapHeightKey () {
    return `map-height-${this.heightStorageKey}`
  }

  // Dynamic resizing

  initResize () {
    this.isResizing = true
    document.body.style.userSelect = 'none'
  }

  doMapResize (event: MouseEvent) {
    if (!this.isResizing || !this.$refs.map) {
      return
    }

    const mapElement = this.$refs.map as Vue & {
      mapObject: Map
      $el: HTMLElement
    }
    const newHeight = event.clientY - mapElement.$el.getBoundingClientRect().top

    if (newHeight >= this.resizingMinHeight && newHeight <= this.resizingMaxHeight) {
      this.mapState.height = newHeight
    }
  }

  @Watch('mapState.height')
  invalidateSize () {
    const mapElement = this.$refs.map as Vue & {
      mapObject: {
        invalidateSize: () => void;
      },
      $el: HTMLElement
    }
    if (!mapElement) {
      return
    }
    this.$nextTick(() => mapElement.mapObject.invalidateSize())
  }

  stopResize () {
    this.isResizing = false
    document.body.style.userSelect = 'auto'
    localStorage.setItem(this.localStorageMapHeightKey, String(this.mapState.height))
  }

  // Hover effects

  onMapHoverBegin () {
    this.mapHovered = !!this.resizable
  }

  onMapHoverEnd () {
    this.mapHovered = false
  }

  onDraggerHoverBegin () {
    this.draggerHovered = !!this.resizable
  }

  onDraggerHoverEnd () {
    this.draggerHovered = false
  }
}
</script>

<style scoped>
@import '~/assets/leaflet-geosearch@2.6.0.css';

.reziseDragger {
  height: 20px;
  cursor: ns-resize;
  width: 100%;
  z-index: 1000;
  position: relative;
  bottom: 10px;
}

.mapContainer {
  border-bottom: 2px solid transparent;
  transition: border .3s;
  padding-bottom: 4px;
}

.map {
  z-index: 0;
}

@media all and (min-width: 960px) {
  /* disable hover effects for mobile devices */
  .mapContainer.mapHover {
    border-bottom: 2px solid #bbb;
    transition: border .3s;
  }

  .mapContainer.draggerHover {
    border-bottom: 2px solid black;
    transition: border .3s;
  }
}
</style>
