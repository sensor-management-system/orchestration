<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddDeviceSoftwareUpdateAction,
  LoadAllDeviceActionsAction,
  DevicesState
} from '@/store/devices'

import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  middleware: ['auth'],
  components: { SaveAndCancelButtons, SoftwareUpdateActionForm },
  computed: mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
  methods: {
    ...mapActions('devices', ['addDeviceSoftwareUpdateAction', 'loadAllDeviceActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewDeviceSoftwareUpdateActions extends mixins(CheckEditAccess) {
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()

  // vuex definition for typescript check
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  deviceAttachments!: DevicesState['deviceAttachments']
  addDeviceSoftwareUpdateAction!: AddDeviceSoftwareUpdateAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
  setLoading!: SetLoadingAction
  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/actions'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this device.'
  }

  created () {
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
      this.setLoading(true)
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
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
