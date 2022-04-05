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
      <!-- New static location view -->
      <v-card-title>Begin of the static location</v-card-title>
      <v-card-text>
        <ConfigurationStaticLocationBeginActionDataForm
          ref="newStaticLocationForm"
          v-model="beginAction"
          :epsg-codes="epsgCodes"
          :elevation-data="elevationData"
          :contacts="contacts"
          :current-user-mail="currentUserMail"
          :earliest-date-exclusive="latestActiveActionEndDate"
          :latest-date-exclusive="nextActiveLocationBeginDate"
        />
      </v-card-text>
      <v-card-actions v-if="$auth.loggedIn">
        <v-spacer />
        <v-btn small @click="closeNewStaticLocationForm">
          Cancel
        </v-btn>
        <v-btn color="green" small @click="saveNewStaticLocation">
          Add
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
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'

import {
  getCurrentlyActiveLocationAction,
  getLatestActiveActionEndDate,
  getNextActiveLocationBeginDate
} from '@/utils/locationHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationStaticLocationBeginActionDataForm from '@/components/configurations/ConfigurationStaticLocationBeginActionDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ConfigurationStaticLocationBeginActionDataForm,
    DateTimePicker,
    ProgressIndicator
  },
  middleware: ['auth']
})
export default class StaticLocationBeginActionNew extends mixins(Rules) {
  private configuration: Configuration = new Configuration()
  private beginAction: StaticLocationBeginAction = new StaticLocationBeginAction()
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
      this.configuration = Configuration.createFromObject(this.value)
    }
    this.beginAction.beginDate = this.selectedDate
  }

  get selectedDate (): DateTime {
    if ('date' in this.$route.query && this.$route.query.date) {
      return DateTime.fromISO(this.$route.query.date as string).toUTC()
    }
    return DateTime.utc()
  }

  get currentlyActiveLocationAction (): StaticLocationBeginAction | DynamicLocationBeginAction | null {
    return getCurrentlyActiveLocationAction(this.configuration, this.selectedDate)
  }

  get nextActiveLocationBeginDate (): DateTime | null {
    // The nearest begin date AFTER the current one
    const checkDate = this.currentlyActiveLocationAction?.beginDate || this.selectedDate
    return getNextActiveLocationBeginDate(this.configuration, checkDate)
  }

  get latestActiveActionEndDate (): DateTime | null {
    // The end date of the latest (freshed) end action BEFORE
    // the current selected date (currently active action can be null
    // if we are going to insert a location action)
    const checkDate = this.currentlyActiveLocationAction?.beginDate || this.selectedDate
    return getLatestActiveActionEndDate(this.configuration, checkDate)
  }

  closeNewStaticLocationForm (): void {
    this.$router.push('/configurations/' + this.value.id + '/locations/' + this.selectedDate.toISO())
  }

  async saveNewStaticLocation () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.newStaticLocationForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    const configurationBeforeSave = this.$store.state.configurations.configuration
    try {
      // I have to save it the same way as the mount and unmount actions as it
      // is always possible that someone goes into the past and makes an earlier
      // begin or end of the location.
      this.configuration.staticLocationBeginActions.push(this.beginAction)
      this.$store.commit('configurations/setConfiguration', this.configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.isSaving = false
      this.closeNewStaticLocationForm()
    } catch (e) {
      this.$store.commit('configurations/setConfiguration', configurationBeforeSave)
      this.$store.commit('snackbar/setError', 'Save failed')
      this.isSaving = false
    }
  }

  get currentUserMail (): string | null {
    return this.$auth.user?.email as string | null
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChange (val: Configuration): void {
    this.configuration = Configuration.createFromObject(val)
  }
}
</script>
