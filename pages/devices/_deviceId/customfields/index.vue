<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <v-card-actions
      v-if="editable"
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
        <CustomFieldListItem
          :value="item"
          :editable="editable"
          :to="'/devices/' + deviceId + '/customfields/' + item.id + '/edit'"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!editable"
              @click="initDeleteDialog(item)"
            />
          </template>
        </CustomFieldListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceCustomFields.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/customfields/new'"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <DeleteDialog
      v-if="customFieldToDelete"
      v-model="showDeleteDialog"
      title="Delete Custom Field"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the field &quot;<em>{{ customFieldToDelete.key | shortenRight }}</em>&quot;?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DeleteDeviceCustomFieldAction, DevicesState, LoadDeviceCustomFieldsAction } from '@/store/devices'

import { CustomTextField } from '@/models/CustomTextField'

import BaseList from '@/components/shared/BaseList.vue'
import CustomFieldListItem from '@/components/shared/CustomFieldListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  components: { HintCard, DeleteDialog, DotMenuActionDelete, CustomFieldListItem, BaseList },
  computed: {
    ...mapState('devices', ['deviceCustomFields']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['deleteDeviceCustomField', 'loadDeviceCustomFields']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private customFieldToDelete: CustomTextField | null = null

  // vuex definition for typescript check
  deviceCustomFields!: DevicesState['deviceCustomFields']
  loadDeviceCustomFields!: LoadDeviceCustomFieldsAction
  deleteDeviceCustomField!: DeleteDeviceCustomFieldAction
  setLoading!: SetLoadingAction

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
      this.setLoading(true)
      await this.deleteDeviceCustomField(this.customFieldToDelete.id)
      this.loadDeviceCustomFields(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Custom field deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete custom field')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }
}
</script>
