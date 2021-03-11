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
        v-for="(field, index) in properties"
      >
        <NuxtChild
          :key="'property-' + index"
          v-model="properties[index]"
          @delete="deleteProperty"
        />
      </template>
    </v-expansion-panels>
    <v-card-actions
      v-if="properties.length > 3"
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
import { Component, Vue } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class DevicePropertiesPage extends Vue {
  private openedPanels: number[] = []
  private properties: DeviceProperty[] = []
  private isLoading = false
  private isSaving = false

  mounted () {
    this.isLoading = true
    this.$api.devices.findRelatedDeviceProperties(this.deviceId).then((foundProperties) => {
      this.properties = foundProperties
      this.isLoading = false
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch custom fields')
      this.isLoading = false
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

  addProperty (): void {
  }

  deleteProperty (property: DeviceProperty) {
  }
}
</script>
