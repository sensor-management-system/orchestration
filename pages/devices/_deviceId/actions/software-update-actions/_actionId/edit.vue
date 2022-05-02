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
    <v-select
      value="Software Update"
      :items="['Software Update']"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="action"
      :attachments="deviceAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
@Component({
  components: {
    ProgressIndicator,
    SaveAndCancelButtons,
    SoftwareUpdateActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('devices', ['deviceSoftwareUpdateAction', 'deviceAttachments']),
  methods: mapActions('devices', ['loadDeviceSoftwareUpdateAction', 'loadAllDeviceActions', 'loadDeviceAttachments', 'updateDeviceSoftwareUpdateAction'])
})
export default class DeviceSoftwareUpdateActionEditPage extends Vue {
  private action: SoftwareUpdateAction = new SoftwareUpdateAction()
  private isSaving = false
  private isLoading = false

  async created () {
    try {
      this.isLoading = true
      await this.loadDeviceSoftwareUpdateAction(this.actionId)
      await this.loadDeviceAttachments(this.deviceId)
      this.action = SoftwareUpdateAction.createFromObject(this.deviceSoftwareUpdateAction)
    } catch {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.isLoading = false
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save (): void {
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.updateDeviceSoftwareUpdateAction({
        deviceId: this.deviceId,
        softwareUpdateAction: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Software Update Action updated')
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
