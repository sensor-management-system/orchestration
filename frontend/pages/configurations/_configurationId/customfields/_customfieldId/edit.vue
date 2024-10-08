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
          :to="'/configurations/' + configurationId + '/customfields'"
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
          :to="'/configurations/' + configurationId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <template
      v-if="configurationCustomFieldsExceptCurrent.length"
    >
      <v-subheader>Existing custom fields</v-subheader>
      <BaseList
        v-if="valueCopy !== null"
        :list-items="configurationCustomFieldsExceptCurrent"
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
  ConfigurationsState,
  LoadConfigurationCustomFieldAction,
  LoadConfigurationCustomFieldsAction,
  UpdateConfigurationCustomFieldAction
} from '@/store/configurations'

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
    ...mapState('configurations', ['configurationCustomField', 'configurationCustomFields']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfigurationCustomField', 'loadConfigurationCustomFields', 'updateConfigurationCustomField']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationCustomFieldsEditPage extends mixins(CheckEditAccess) {
  private valueCopy: CustomTextField = new CustomTextField()

  // vuex definition for typescript check
  configurationCustomField!: ConfigurationsState['configurationCustomField']
  configurationCustomFields!: ConfigurationsState['configurationCustomFields']
  loadConfigurationCustomField!: LoadConfigurationCustomFieldAction
  updateConfigurationCustomField!: UpdateConfigurationCustomFieldAction
  loadConfigurationCustomFields!: LoadConfigurationCustomFieldsAction
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
    return '/configurations/' + this.configurationId + '/customfields'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadConfigurationCustomField(this.customFieldId)
      if (this.configurationCustomField) {
        this.valueCopy = CustomTextField.createFromObject(this.configurationCustomField)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load custom field')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get customFieldId (): string {
    return this.$route.params.customfieldId
  }

  get configurationCustomFieldsExceptCurrent (): CustomTextField[] {
    return this.configurationCustomFields.filter(i => i.id !== this.customFieldId)
  }

  async save () {
    try {
      this.setLoading(true)
      await this.updateConfigurationCustomField({
        configurationId: this.configurationId,
        configurationCustomField: this.valueCopy
      })
      this.loadConfigurationCustomFields(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Custom field updated')
      this.$router.push('/configurations/' + this.configurationId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
