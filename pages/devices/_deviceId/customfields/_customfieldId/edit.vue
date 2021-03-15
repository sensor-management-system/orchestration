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
          v-if="isLoggedIn"
          text
          small
          nuxt
          :to="'/devices/' + deviceId + '/customfields'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
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

@Component({
  components: {
    CustomFieldCardForm,
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
  private isSaving: boolean = false
  private valueCopy: CustomTextField = new CustomTextField()

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  created () {
    this.valueCopy = CustomTextField.createFromObject(this.value)
  }

  mounted () {
    (this.$refs.customFieldCardForm as Vue & { focus: () => void}).focus()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  save (): void {
    this.isSaving = true
    this.$api.customfields.update(this.deviceId, this.valueCopy).then((newField: CustomTextField) => {
      this.isSaving = false
      this.$emit('input', newField)
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    })
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: CustomTextField) {
    this.valueCopy = CustomTextField.createFromObject(val)
  }
}
</script>
