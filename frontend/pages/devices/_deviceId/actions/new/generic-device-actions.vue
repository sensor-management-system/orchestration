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
    <GenericActionForm
      ref="genericDeviceActionForm"
      v-model="genericDeviceAction"
      :attachments="deviceAttachments"
      :current-user-contact-id="userInfo.contactId"
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
  AddDeviceGenericAction,
  LoadAllDeviceActionsAction,
  DevicesState
} from '@/store/devices'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  middleware: ['auth'],
  components: { SaveAndCancelButtons, GenericActionForm },
  computed: {
    ...mapState('devices', ['deviceAttachments', 'chosenKindOfDeviceAction']),
    ...mapState('permissions', ['userInfo'])
  },
  methods: {
    ...mapActions('devices', ['addDeviceGenericAction', 'loadAllDeviceActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewGenericDeviceAction extends mixins(CheckEditAccess) {
  private genericDeviceAction: GenericAction = new GenericAction()

  // vuex definition for typescript check
  deviceAttachments!: DevicesState['deviceAttachments']
  chosenKindOfDeviceAction!: DevicesState['chosenKindOfDeviceAction']
  addDeviceGenericAction!: AddDeviceGenericAction
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
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericDeviceAction.actionTypeName = this.chosenKindOfDeviceAction?.name || ''
    this.genericDeviceAction.actionTypeUrl = this.chosenKindOfDeviceAction?.uri || ''

    try {
      this.setLoading(true)
      await this.addDeviceGenericAction({
        deviceId: this.deviceId,
        genericAction: this.genericDeviceAction
      })
      this.loadAllDeviceActions(this.deviceId)
      const successMessage = this.genericDeviceAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
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
