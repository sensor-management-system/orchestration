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
          :to="'/devices/' + deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <CustomFieldForm
          ref="customFieldCardForm"
          v-model="valueCopy"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Apply"
          :to="'/devices/' + deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <template
      v-if="deviceCustomFieldsExceptCurrent.length"
    >
      <v-subheader>Existing custom fields</v-subheader>
      <BaseList
        v-if="valueCopy !== null"
        :list-items="deviceCustomFieldsExceptCurrent"
      >
        <template #list-item="{item}">
          <CustomFieldListItem
            :value="item"
            :editable="false"
          />
        </template>
      </BaseList>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  DevicesState,
  LoadDeviceCustomFieldAction,
  LoadDeviceCustomFieldsAction,
  UpdateDeviceCustomFieldAction
} from '@/store/devices'

import { CustomTextField } from '@/models/CustomTextField'

import BaseList from '@/components/shared/BaseList.vue'
import CustomFieldForm from '@/components/shared/CustomFieldForm.vue'
import CustomFieldListItem from '@/components/shared/CustomFieldListItem.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    BaseList,
    CustomFieldForm,
    CustomFieldListItem,
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  computed: {
    ...mapState('devices', ['deviceCustomField', 'deviceCustomFields']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceCustomField', 'loadDeviceCustomFields', 'updateDeviceCustomField']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceCustomFieldsEditPage extends mixins(CheckEditAccess) {
  private valueCopy: CustomTextField = new CustomTextField()

  // vuex definition for typescript check
  deviceCustomField!: DevicesState['deviceCustomField']
  deviceCustomFields!: DevicesState['deviceCustomFields']
  loadDeviceCustomField!: LoadDeviceCustomFieldAction
  updateDeviceCustomField!: UpdateDeviceCustomFieldAction
  loadDeviceCustomFields!: LoadDeviceCustomFieldsAction
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
    return '/devices/' + this.deviceId + '/customfields'
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
      await this.loadDeviceCustomField(this.customFieldId)
      if (this.deviceCustomField) {
        this.valueCopy = CustomTextField.createFromObject(this.deviceCustomField)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load custom field')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get customFieldId (): string {
    return this.$route.params.customfieldId
  }

  get deviceCustomFieldsExceptCurrent (): CustomTextField[] {
    return this.deviceCustomFields.filter(i => i.id !== this.customFieldId)
  }

  async save () {
    try {
      this.setLoading(true)
      await this.updateDeviceCustomField({
        deviceId: this.deviceId,
        deviceCustomField: this.valueCopy
      })
      this.loadDeviceCustomFields(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Custom field updated')
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
