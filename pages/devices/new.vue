<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
  <div>
    <v-card
      outlined
    >
      <v-tabs-items
        v-model="activeTab"
      >
        <v-tab-item :eager="true">
          <DeviceBasicDataForm v-model="device" />
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </div>
</template>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'

import AttachmentList from '@/components/AttachmentList.vue'
import ContactSelect from '@/components/ContactSelect.vue'
import CustomFieldCards from '@/components/CustomFieldCards.vue'
import DevicePropertyExpansionPanels from '@/components/DevicePropertyExpansionPanels.vue'
import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'

@Component({
  components: {
    DeviceBasicDataForm
  }
})
// @ts-ignore
export default class DeviceNewPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private device: Device = new Device()

  created () {
    this.initializeAppBar()
    this.registerButtonActions()
  }

  mounted () {
    this.$store.commit('appbar/setTitle', 'Add Device')
  }

  beforeDestroy () {
    this.unregisterButtonActions()
    this.$store.dispatch('appbar/setDefaults')
  }

  registerButtonActions () {
    this.$nuxt.$on('AppBarEditModeContent:save-btn-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarEditModeContent:cancel-btn-click', () => {
      this.cancel()
    })
  }

  unregisterButtonActions () {
    this.$nuxt.$off('AppBarEditModeContent:save-btn-click')
    this.$nuxt.$off('AppBarEditModeContent:cancel-btn-click')
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        'Basic Data'
      ],
      title: 'Add Device',
      saveBtnHidden: false,
      cancelBtnHidden: false
    })
  }

  get activeTab (): number | null {
    return this.$store.state.appbar.activeTab
  }

  set activeTab (tab: number | null) {
    this.$store.commit('appbar/setActiveTab', tab)
  }

  save (): void {
    this.$api.devices.save(this.device).then((savedDevice) => {
      if (this.isLoggedIn) {
        this.$router.push('/devices/show/' + savedDevice.id + '')
      } else {
        throw new Error('You need to be logged in to save the device')
      }
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  cancel () {
    this.$router.push('/search/devices')
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
