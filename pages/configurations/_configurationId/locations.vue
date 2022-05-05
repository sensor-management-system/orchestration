<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
  <NuxtChild />
<!--  <v-card-->
<!--    flat-->
<!--  >-->
<!--    <ProgressIndicator-->
<!--      v-model="isSaving"-->
<!--      dark-->
<!--    />-->
<!--    <v-card-text>-->
<!--      <v-row>-->
<!--        <v-col cols="12" md="3">-->
<!--          <DateTimePicker-->
<!--            v-model="selectedDate"-->
<!--            placeholder="e.g. 2000-01-31 12:00"-->
<!--            label="Configuration at date"-->
<!--            :rules="[dateRules.dateNotNull]"-->
<!--            :readonly="isInEditMode"-->
<!--            :disabled="isInEditMode"-->
<!--          />-->
<!--        </v-col>-->
<!--        <v-col>-->
<!--          <v-select-->
<!--            v-model="selectedDate"-->
<!--            :item-value="(x) => x.date"-->
<!--            :item-text="(x) => x.text"-->
<!--            :items="actionDates"-->
<!--            label="Dates defined by actions"-->
<!--            :readonly="isInEditMode"-->
<!--            :disabled="isInEditMode"-->
<!--            hint="The referenced time zone is UTC."-->
<!--            persistent-hint-->
<!--          />-->
<!--        </v-col>-->
<!--      </v-row>-->
<!--      &lt;!&ndash; First show the current state for the selected date.-->
<!--           In case we have no location at all that is active,-->
<!--           show right that.-->
<!--           In case we have a static location active, let us show that.-->
<!--           And if we already know that we have an end for it, show that-->
<!--           one as well.-->
<!--           In case our active location is a dynamic one - do the very-->
<!--           same stuff as for the static ones - but this time with their-->
<!--           data.-->

<!--           Depending on the current state we also have different actions.-->

<!--      &ndash;&gt;-->
<!--      <div-->
<!--        v-if="showCreateButtons"-->
<!--      >-->
<!--        <v-row-->
<!--          v-if="$auth.loggedIn"-->
<!--        >-->
<!--          <v-col class="text-right">-->
<!--            <v-btn small color="primary" @click="openNewStaticLocationForm">-->
<!--              Start static location-->
<!--            </v-btn>-->
<!--            <v-btn small color="primary" @click="openNewDynamicLocationForm">-->
<!--              Start dynamic location-->
<!--            </v-btn>-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--        <v-row>-->
<!--          <v-row>-->
<!--            <v-col>-->
<!--              <p class="text-center">-->
<!--                There is no location active for the selected date.-->
<!--              </p>-->
<!--            </v-col>-->
<!--          </v-row>-->
<!--        </v-row>-->
<!--      </div>-->

<!--      &lt;!&ndash;-->
<!--      The following pages are included via the NuxtChild component:-->
<!--      - locations/_timestamp.vue - selected readonly version of an action-->
<!--      - locations/static-location-begin-actions/new.vue - new static location begin action-->
<!--      - locations/static-location-begin-actions/_id/edit.vue - edit static location begin action-->
<!--      - locations/static-location-end-actions/new.vue - new static location end action-->
<!--      - locations/static-location-end-actions/_id/edit.vue - edit static location end action-->
<!--      - locations/dynamic-location-begin-actions/new.vue - new dynamic location begin action-->
<!--      - locations/dynamic-location-begin-actions/_id/edit.vue - edit dynamic location begin action-->
<!--      - locations/dynamic-location-end-actions/new.vue - new dynamic location end action-->
<!--      - locations/dynamic-location-end-actions/_id/edit.vue - edit dynamic location end action-->
<!--      &ndash;&gt;-->
<!--      <NuxtChild-->
<!--        v-if="value"-->
<!--        v-model="value"-->
<!--        :contacts="contacts"-->
<!--        :elevation-data="elevationData"-->
<!--        :epsg-codes="epsgCodes"-->
<!--      />-->
<!--    </v-card-text>-->
<!--  </v-card>-->
</template>

<script lang="ts">
import { Component, Prop, Watch, mixins } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'
import * as VueRouter from 'vue-router'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Configuration } from '@/models/Configuration'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'

import { IActionDateWithTextItem } from '@/utils/configurationInterfaces'
import ConfigurationHelper from '@/utils/configurationHelper'
import Validator from '@/utils/validator'

import {
  getCurrentlyActiveLocationAction
} from '@/utils/locationHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions } from 'vuex'

@Component({
  components: {
    DateTimePicker,
    ProgressIndicator
  },
  methods:{
    ...mapActions('vocabulary',['loadEpsgCodes','loadElevationData']),
    ...mapActions('contacts',['loadAllContacts'])
  }
})
export default class ConfigurationLocations extends mixins(Rules) {

  // vuex definition for typescript check
  loadEpsgCodes!:()=>void
  loadElevationData!:()=>void
  loadAllContacts!:()=>void

  async created(){ //TODO Try catch + progress inidcator
    await this.loadEpsgCodes()
    await this.loadElevationData()
    await this.loadAllContacts()
  }

  // private configuration: Configuration = new Configuration()
  // private epsgCodes: EpsgCode[] = []
  // private elevationData: ElevationDatum[] = []
  // private isSaving: boolean = false
  //
  // @Prop({
  //   required: true,
  //   type: Object
  // })
  // readonly value!: Configuration
  //
  // private dateRules: Object = {
  //   dateNotNull: Validator.mustBeProvided('Date')
  // }
  //
  // async fetch (): Promise<void> {
  //   try {
  //     // eslint-disable-next-line
  //     const [_, elevationData, epsgCodes] = await Promise.all([
  //       this.$store.dispatch('contacts/loadAllContacts'),
  //       this.$api.elevationData.findAll(),
  //       this.$api.epsgCodes.findAll()
  //     ])
  //     this.elevationData = elevationData
  //     this.epsgCodes = epsgCodes
  //   } catch (e) {
  //     this.$store.commit('snackbar/setError', 'Failed to fetch resources')
  //   }
  // }
  //
  // created () {
  //   if (this.value) {
  //     this.configuration = Configuration.createFromObject(this.value)
  //   }
  //
  //   // if we get the date via the URL, set the date accordingly
  //   const dateFromUrl = this.dateFromUrlParam(this.$route)
  //   if (dateFromUrl && !this.selectedDate.equals(dateFromUrl)) {
  //     this.selectedDate = dateFromUrl
  //   }
  // }
  //
  // get contacts (): Contact[] {
  //   return this.$store.state.contacts.allContacts
  // }
  //
  // get selectedDate () {
  //   return this.$store.getters['configurations/configurationEditDate']
  // }
  //
  // set selectedDate (newDate: DateTime) {
  //   if (!newDate) {
  //     return
  //   }
  //   const oldDate = this.selectedDate
  //   this.$store.commit('configurations/setConfigurationEditDate', newDate)
  //   if (this.value.id && !newDate.equals(oldDate)) {
  //     const dateString = newDate.toUTC().toISO()
  //     this.$router.push('/configurations/' + this.value.id + '/locations/' + dateString)
  //   }
  // }
  //
  // get isInEditMode (): boolean {
  //   const editUrl = new RegExp('/configurations/' + this.value.id + '/locations/(static-location-begin-actions|static-location-end-actions|dynamic-location-begin-actions|dynamic-location-end-actions)/[0-9]*/?(new|edit)')
  //   return !!this.$route.path.match(editUrl)
  // }
  //
  // get actionDates (): IActionDateWithTextItem[] {
  //   return ConfigurationHelper.getActionDatesWithTextsByConfiguration(this.configuration, this.selectedDate, { useMounts: false, useLoctions: true })
  // }
  //
  // get currentlyActiveLocationAction (): StaticLocationBeginAction | DynamicLocationBeginAction | null {
  //   return getCurrentlyActiveLocationAction(this.configuration, this.selectedDate)
  // }
  //
  // get hasNoActiveLocation (): boolean {
  //   return this.currentlyActiveLocationAction === null
  // }
  //
  // openNewStaticLocationForm (): void {
  //   this.$router.push('/configurations/' + this.value.id + '/locations/static-location-begin-actions/new?date=' + this.selectedDate.toISO())
  // }
  //
  // openNewDynamicLocationForm (): void {
  //   this.$router.push('/configurations/' + this.value.id + '/locations/dynamic-location-begin-actions/new?date=' + this.selectedDate.toISO())
  // }
  //
  // get showCreateButtons (): boolean {
  //   return this.hasNoActiveLocation && !this.isInEditMode
  // }
  //
  // dateFromUrlParam (route: VueRouter.Route): DateTime | undefined {
  //   if (!route.params.timestamp) {
  //     return
  //   }
  //   return DateTime.fromISO(route.params.timestamp).toUTC()
  // }
  //
  // @Watch('value', {
  //   deep: true,
  //   immediate: true
  // })
  // onValueChange (val: Configuration): void {
  //   if (val) {
  //     this.configuration = Configuration.createFromObject(val)
  //   }
  // }
  //
  // @Watch('$route', {
  //   deep: true,
  //   immediate: true
  // })
  // onRouteChange (route: VueRouter.Route): void {
  //   if (route) {
  //     // when the date param is changed (eg. by a cancel or apply button of a child page)
  //     // set the selected date to the date of the URL param
  //     const dateFromUrl = this.dateFromUrlParam(route)
  //     if (dateFromUrl && !dateFromUrl.equals(this.selectedDate)) {
  //       this.selectedDate = dateFromUrl
  //     }
  //   }
  // }
}
</script>
