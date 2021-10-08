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
    <v-card
      v-if="currentlyActiveLocationAction"
    >
      <v-card-title>
        Begin of the static location
      </v-card-title>
      <v-card-text class="text--primary">
        <ConfigurationStaticLocationBeginActionData
          v-model="currentlyActiveLocationAction"
          :epsg-codes="epsgCodes"
          :elevation-data="elevationData"
        />
      </v-card-text>
      <v-divider class="mx-4 mt-4" />
      <v-card-title id="static-location-end">
        End of the static location
      </v-card-title>
      <v-card-text>
        <ConfigurationStaticLocationEndActionDataForm
          ref="stopStaticLocationForm"
          v-model="endAction"
          :contacts="contacts"
          :current-user-mail="currentUserMail"
          :earliest-date-exclusive="currentlyActiveLocationAction.beginDate"
          :latest-date-exclusive="nextActiveLocationBeginDate"
        />
      </v-card-text>
      <v-card-actions v-if="$auth.loggedIn">
        <v-spacer />
        <v-btn small @click="closeFormOnCancel">
          Cancel
        </v-btn>
        <v-btn color="green" small @click="saveStopStaticLocation">
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
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

import {
  getCurrentlyActiveLocationAction,
  getNextActiveLocationBeginDate
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
export default class StaticLocationEndActionNew extends mixins(Rules) {
  private configuration: Configuration = new Configuration()
  private endAction: StaticLocationEndAction = new StaticLocationEndAction()
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
    this.endAction.endDate = this.selectedDate || DateTime.utc()
  }

  mounted () {
    this.scrollToEditForm()
  }

  activated () {
    this.scrollToEditForm()
  }

  get selectedDate (): DateTime | undefined {
    const dateFromUrl = this.dateFromUrlParam()
    if (dateFromUrl) {
      return dateFromUrl
    }
  }

  get currentlyActiveLocationAction () : StaticLocationBeginAction | DynamicLocationBeginAction | null {
    if (!this.selectedDate) {
      return null
    }
    return getCurrentlyActiveLocationAction(this.configuration, this.selectedDate)
  }

  get nextActiveLocationBeginDate (): DateTime | null {
    // The nearest begin date AFTER the current one
    const checkDate = this.currentlyActiveLocationAction?.beginDate || this.selectedDate
    if (!checkDate) {
      return null
    }
    return getNextActiveLocationBeginDate(this.configuration, checkDate)
  }

  closeFormOnCancel (): void {
    this.closeStopStaticLocationForm(this.dateFromUrlParam())
  }

  closeFormOnSave (): void {
    this.closeStopStaticLocationForm(this.endAction.endDate)
  }

  closeStopStaticLocationForm (date?: DateTime | null): void {
    if (!date) {
      date = DateTime.utc()
    }
    this.$router.push('/configurations/' + this.value.id + '/locations/' + date.toISO())
  }

  async saveStopStaticLocation () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.stopStaticLocationForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    try {
      const currentlyActiveBeginDate = this.currentlyActiveLocationAction?.beginDate
      if (currentlyActiveBeginDate && this.endAction.endDate && this.endAction.endDate.equals(currentlyActiveBeginDate)) {
        // in case we have the end date on the very same time as the begin date
        // there was no active location effectifly,
        // there may be some more important things to consider
        // like removing a later end action that was used so far
        this.configuration.staticLocationBeginActions = this.configuration.staticLocationBeginActions.filter(x => x !== this.currentlyActiveLocationAction)
      } else {
        this.configuration.staticLocationEndActions.push(this.endAction)
      }
      this.$store.commit('configurations/setConfiguration', this.configuration)
      await this.$store.dispatch('configurations/saveConfiguration')
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.isSaving = false
      this.closeFormOnSave()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
      this.isSaving = false
    }
  }

  get currentUserMail (): string | null {
    return this.$auth.user?.email as string | null
  }

  dateFromUrlParam (): DateTime | undefined {
    if ('date' in this.$route.query && this.$route.query.date) {
      return DateTime.fromISO(this.$route.query.date as string).toUTC()
    }
  }

  scrollToEditForm () {
    Vue.nextTick(() => this.$vuetify.goTo('#static-location-end'))
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
