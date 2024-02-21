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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Add & Set Value
        </v-btn>
      </v-card-actions>
      <v-card-text>
        <parameter-form
          ref="parameterForm"
          v-model="value"
          :units="units"
          auto-completion-endpoint="device-parameter-labels"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + deviceId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Add & Set Value
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-subheader
      v-if="deviceParametersSortedAlphabetically.length > 0"
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
          :parameter-change-actions="deviceParameterChangeActions"
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
  AddDeviceParameterAction,
  DevicesState,
  LoadDeviceParametersAction, SetChosenKindOfDeviceActionAction, SetDevicePresetParameterAction
} from '@/store/devices'
import { VocabularyState } from '@/store/vocabulary'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import ParameterForm from '@/components/shared/ParameterForm.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'
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
    ...mapState('devices', ['deviceParameterChangeActions']),
    ...mapGetters('devices', ['deviceParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('devices', ['addDeviceParameter', 'loadDeviceParameters', 'setChosenKindOfDeviceAction', 'setDevicePresetParameter']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class ParametersAddPage extends mixins(CheckEditAccess) {
  private value: Parameter = new Parameter()

  // vuex definition for typescript check
  units!: VocabularyState['units']
  deviceParametersSortedAlphabetically!: DevicesState['deviceParameters']
  deviceParameterChangeActions!: DevicesState['deviceParameterChangeActions']
  addDeviceParameter!: AddDeviceParameterAction
  loadDeviceParameters!: LoadDeviceParametersAction
  setLoading!: SetLoadingAction
  setChosenKindOfDeviceAction!: SetChosenKindOfDeviceActionAction
  setDevicePresetParameter!: SetDevicePresetParameterAction

  mounted () {
    (this.$refs.parameterForm as ParameterForm).focus()
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

  private async _save (callback: (newParameter: Parameter) => void | (() => void)) {
    if (!(this.$refs.parameterForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const newParameter = await this.addDeviceParameter({
        deviceId: this.deviceId,
        parameter: this.value
      })

      this.$store.commit('snackbar/setSuccess', 'New parameter has been added')

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
