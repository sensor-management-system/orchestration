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
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/devices/' + deviceId + '/customfields/new'"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceCustomFields.length === 0">
      There are no custom fields for this device.
    </hint-card>
    <BaseList
      :list-items="deviceCustomFields"
    >
      <template #list-item="{item}">
        <DevicesCustomFieldListItem
          :custom-field="item"
          :device-id="deviceId"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialog(item)"
            />
          </template>
        </DevicesCustomFieldListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceCustomFields.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/customfields/new'"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <DevicesCustomFieldDeleteDialog
      v-model="showDeleteDialog"
      :custom-field-to-delete="customFieldToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import { CustomTextField } from '@/models/CustomTextField'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesCustomFieldListItem from '@/components/devices/DevicesCustomFieldListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DevicesCustomFieldDeleteDialog from '@/components/devices/DevicesCustomFieldDeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, HintCard, DevicesCustomFieldDeleteDialog, DotMenuActionDelete, DevicesCustomFieldListItem, BaseList },
  computed: mapState('devices', ['deviceCustomFields']),
  methods: mapActions('devices', ['deleteDeviceCustomField', 'loadDeviceCustomFields'])
})
export default class DeviceCustomFieldsShowPage extends Vue {
  private isSaving = false
  private showDeleteDialog = false
  private customFieldToDelete: CustomTextField|null = null

  // vuex definition for typescript check
  loadDeviceCustomFields!:(id: string)=>void
  deleteDeviceCustomField!:(customField: string)=>Promise<void>


  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initDeleteDialog (customField: CustomTextField) {
    this.showDeleteDialog = true
    this.customFieldToDelete = customField
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.customFieldToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.customFieldToDelete === null || this.customFieldToDelete.id === null) {
      return
    }
    try {
      this.isSaving = true
      await this.deleteDeviceCustomField(this.customFieldToDelete.id)
      this.loadDeviceCustomFields(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Custom field deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete custom field')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }
}
</script>
