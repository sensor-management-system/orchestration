<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
      <v-card-title class="pl-0">
        New Dynamic Location
      </v-card-title>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/locations'"
      >
        cancel
      </v-btn>
    </v-card-actions>
    <DynamicLocationWizard
      ref="DynamicLocationWizard"
      v-model="beginAction"
    >
      <template #save>
        <v-btn
          block
          color="primary"
          @click="save"
        >
          Submit
        </v-btn>
      </template>
    </DynamicLocationWizard>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import { mapActions, mapGetters, mapState } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { SetLoadingAction } from '@/store/progressindicator'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { VocabularyState } from '@/store/vocabulary'
import { ContactsState } from '@/store/contacts'
import {
  AddDynamicLocationBeginActionAction,
  ConfigurationsState,
  LoadDeviceMountActionsIncludingDeviceInformationAction,
  LoadLocationActionTimepointsAction
} from '@/store/configurations'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'
import DynamicLocationWizard from '@/components/configurations/dynamicLocation/DynamicLocationWizard.vue'
@Component({
  components: { DynamicLocationWizard },
  middleware: ['auth'],
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData']),
    ...mapState('contacts', ['contacts']),
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate']),
    ...mapState('configurations', ['selectedLocationDate'])
  },
  methods: {
    ...mapActions('configurations', ['addDynamicLocationBeginAction', 'loadLocationActionTimepoints', 'loadDeviceMountActionsIncludingDeviceInformation']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DynamicLocationActionNew extends mixins(CheckEditAccess) {
  private beginAction: DynamicLocationAction = new DynamicLocationAction()

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  contacts!: ContactsState['contacts']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
  addDynamicLocationBeginAction!: AddDynamicLocationBeginActionAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/locations'
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

  created () {
    this.beginAction.beginDate = this.selectedDate
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get selectedDate (): DateTime {
    return this.selectedLocationDate !== null ? this.selectedLocationDate : currentAsUtcDateSecondsAsZeros()
  }

  closeNewDynamicLocationForm (): void {
    this.$router.push('/configurations/' + this.configurationId + '/locations')
  }

  async save () {
    if (!(this.$refs.DynamicLocationWizard as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.setLoading(true)
      const newId = await this.addDynamicLocationBeginAction({
        configurationId: this.configurationId,
        dynamicLocationAction: this.beginAction
      })
      this.loadLocationActionTimepoints(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/locations/dynamic-location-actions/' + newId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
