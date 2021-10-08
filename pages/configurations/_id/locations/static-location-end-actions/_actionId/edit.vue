<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
      v-model="isSaving"
      dark
    />
    <v-card>
      <!-- 1) Ready-only static location view -->
      <template
        v-if="beginAction"
      >
        <v-card-title>
          Begin of the static location
        </v-card-title>
        <v-card-text class="text--primary">
          <ConfigurationStaticLocationBeginActionData
            v-model="beginAction"
            :epsg-codes="epsgCodes"
            :elevation-data="elevationData"
          />
        </v-card-text>
        <v-divider class="mx-4 mt-4" />
      </template>
      <v-card-title
        id="static-location-end"
      >
        End of the static location
      </v-card-title>
      <v-card-text>
        <ConfigurationStaticLocationEndActionDataForm
          ref="editStaticLocationEndForm"
          v-model="endAction"
          :contacts="contacts"
          :current-user-mail="currentUserMail"
          :earliest-date-exclusive="beginAction ? beginAction.beginDate : null"
          :latest-date-exclusive="nextActiveLocationBeginDate"
        />
      </v-card-text>
      <v-card-actions v-if="$auth.loggedIn">
        <v-spacer />
        <v-btn small @click="closeEditStaticLocationEndForm">
          Cancel
        </v-btn>
        <v-btn color="green" small @click="saveEditedStopStaticLocation">
          Apply
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch, mixins } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Configuration } from '@/models/Configuration'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

import {
  getNextActiveLocationBeginDate,
  getBeginActionForLocationEndAction
} from '@/utils/locationHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationStaticLocationBeginActionData from '@/components/configurations/ConfigurationStaticLocationBeginActionData.vue'
import ConfigurationStaticLocationEndActionDataForm from '@/components/configurations/ConfigurationStaticLocationEndActionDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ConfigurationStaticLocationBeginActionData,
    ConfigurationStaticLocationEndActionDataForm,
    DateTimePicker,
    ProgressIndicator
  }
})
export default class StaticLocationEndActionEdit extends mixins(Rules) {
  private configuration: Configuration = new Configuration()
  private beginAction: StaticLocationBeginAction | null = null
  private endAction: StaticLocationEndAction = new StaticLocationEndAction()
  private endDate: DateTime | null = null
  private isSaving: boolean = false

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly elevationData!: ElevationDatum[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly epsgCodes!: EpsgCode[]

  created () {
    if (this.value) {
      this.initializeConfigurationAndAction(this.value)
    }
  }

  mounted () {
    this.scrollToEditForm()
  }

  activated () {
    this.scrollToEditForm()
  }

  initializeConfigurationAndAction (configuration: Configuration) {
    this.configuration = Configuration.createFromObject(configuration)
    const endAction = this.configuration.staticLocationEndActions.find(action => action.id === this.actionId)
    if (endAction) {
      // as we already created a deep copy of the configuration, we don't need to create a copy of the endAction
      this.endAction = endAction
      // we also create a reference to the end date of the end action
      this.endDate = endAction.endDate

      const beginAction = getBeginActionForLocationEndAction(this.configuration, this.endAction)
      if (beginAction instanceof StaticLocationBeginAction) {
        this.beginAction = beginAction
      }
    }
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get nextActiveLocationBeginDate (): DateTime | null {
    // The nearest begin date AFTER the current one
    if (!this.endDate) {
      return null
    }
    return getNextActiveLocationBeginDate(this.configuration, this.endDate)
  }

  closeEditStaticLocationEndForm (): void {
    this.$router.push('/configurations/' + this.value.id + '/locations/' + (this.endDate ? this.endDate.toISO() : ''))
  }

  async saveEditedStopStaticLocation () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.editStaticLocationEndForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    try {
      this.configuration.staticLocationEndActions = this.configuration.staticLocationEndActions.filter(x => x.id !== this.endAction.id)
      this.configuration.staticLocationEndActions.push(this.endAction)
      this.$store.commit('configurations/setConfiguration', this.configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.isSaving = false
      this.closeEditStaticLocationEndForm()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
      this.isSaving = false
    }
  }

  get currentUserMail (): string | null {
    return this.$auth.user?.email as string | null
  }

  scrollToEditForm (): void {
    Vue.nextTick(() => this.$vuetify.goTo('#static-location-end'))
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChange (val: Configuration): void {
    this.initializeConfigurationAndAction(val)
    this.scrollToEditForm()
  }
}
</script>
