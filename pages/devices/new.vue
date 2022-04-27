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
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          @save="save"
          save-btn-text="create"
        />
      </v-card-actions>
      <DeviceBasicDataForm
        ref="basicForm"
        v-model="device"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/devices'"
          @save="save"
          save-btn-text="create"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'

import DeviceBasicDataForm from '@/components/DeviceBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions } from 'vuex'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    DeviceBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  methods:{
    ...mapActions('devices',['saveDevice']),
    ...mapActions('appbar',['initDevicesNewAppBar','setDefaults'])
  }
})
// @ts-ignore
export default class DeviceNewPage extends mixins(Rules) {
  private device: Device = new Device()
  private isLoading: boolean = false

  created () {
    this.initDevicesNewAppBar()
  }

  beforeDestroy () {
    this.setDefaults()
  }

  async save (): void {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isLoading = true
      const savedDevice = await this.saveDevice(this.device)
      this.$store.commit('snackbar/setSuccess', 'Device created')
      this.$router.push('/devices/' + savedDevice.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }

  }

}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
