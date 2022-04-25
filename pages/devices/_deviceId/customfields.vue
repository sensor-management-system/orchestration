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
  <NuxtChild/>
<!--  <div>-->
<!--    <ProgressIndicator-->
<!--      v-model="isInProgress"-->
<!--      :dark="isSaving"-->
<!--    />-->
<!--    <v-card-actions>-->
<!--      <v-spacer />-->
<!--      <v-btn-->
<!--        v-if="$auth.loggedIn"-->
<!--        :disabled="isEditCustomFieldsPage"-->
<!--        color="primary"-->
<!--        small-->
<!--        @click="addField"-->
<!--      >-->
<!--        Add Custom Field-->
<!--      </v-btn>-->
<!--    </v-card-actions>-->
<!--    <v-card-actions-->
<!--      v-if="customFields.length > 3"-->
<!--    >-->
<!--      <v-spacer />-->
<!--      <v-btn-->
<!--        v-if="$auth.loggedIn"-->
<!--        :disabled="isEditCustomFieldsPage"-->
<!--        color="primary"-->
<!--        small-->
<!--        @click="addField"-->
<!--      >-->
<!--        Add Custom Field-->
<!--      </v-btn>-->
<!--    </v-card-actions>-->
<!--  </div>-->
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { CustomTextField } from '@/models/CustomTextField'

import { mapActions } from 'vuex'

@Component({
  methods:mapActions('devices',['loadDeviceCustomFields'])
})
export default class DeviceCustomFieldsPage extends Vue {
  async created(){
    try {
      await this.loadDeviceCustomFields(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch custom fields')
    }
  }
  head () {
    return {
      titleTemplate: 'Custom Fields - %s'
    }
  }
  get deviceId (): string {
    return this.$route.params.deviceId
  }
  //
  // get isEditCustomFieldsPage (): boolean {
  //   // eslint-disable-next-line no-useless-escape
  //   const editUrl = '^\/devices\/' + this.deviceId + '\/customfields\/([0-9]+)\/edit$'
  //   return !!this.$route.path.match(editUrl)
  // }
  //
  // addField (): void {
  //   const field = new CustomTextField()
  //   this.isSaving = true
  //   this.$api.customfields.add(this.deviceId, field).then((newField: CustomTextField) => {
  //     this.isSaving = false
  //     this.customFields.push(newField)
  //     this.$router.push('/devices/' + this.deviceId + '/customfields/' + newField.id + '/edit')
  //   }).catch(() => {
  //     this.isSaving = false
  //     this.$store.commit('snackbar/setError', 'Failed to save custom field')
  //   })
  // }
  //
  // deleteAndCloseDialog (field: CustomTextField) {
  //   if (!field.id) {
  //     return
  //   }
  //   this.$api.customfields.deleteById(field.id).then(() => {
  //     const index: number = this.customFields.findIndex((f: CustomTextField) => f.id === field.id)
  //     if (index > -1) {
  //       this.customFields.splice(index, 1)
  //     }
  //   }).catch(() => {
  //     this.$store.commit('snackbar/setError', 'Failed to delete custom field')
  //   })
  //
  //   this.showDeleteDialog = {}
  // }
  //
  // showDeleteDialogFor (id: string) {
  //   Vue.set(this.showDeleteDialog, id, true)
  // }
  //
  // hideDeleteDialogFor (id: string) {
  //   Vue.set(this.showDeleteDialog, id, false)
  // }
}
</script>
