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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <DynamicLocationActionDataForm
      ref="editDynamicLocationForm"
      v-model="valueCopy"
      :devices="allActiveDevices"
    >
      <template #actions>
        <v-card-actions v-if="$auth.loggedIn">
          <v-spacer />
          <v-btn small @click="closeEditDynamicLocationForm">
            Cancel
          </v-btn>
          <v-btn color="accent" small @click="saveEditedDynamicLocation">
            Apply
          </v-btn>
        </v-card-actions>
      </template>
    </DynamicLocationActionDataForm>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import { DateTime } from 'luxon'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import {
  ActiveDevicesWithPropertiesForDateGetter,
  ConfigurationsState,
  LoadDeviceMountActionsForDynamicLocationAction,
  LoadDynamicLocationActionAction, LoadLocationActionTimepointsAction, UpdateDynamicLocationActionAction
} from '@/store/configurations'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'
import { Device } from '@/models/Device'
import DynamicLocationActionDataForm from '@/components/configurations/DynamicLocationActionDataForm.vue'

@Component({
  components: {
    DynamicLocationActionDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['dynamicLocationAction', 'selectedLocationDate']),
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate'])
  },
  methods: {
    ...mapActions('configurations', ['loadDynamicLocationAction', 'updateDynamicLocationAction', 'loadDeviceMountActionsForDynamicLocation', 'loadLocationActionTimepoints'])
  }
})
export default class DynamicLocationActionEdit extends Vue {
  private valueCopy: DynamicLocationAction = new DynamicLocationAction()
  private isSaving: boolean = false
  private isLoading: boolean = false

  // vuex definition for typescript check
  dynamicLocationAction!: ConfigurationsState['dynamicLocationAction']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadDynamicLocationAction!: LoadDynamicLocationActionAction
  loadDeviceMountActionsForDynamicLocation!: LoadDeviceMountActionsForDynamicLocationAction
  updateDynamicLocationAction!: UpdateDynamicLocationActionAction
  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction

  async created () {
    try {
      this.isLoading = true

      await this.loadDynamicLocationAction(this.actionId)
      await this.loadDeviceMountActionsForDynamicLocation(this.configurationId)
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
    return this.activeDevicesWithPropertiesForDate(this.valueCopy.beginDate)
  }

  get hasEndAction () {
    return this.valueCopy.endContact != null
  }

  closeEditDynamicLocationForm (): void {
    this.$router.push('/configurations/' + this.configurationId + '/locations/dynamic-location-actions/' + this.actionId)
  }

  async saveEditedDynamicLocation () {
    if (!(this.$refs.editDynamicLocationForm as Vue & { isValid: () => boolean }).isValid()) {
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
