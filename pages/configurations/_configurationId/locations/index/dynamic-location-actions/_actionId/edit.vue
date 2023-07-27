<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-card-title class="pl-0">
        Edit Dynamic Location
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
      v-if="valueCopy"
      ref="DynamicLocationWizard"
      v-model="valueCopy"
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
import { mapActions, mapGetters, mapState } from 'vuex'
import { DateTime } from 'luxon'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import {
  ActiveDevicesWithPropertiesForDateGetter,
  ConfigurationsState,
  LoadDeviceMountActionsIncludingDeviceInformationAction,
  LoadDynamicLocationActionAction, LoadLocationActionTimepointsAction, UpdateDynamicLocationActionAction
} from '@/store/configurations'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'
import { Device } from '@/models/Device'
import DynamicLocationWizard from '@/components/configurations/dynamicLocation/DynamicLocationWizard.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    DynamicLocationWizard,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['dynamicLocationAction', 'selectedLocationDate']),
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate'])
  },
  methods: {
    ...mapActions('configurations', ['loadDynamicLocationAction', 'updateDynamicLocationAction', 'loadDeviceMountActionsIncludingDeviceInformation', 'loadLocationActionTimepoints'])
  }
})
export default class DynamicLocationActionEdit extends mixins(CheckEditAccess) {
  private valueCopy: DynamicLocationAction|null = null
  private isSaving: boolean = false
  private isLoading: boolean = false

  // vuex definition for typescript check
  dynamicLocationAction!: ConfigurationsState['dynamicLocationAction']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadDynamicLocationAction!: LoadDynamicLocationActionAction
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
  updateDynamicLocationAction!: UpdateDynamicLocationActionAction
  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction

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

  async created () {
    try {
      this.isLoading = true

      await this.loadDynamicLocationAction(this.actionId)
      await this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId)
      if (this.dynamicLocationAction) {
        this.valueCopy = DynamicLocationAction.createFromObject(this.dynamicLocationAction)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load action')
    } finally {
      this.isLoading = false
    }
  }

  get selectedDate (): DateTime {
    return this.selectedLocationDate !== null ? this.selectedLocationDate : currentAsUtcDateSecondsAsZeros()
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get allActiveDevices (): Device[] {
    if (!this.valueCopy) {
      return []
    }
    return this.activeDevicesWithPropertiesForDate(this.valueCopy.beginDate, this.valueCopy.endDate)
  }

  closeEditDynamicLocationForm (): void {
    this.$router.push('/configurations/' + this.configurationId + '/locations/dynamic-location-actions/' + this.actionId)
  }

  async save () {
    if (!this.valueCopy) {
      return
    }

    if (!(this.$refs.DynamicLocationWizard as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.updateDynamicLocationAction({
        configurationId: this.configurationId,
        dynamicLocationAction: this.valueCopy
      })
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      await this.loadDynamicLocationAction(this.actionId)
      this.loadLocationActionTimepoints(this.configurationId)
      this.closeEditDynamicLocationForm()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
