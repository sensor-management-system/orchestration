<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditPropertiesPage"
        color="primary"
        small
        @click="addProperty"
      >
        Add Property
      </v-btn>
    </v-card-actions>
    <v-expansion-panels
      v-model="openedPanels"
      multiple
    >
      <template
        v-for="(field, index) in deviceProperties"
      >
        <NuxtChild
          :key="'property-' + index"
          v-model="deviceProperties[index]"
          :compartments="compartments"
          :sampling-medias="samplingMedias"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
          @delete="deleteProperty"
        />
      </template>
    </v-expansion-panels>
    <v-card-actions
      v-if="deviceProperties.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditPropertiesPage"
        color="primary"
        small
        @click="addProperty"
      >
        Add Property
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class DevicePropertiesPage extends Vue {
  private openedPanels: number[] = []
  private deviceProperties: DeviceProperty[] = []
  private isLoading = false
  private isSaving = false

  private compartments: Compartment[] = []
  private samplingMedias: SamplingMedia[] = []
  private properties: Property[] = []
  private units: Unit[] = []
  private measuredQuantityUnits: MeasuredQuantityUnit[] = []

  mounted () {
    this.isLoading = true
    this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundProperties) => {
      this.deviceProperties = foundProperties
      this.isLoading = false
      this.openSelectedPanel()
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch properties')
      this.isLoading = false
    })
    this.$api.compartments.findAllPaginated().then((foundCompartments) => {
      this.compartments = foundCompartments
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of compartments failed')
    })
    this.$api.samplingMedia.findAllPaginated().then((foundSamplingMedias) => {
      this.samplingMedias = foundSamplingMedias
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of sampling medias failed')
    })
    this.$api.properties.findAllPaginated().then((foundProperties) => {
      this.properties = foundProperties
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of properties failed')
    })
    this.$api.units.findAllPaginated().then((foundUnits) => {
      this.units = foundUnits
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of units failed')
    })
    this.$api.measuredQuantityUnits.findAllPaginated().then((foundUnits) => {
      this.measuredQuantityUnits = foundUnits
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of measuredquantityunits failed')
    })
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditPropertiesPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/properties\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  getPropertyIdFromUrl (): string | undefined {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/properties\/([0-9]+)\/?.*$'
    const matches = this.$route.path.match(editUrl)
    if (!matches) {
      return
    }
    return matches[1]
  }

  openSelectedPanel (): void {
    const propertyId = this.getPropertyIdFromUrl()
    console.log('propertyId by URL is', propertyId)
    if (!propertyId) {
      return
    }
    const propertyIndex: number = this.deviceProperties.findIndex((prop: DeviceProperty) => prop.id === propertyId)
    console.log('propertyIndex is', propertyIndex)
    if (propertyIndex === -1) {
      return
    }
    Vue.set(this, 'openedPanels', [propertyIndex])
  }

  addProperty (): void {
    const property = new DeviceProperty()
    this.isSaving = true
    this.$api.deviceProperties.add(this.deviceId, property).then((newProperty: DeviceProperty) => {
      this.isSaving = false
      this.deviceProperties.push(newProperty)
      this.$router.push('/devices/' + this.deviceId + '/properties/' + newProperty.id + '/edit')
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save property')
    })
  }

  deleteProperty (property: DeviceProperty) {
    if (!property.id) {
      return
    }
    this.$api.deviceProperties.deleteById(property.id).then(() => {
      const index: number = this.deviceProperties.findIndex((p: DeviceProperty) => p.id === property.id)
      if (index > -1) {
        this.deviceProperties.splice(index, 1)
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to delete property')
    })
  }

  @Watch('$route', { immediate: true, deep: true })
  // @ts-ignore
  onRouteChanged () {
    this.openSelectedPanel()
    console.log('route changed', this.openedPanels)
  }
}
</script>
