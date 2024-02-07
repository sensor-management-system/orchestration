<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="configurationActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        >
          <template #append-outer>
            <v-btn icon @click="showNewActionTypeDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
        </v-select>
      </v-card-text>
    </v-card>
    <v-card-actions v-if="!chosenKindOfAction">
      <v-spacer />
      <v-btn
        small
        text
        nuxt
        :to="'/configurations/' + configurationId + '/actions'"
      >
        cancel
      </v-btn>
    </v-card-actions>
    <NuxtChild />
    <action-type-dialog
      v-model="showNewActionTypeDialog"
      :initial-action-type-api-filter-type="selectedActionCategory"
      @aftersubmit="setChosenKindOfConfigurationActionAndUpdateRoute"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import ActionTypeDialog from '@/components/shared/ActionTypeDialog.vue'
import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ActionType } from '@/models/ActionType'

import {
  ConfigurationActionTypeItemsGetter,
  LoadConfigurationGenericActionTypesAction
} from '@/store/vocabulary'
import {
  ConfigurationsState,
  LoadConfigurationAttachmentsAction, LoadConfigurationParametersAction,
  SetChosenKindOfConfigurationActionAction, SetConfigurationPresetParameterAction
} from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'
import { ACTION_TYPE_API_FILTER_CONFIGURATION } from '@/services/cv/ActionTypeApi'
import { KIND_OF_ACTION_TYPE_GENERIC_ACTION, KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION } from '@/models/ActionKind'

@Component({
  components: { ActionTypeDialog },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['configurationActionTypeItems']),
    ...mapState('configurations', ['chosenKindOfConfigurationAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadConfigurationGenericActionTypes']),
    ...mapActions('configurations', ['setChosenKindOfConfigurationAction', 'loadConfigurationAttachments', 'loadConfigurationParameters', 'setConfigurationPresetParameter']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ActionAddPage extends mixins(CheckEditAccess) {
  private showNewActionTypeDialog = false

  // vuex definition for typescript check
  configurationActionTypeItems!: ConfigurationActionTypeItemsGetter
  chosenKindOfConfigurationAction!: ConfigurationsState['chosenKindOfConfigurationAction']

  loadConfigurationGenericActionTypes!: LoadConfigurationGenericActionTypesAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  loadConfigurationParameters!: LoadConfigurationParametersAction
  setChosenKindOfConfigurationAction!: SetChosenKindOfConfigurationActionAction
  setLoading!: SetLoadingAction
  setConfigurationPresetParameter!: SetConfigurationPresetParameterAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/actions'
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

  get selectedActionCategory (): string {
    return ACTION_TYPE_API_FILTER_CONFIGURATION
  }

  get isBasePath (): boolean {
    return this.$route.path === '/configurations/' + this.configurationId + '/actions/new'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      if (this.isBasePath) {
        this.chosenKindOfAction = null
        this.setConfigurationPresetParameter(null)
      }
      await Promise.all([
        this.loadConfigurationGenericActionTypes(),
        this.loadConfigurationAttachments(this.configurationId),
        this.loadConfigurationParameters(this.configurationId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get chosenKindOfAction () {
    return this.chosenKindOfConfigurationAction
  }

  set chosenKindOfAction (newVal) {
    this.setChosenKindOfConfigurationAction(newVal)
  }

  setChosenKindOfConfigurationActionAndUpdateRoute (newVal: ActionType) {
    this.setChosenKindOfConfigurationAction({
      kind: KIND_OF_ACTION_TYPE_GENERIC_ACTION,
      id: newVal.id,
      name: newVal.name,
      uri: newVal.uri
    })
    this.updateRoute()
  }

  get genericActionChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION
  }

  get parameterChangeActionChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
  }

  updateRoute () {
    if (this.genericActionChosen) {
      this.$router.push(`/configurations/${this.configurationId}/actions/new/generic-configuration-actions`)
      return
    }
    if (this.parameterChangeActionChosen) {
      this.$router.push(`/configurations/${this.configurationId}/actions/new/parameter-change-actions`)
      return
    }
    if (!this.chosenKindOfAction) {
      this.$router.push(`/configurations/${this.configurationId}/actions/new`)
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/configurations/' + this.configurationId + '/actions', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }
}
</script>
