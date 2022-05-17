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
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/devices/' + deviceId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceAttachments.length === 0">
      There are no attachments for this device.
    </hint-card>

    <BaseList
      :list-items="deviceAttachments"
    >
      <template #list-item="{item}">
        <DevicesAttachmentListItem
          :attachment="item"
          :device-id="deviceId"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialog(item)"
            />
          </template>
        </DevicesAttachmentListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <DevicesAttachmentDeleteDialog
      v-model="showDeleteDialog"
      :attachment-to-delete="attachmentToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Attachment } from '@/models/Attachment'

import BaseList from '@/components/shared/BaseList.vue'
import DevicesAttachmentListItem from '@/components/devices/DevicesAttachmentListItem.vue'
import DevicesAttachmentDeleteDialog from '@/components/devices/DevicesAttachmentDeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, DotMenuActionDelete, HintCard, DevicesAttachmentDeleteDialog, DevicesAttachmentListItem, BaseList },
  computed: mapState('devices', ['deviceAttachments']),
  methods: mapActions('devices', ['loadDeviceAttachments', 'deleteDeviceAttachment'])
})
export default class DeviceAttachmentShowPage extends Vue {
  private isSaving = false
  private showDeleteDialog = false
  private attachmentToDelete: Attachment|null = null

  // vuex definition for typescript check
  deleteDeviceAttachment!: (attachmentId: string) => Promise<void>
  loadDeviceAttachments!: (id: string) => void

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initDeleteDialog (attachment: Attachment) {
    this.showDeleteDialog = true
    this.attachmentToDelete = attachment
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.attachmentToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      this.isSaving = true
      await this.deleteDeviceAttachment(this.attachmentToDelete.id)
      this.loadDeviceAttachments(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.isSaving = false
      this.closeDialog()
    }
  }
}
</script>

<style scoped>

</style>
