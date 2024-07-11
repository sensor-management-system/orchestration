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
          :to="'/configurations/' + configurationId + '/parameters'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <parameter-form
          ref="parameterForm"
          v-model="valueCopy"
          :units="units"
          auto-completion-endpoint="configuration-parameter-labels"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Apply"
          :to="'/configurations/' + configurationId + '/parameters'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <v-subheader
      v-if="configurationParametersSortedAlphabetically.length > 1"
    >
      Existing parameters
    </v-subheader>
    <BaseList
      :list-items="configurationParametersSortedAlphabetically"
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
  ConfigurationsState,
  LoadConfigurationParameterAction,
  LoadConfigurationParameterChangeActionsAction,
  LoadConfigurationParametersAction,
  UpdateConfigurationParameterAction
} from '@/store/configurations'
import { VocabularyState } from '@/store/vocabulary'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import ParameterForm from '@/components/shared/ParameterForm.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { SetLoadingAction } from '@/store/progressindicator'

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
    ...mapState('configurations', ['configurationParameter']),
    ...mapGetters('configurations', ['configurationParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('configurations', ['updateConfigurationParameter', 'loadConfigurationParameters', 'loadConfigurationParameter', 'loadConfigurationParameterChangeActions']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class ParametersEditPage extends mixins(CheckEditAccess) {
  private valueCopy: Parameter = new Parameter()

  // vuex definition for typescript check
  configurationParameter!: ConfigurationsState['configurationParameter']
  configurationParametersSortedAlphabetically!: ConfigurationsState['configurationParameters']
  loadConfigurationParameter!: LoadConfigurationParameterAction
  loadConfigurationParameters!: LoadConfigurationParametersAction
  loadConfigurationParameterChangeActions!: LoadConfigurationParameterChangeActionsAction
  updateConfigurationParameter!: UpdateConfigurationParameterAction
  units!: VocabularyState['units']
  setLoading!: SetLoadingAction

  mounted () {
    (this.$refs.parameterForm as ParameterForm).focus()
  }

  async fetch () {
    try {
      await this.loadConfigurationParameter(this.parameterId)
      // units are already loaded in the parent page
      if (this.configurationParameter) {
        this.valueCopy = Parameter.createFromObject(this.configurationParameter)
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
    return '/configurations/' + this.configurationId + '/parameters'
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

  get configurationId (): string {
    return this.$route.params.configurationId
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
      await this.updateConfigurationParameter({
        configurationId: this.configurationId,
        parameter: this.valueCopy
      })
      this.loadConfigurationParameters(this.configurationId)
      this.loadConfigurationParameterChangeActions(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Parameter successfully updated')
      this.$router.push('/configurations/' + this.configurationId + '/parameters')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save parameter')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>
