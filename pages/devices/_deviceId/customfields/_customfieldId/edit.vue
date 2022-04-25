<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
      v-model="isSaving"
      dark
    />
    <CustomFieldCardForm
      ref="customFieldCardForm"
      v-model="valueCopy"
    >
      <template #actions>
        <v-btn
          v-if="$auth.loggedIn"
          ref="cancelButton"
          text
          small
          nuxt
          :to="'/devices/' + deviceId + '/customfields'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="$auth.loggedIn"
          color="green"
          small
          @click="save()"
        >
          Apply
        </v-btn>
      </template>
    </CustomFieldCardForm>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import { CustomTextField } from '@/models/CustomTextField'

import CustomFieldCardForm from '@/components/CustomFieldCardForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { mapActions, mapState } from 'vuex'

@Component({
  components: {
    CustomFieldCardForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('devices',['deviceCustomField']),
  methods: mapActions('devices',['loadDeviceCustomField','loadDeviceCustomFields','updateDeviceCustomField'])
})
export default class DeviceCustomFieldsShowPage extends Vue {
  private isSaving: boolean = false
  private valueCopy: CustomTextField = new CustomTextField()

  async created () {
    await this.loadDeviceCustomField(this.customFieldId);
    this.valueCopy = CustomTextField.createFromObject(this.deviceCustomField)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get customFieldId():string{
    return this.$route.params.customfieldId;
  }

  async save (): void {

    try {
      this.isSaving = true
      await this.updateDeviceCustomField({
        deviceId: this.deviceId,
        deviceCustomField: this.valueCopy
      })
      this.loadDeviceCustomFields(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
