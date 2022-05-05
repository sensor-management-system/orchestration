<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        :disabled="this.selectedAction !== null"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/locations/static-location-begin-actions/new?timestamp=' + this.selectedDate.toISO()"
      >
        Start Static Location
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        :disabled="this.selectedAction !== null"
        small
        nuxt
      >
        Start Dynamic Location
      </v-btn>
    </v-card-actions>
    <v-row>
      <v-col cols="12" md="3">
        <DateTimePicker
          v-model="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          @input="updateUrlDate"
        />
      </v-col>
      <v-col>
        <v-select
          v-model="selectedAction"
          :item-text="(x) => x.text"
          :items="locationActionsDates"
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          return-object
          persistent-hint
          @input="updateDate"
        />
      </v-col>
    </v-row>
    <v-row v-if="selectedAction && selectedAction.value">
      <v-col>
        <v-card>
          <v-container>
            <ConfigurationStaticLocationBeginActionData
              v-if="isStaticLocationStartAction"
              :value="selectedAction.value"
              :elevation-data="[]"
              :epsg-codes="[]"
            />
            <ConfigurationStaticLocationEndActionData
              v-if="isStaticLocationEndAction"
              :value="selectedAction.value"
            />
            <ConfigurationDynamicLocationBeginActionData
              v-if="isDynamicLocationStartAction"
              :value="selectedAction.value"
              :epsg-codes="[]"
              :elevation-data="[]"
              :devices="[]"
            />
            <ConfigurationDynamicLocationEndActionData
              v-if="isDynamicLocationEndAction"
              :value="selectedAction.value"
            />
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DateTime } from 'luxon'
import { LocationTypes } from '@/store/configurations'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import ConfigurationStaticLocationBeginActionData
  from '@/components/configurations/ConfigurationStaticLocationBeginActionData.vue'
import ConfigurationStaticLocationEndActionData
  from '@/components/configurations/ConfigurationStaticLocationEndActionData.vue'
import ConfigurationDynamicLocationBeginActionData
  from '@/components/configurations/ConfigurationDynamicLocationBeginActionData.vue'
import ConfigurationDynamicLocationEndActionData
  from '@/components/configurations/ConfigurationDynamicLocationEndActionData.vue'
import { currentAsUtcDateSecondsAsZeros, stringToDate } from '@/utils/dateHelper'

@Component({
  components: { ConfigurationDynamicLocationEndActionData, ConfigurationDynamicLocationBeginActionData, ConfigurationStaticLocationEndActionData, ConfigurationStaticLocationBeginActionData, DateTimePicker },
  computed: mapGetters('configurations', ['locationActionsDates'])
})
export default class ConfigurationShowLocationPage extends Vue {
  private selectedDate = currentAsUtcDateSecondsAsZeros()
  private selectedAction: StaticLocationBeginAction|StaticLocationEndAction|DynamicLocationBeginAction|DynamicLocationEndAction|null = null

  created(){
    if(this.$route.query.timestamp){
      this.selectedDate=stringToDate(this.$route.query.timestamp)
    }
  }
  get configurationId (): string {
    return this.$route.params.configurationId
  }

  updateDate (val) {
    this.selectedDate = val.date
    this.updateUrlDate()
  }

  updateUrlDate(newDate){
    this.$router.push({
      query: {timestamp:this.selectedDate},
      hash: this.$route.hash
    })
  }

  get isStaticLocationStartAction () {
    if (this.selectedAction && this.selectedAction.type) {
      return this.selectedAction.type === LocationTypes.staticStart
    }
    return false
  }

  get isStaticLocationEndAction () {
    if (this.selectedAction && this.selectedAction.type) {
      return this.selectedAction.type === LocationTypes.staticEnd
    }
    return false
  }

  get isDynamicLocationStartAction () {
    if (this.selectedAction && this.selectedAction.type) {
      return this.selectedAction.type === LocationTypes.dynamicStart
    }
    return false
  }

  get isDynamicLocationEndAction () {
    if (this.selectedAction && this.selectedAction.type) {
      return this.selectedAction.type === LocationTypes.dynamicEnd
    }
    return false
  }
}
</script>

<style scoped>

</style>
