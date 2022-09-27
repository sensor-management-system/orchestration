<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="configurationActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        />
      </v-card-text>
    </v-card>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ConfigurationActionTypeItemsGetter, LoadConfigurationGenericActionTypesAction } from '@/store/vocabulary'
import {
  ConfigurationsState,
  SetChosenKindOfConfigurationActionAction,
  LoadConfigurationAttachmentsAction
} from '@/store/configurations'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['configurationActionTypeItems']),
    ...mapState('configurations', ['chosenKindOfConfigurationAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadConfigurationGenericActionTypes']),
    ...mapActions('configurations', ['setChosenKindOfConfigurationAction', 'loadConfigurationAttachments'])
  }
})
export default class ActionAddPage extends mixins(CheckEditAccess) {
  private isLoading: boolean = false

  // vuex definition for typescript check
  configurationActionTypeItems!: ConfigurationActionTypeItemsGetter
  chosenKindOfConfigurationAction!: ConfigurationsState['chosenKindOfConfigurationAction']

  loadConfigurationGenericActionTypes!: LoadConfigurationGenericActionTypesAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  setChosenKindOfConfigurationAction!: SetChosenKindOfConfigurationActionAction

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

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      this.chosenKindOfAction = null
      await Promise.all([
        this.loadConfigurationGenericActionTypes(),
        this.loadConfigurationAttachments(this.configurationId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    } finally {
      this.isLoading = false
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

  updateRoute () {
    this.$router.push(`/configurations/${this.configurationId}/actions/new/generic-configuration-actions`)
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
