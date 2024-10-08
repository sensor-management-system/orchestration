<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
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
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
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
    DynamicLocationWizard
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['dynamicLocationAction', 'selectedLocationDate']),
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate'])
  },
  methods: {
    ...mapActions('configurations', ['loadDynamicLocationAction', 'updateDynamicLocationAction', 'loadDeviceMountActionsIncludingDeviceInformation', 'loadLocationActionTimepoints']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DynamicLocationActionEdit extends mixins(CheckEditAccess) {
  private valueCopy: DynamicLocationAction|null = null

  // vuex definition for typescript check
  dynamicLocationAction!: ConfigurationsState['dynamicLocationAction']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadDynamicLocationAction!: LoadDynamicLocationActionAction
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
  updateDynamicLocationAction!: UpdateDynamicLocationActionAction
  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  isLoading!: LoadingSpinnerState['isLoading']
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

  async created () {
    try {
      this.setLoading(true)

      await this.loadDynamicLocationAction(this.actionId)
      await this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId)
      if (this.dynamicLocationAction) {
        this.valueCopy = DynamicLocationAction.createFromObject(this.dynamicLocationAction)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load action')
    } finally {
      this.setLoading(false)
    }
  }

  get selectedDate (): DateTime {
    return this.selectedLocationDate !== null ? this.selectedLocationDate : currentAsUtcDateSecondsAsZeros()
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
      this.setLoading(true)
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
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
