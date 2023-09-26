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
    <v-select
      value="Parameter Value Change"
      :items="['Parameter Value Change']"
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

    <ParameterChangeActionForm
      ref="deviceParameterChangeActionForm"
      v-model="action"
      :parameters="deviceParameters"
      :current-user-mail="$auth.user.email"
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
  LoadDeviceParameterChangeActionAction,
  LoadAllDeviceActionsAction,
  LoadDeviceParametersAction,
  UpdateDeviceParameterChangeActionAction,
  DevicesState
} from '@/store/devices'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import ParameterChangeActionForm from '@/components/actions/ParameterChangeActionForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    ParameterChangeActionForm,
    SaveAndCancelButtons
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed: mapState('devices', ['deviceParameterChangeAction', 'deviceParameters']),
  methods: {
    ...mapActions('devices', ['loadDeviceParameterChangeAction', 'loadAllDeviceActions', 'loadDeviceParameters', 'updateDeviceParameterChangeAction']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceParameterChangeActionEditPage extends mixins(CheckEditAccess) {
  private action: ParameterChangeAction = new ParameterChangeAction()

  // vuex definition for typescript check
  deviceParameterChangeAction!: DevicesState['deviceParameterChangeAction']
  deviceParameters!: DevicesState['deviceParameters']
  loadDeviceParameterChangeAction!: LoadDeviceParameterChangeActionAction
  loadDeviceParameters!: LoadDeviceParametersAction
  updateDeviceParameterChangeAction!: UpdateDeviceParameterChangeActionAction
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

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDeviceParameterChangeAction(this.actionId),
        this.loadDeviceParameters(this.deviceId)
      ])
      if (this.deviceParameterChangeAction) {
        this.action = ParameterChangeAction.createFromObject(this.deviceParameterChangeAction)
      }
    } catch {
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
    if (!(this.$refs.deviceParameterChangeActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    if (!this.action.parameter || this.action.parameter.id === null) {
      this.$store.commit('snackbar/setError', 'Please select a parameter')
      return
    }

    try {
      this.setLoading(true)
      await this.updateDeviceParameterChangeAction({
        parameterId: this.action.parameter.id,
        action: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
