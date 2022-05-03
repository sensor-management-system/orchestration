<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
      v-model="isSaving"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <CustomFieldForm
          v-model="customField"
          :readonly="false"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions } from 'vuex'
import CustomFieldForm from '@/components/CustomFieldForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { CustomTextField } from '@/models/CustomTextField'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  middleware: ['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons, CustomFieldForm },
  methods: mapActions('devices', ['addDeviceCustomField', 'loadDeviceCustomFields'])
})
export default class DeviceCustomFieldAddPage extends Vue {
  private isSaving = false

  private customField: CustomTextField = new CustomTextField()

  // vuex definition for typescript check
  loadDeviceCustomFields!:(id: string)=>void
  addDeviceCustomField!:({
    deviceId,
    deviceCustomField
  }: { deviceId: string, deviceCustomField: CustomTextField })=> Promise<void>

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {
    try {
      this.isSaving = true

      await this.addDeviceCustomField({
        deviceId: this.deviceId,
        deviceCustomField: this.customField
      })
      this.loadDeviceCustomFields(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New custom field added')
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
