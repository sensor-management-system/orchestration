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
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="softwareUpdateAction"
      :attachments="deviceAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Create"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import {
  AddDeviceSoftwareUpdateAction,
  LoadAllDeviceActionsAction,
  DevicesState
} from '@/store/devices'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  middleware: ['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons, SoftwareUpdateActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: mapActions('devices', ['addDeviceSoftwareUpdateAction', 'loadAllDeviceActions'])
})
export default class NewDeviceSoftwareUpdateActions extends Vue {
  @InjectReactive()
    editable!: boolean

  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()
  private isSaving: boolean = false

  // vuex definition for typescript check
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  deviceAttachments!: DevicesState['deviceAttachments']
  addDeviceSoftwareUpdateAction!: AddDeviceSoftwareUpdateAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction

  created () {
    if (!this.editable) {
      this.$router.replace('/devices/' + this.deviceId + '/actions', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this device.')
      })
    }
    if (this.chosenKindOfDeviceAction === null) {
      this.$router.push('/devices/' + this.deviceId + '/actions')
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save () {
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.addDeviceSoftwareUpdateAction({
        deviceId: this.deviceId,
        softwareUpdateAction: this.softwareUpdateAction
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New Software Update Action added')
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
