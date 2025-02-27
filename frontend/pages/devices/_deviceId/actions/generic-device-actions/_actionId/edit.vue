<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="action.actionTypeName"
      :items="[action.actionTypeName]"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/devices/' + deviceId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <GenericActionForm
      ref="genericDeviceActionForm"
      v-model="action"
      :attachments="deviceAttachments"
      :current-user-contact-id="userInfo.contactId"
    />

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
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
  LoadDeviceGenericActionAction,
  LoadAllDeviceActionsAction,
  LoadDeviceAttachmentsAction,
  UpdateDeviceGenericAction,
  DevicesState
} from '@/store/devices'

import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    GenericActionForm
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceGenericAction', 'deviceAttachments']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapState('permissions', ['userInfo'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceGenericAction', 'loadAllDeviceActions', 'loadDeviceAttachments', 'updateDeviceGenericAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class GenericDeviceActionEditPage extends mixins(CheckEditAccess) {
  private action: GenericAction = new GenericAction()

  // vuex definition for typescript check
  deviceGenericAction!: DevicesState['deviceGenericAction']
  deviceAttachments!: DevicesState['deviceAttachments']
  loadDeviceGenericAction!: LoadDeviceGenericActionAction
  loadDeviceAttachments!: LoadDeviceAttachmentsAction
  updateDeviceGenericAction!: UpdateDeviceGenericAction
  loadAllDeviceActions!: LoadAllDeviceActionsAction
  isLoading!: LoadingSpinnerState['isLoading']
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

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDeviceGenericAction(this.actionId),
        this.loadDeviceAttachments(this.deviceId)
      ])
      if (this.deviceGenericAction) {
        this.action = GenericAction.createFromObject(this.deviceGenericAction)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  async save () {
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      this.setLoading(true)
      await this.updateDeviceGenericAction({
        deviceId: this.deviceId,
        genericAction: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', `${this.action.actionTypeName} updated`)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
