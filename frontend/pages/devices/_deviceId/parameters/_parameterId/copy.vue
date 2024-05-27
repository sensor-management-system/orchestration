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
          save-btn-text="Copy"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Copy & Set Value
        </v-btn>
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
          save-btn-text="Copy"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Copy & Set Value
        </v-btn>
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
  LoadDeviceParametersAction,
  AddDeviceParameterAction, SetChosenKindOfDeviceActionAction, SetDevicePresetParameterAction
} from '@/store/devices'
import { VocabularyState } from '@/store/vocabulary'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import ParameterForm from '@/components/shared/ParameterForm.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { deviceParameterChangeActionOption } from '@/models/ActionKind'

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
    ...mapActions('devices', ['addDeviceParameter', 'loadDeviceParameters', 'loadDeviceParameter', 'setChosenKindOfDeviceAction', 'setDevicePresetParameter']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class ParametersCopyPage extends mixins(CheckEditAccess) {
  private valueCopy: Parameter = new Parameter()

  // vuex definition for typescript check
  deviceParameter!: DevicesState['deviceParameter']
  deviceParametersSortedAlphabetically!: DevicesState['deviceParameters']
  loadDeviceParameter!: LoadDeviceParameterAction
  loadDeviceParameters!: LoadDeviceParametersAction
  addDeviceParameter!: AddDeviceParameterAction
  units!: VocabularyState['units']
  setLoading!: SetLoadingAction
  setChosenKindOfDeviceAction!: SetChosenKindOfDeviceActionAction
  setDevicePresetParameter!: SetDevicePresetParameterAction

  mounted () {
    (this.$refs.parameterForm as ParameterForm).focus()
  }

  async fetch () {
    try {
      await this.loadDeviceParameter(this.parameterId)
      // units are already loaded in the parent page
      if (this.deviceParameter) {
        this.valueCopy = Parameter.createFromObject(this.deviceParameter)
        this.valueCopy.id = null
        this.valueCopy.label = 'Copy of ' + this.valueCopy.label
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

  private async _save (callback: (newParameter: Parameter) => void | (() => void)) {
    if (!(this.$refs.parameterForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const newParameter = await this.addDeviceParameter({
        deviceId: this.deviceId,
        parameter: this.valueCopy
      })

      this.$store.commit('snackbar/setSuccess', 'Copy of parameter has been saved')

      callback(newParameter)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save parameter')
    } finally {
      this.setLoading(false)
    }
  }

  save () {
    this._save(() => {
      this.loadDeviceParameters(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/parameters')
    })
  }

  saveAndRedirectToAddValue () {
    this._save(
      (newParameter: Parameter) => {
        this.setDevicePresetParameter(newParameter)
        this.setChosenKindOfDeviceAction(deviceParameterChangeActionOption)
        this.$router.push('/devices/' + this.deviceId + '/actions/new/parameter-change-actions')
      }
    )
  }
}
</script>
