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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditCustomFieldsPage"
        color="primary"
        small
        @click="addField"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <template
      v-for="(field, index) in customFields"
    >
      <NuxtChild
        :key="'customfield-' + index"
        v-model="customFields[index]"
        @delete="deleteField"
      />
    </template>
    <v-card-actions
      v-if="customFields.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        :disabled="isEditCustomFieldsPage"
        color="primary"
        small
        @click="addField"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { CustomTextField } from '@/models/CustomTextField'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsPage extends Vue {
  private customFields: CustomTextField[] = []
  private isLoading = false
  private isSaving = false

  mounted () {
    this.isLoading = true
    this.$api.devices.findRelatedCustomFields(this.deviceId).then((foundFields) => {
      this.customFields = foundFields
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

  get isEditCustomFieldsPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/customfields\/([0-9]+)\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  addField (): void {
    const field = new CustomTextField()
    this.isSaving = true
    this.$api.customfields.add(this.deviceId, field).then((newField: CustomTextField) => {
      this.isSaving = false
      this.customFields.push(newField)
      this.$router.push('/devices/' + this.deviceId + '/customfields/' + newField.id + '/edit')
    }).catch(() => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    })
  }

  deleteField (field: CustomTextField) {
    if (!field.id) {
      return
    }
    this.$api.customfields.deleteById(field.id).then(() => {
      const index: number = this.customFields.findIndex((f: CustomTextField) => f.id === field.id)
      if (index > -1) {
        this.customFields.splice(index, 1)
      }
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to delete custom field')
    })
  }
}
</script>
