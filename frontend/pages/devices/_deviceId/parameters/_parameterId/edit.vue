<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Apply"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <parameter-form
          ref="parameterForm"
          v-model="valueCopy"
          :units="units"
          auto-completion-endpoint="device-parameter-labels"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Apply"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <v-subheader
      v-if="deviceParametersSortedAlphabetically.length > 1"
    >
      Existing parameters
    </v-subheader>
    <BaseList
      :list-items="deviceParametersSortedAlphabetically"
    >
      <template #list-item="{item,index}">
        <ParameterListItem
          v-if="item.id !== valueCopy.id"
          :value="item"
          :index="index"
        />
      </template>
    </BaseList>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  DevicesState,
  LoadDeviceParameterAction,
  LoadDeviceParameterChangeActionsAction,
  LoadDeviceParametersAction,
  UpdateDeviceParameterAction
} from '@/store/devices'
import { VocabularyState } from '@/store/vocabulary'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import ParameterForm from '@/components/shared/ParameterForm.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  middleware: ['auth'],
  components: {
    BaseList,
    ParameterForm,
    ParameterListItem,
    SaveAndCancelButtons
  },
  computed: {
    ...mapState('vocabulary', ['units']),
    ...mapState('devices', ['deviceParameter']),
    ...mapGetters('devices', ['deviceParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('devices', ['updateDeviceParameter', 'loadDeviceParameters', 'loadDeviceParameter', 'loadDeviceParameterChangeActions']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class ParametersEditPage extends mixins(CheckEditAccess) {
  private valueCopy: Parameter = new Parameter()

  // vuex definition for typescript check
  deviceParameter!: DevicesState['deviceParameter']
  deviceParametersSortedAlphabetically!: DevicesState['deviceParameters']
  loadDeviceParameter!: LoadDeviceParameterAction
  loadDeviceParameters!: LoadDeviceParametersAction
  loadDeviceParameterChangeActions!: LoadDeviceParameterChangeActionsAction
  updateDeviceParameter!: UpdateDeviceParameterAction
  units!: VocabularyState['units']
  setLoading!: SetLoadingAction

  mounted () {
    (this.$refs.parameterForm as ParameterForm).focus()
  }

  async fetch () {
    try {
      await this.loadDeviceParameter(this.parameterId)
      // units are already loaded in the parent page
      if (this.deviceParameter) {
        this.valueCopy = Parameter.createFromObject(this.deviceParameter)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load parameter')
    }
  }

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/devices/' + this.deviceId + '/parameters'
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

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get parameterId (): string {
    return this.$route.params.parameterId
  }

  async save () {
    if (!(this.$refs.parameterForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      await this.updateDeviceParameter({
        deviceId: this.deviceId,
        parameter: this.valueCopy
      })
      this.loadDeviceParameters(this.deviceId)
      this.loadDeviceParameterChangeActions(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Parameter successfully updated')
      this.$router.push('/devices/' + this.deviceId + '/parameters')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save parameter')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
