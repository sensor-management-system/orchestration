<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-stepper v-model="step">
      <v-stepper-header>
        <v-stepper-step
          editable
          step="1"
        >
          Select Configuration
        </v-stepper-step>

        <v-divider />

        <v-stepper-step
          :editable="isStep2Editable"
          step="2"
        >
          Choose Mount Setup
        </v-stepper-step>

        <v-divider />

        <v-stepper-step
          step="3"
          :editable="isStep3Editable"
        >
          Provide Information
        </v-stepper-step>
        <v-divider />

        <v-stepper-step
          step="4"
          :editable="isStep4Editable"
        >
          Overview & Submit
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <ReuseConfigurationSearch
            @selected="selectConfiguration"
          />
        </v-stepper-content>

        <v-stepper-content step="2">
          <ReuseSelectMount
            v-if="selectedConfiguration"
            :selected-configuration="selectedConfiguration"
            @selected="selectMount"
          />
          <v-btn
            class="mt-1"
            color="secondary"
            @click="step = 1"
          >
            Previous
          </v-btn>
          <v-btn
            class="mt-1"
            color="primary"
            :disabled="!isStep3Editable"
            @click="step = 3"
          >
            Continue
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <ReuseUpdateMountInformation
            v-if="selectedMountTree"
            ref="reuseUpdateMountInformation"
            class="ml-1"
            :selected-mount-tree="selectedMountTree"
            :has-form-errors.sync="hasUpdateMountInformationFormErrors"
            @update="updateMountInformation"
          />
          <v-btn
            class="mt-1"
            color="secondary"
            @click="step = 2"
          >
            Previous
          </v-btn>
          <v-btn
            class="mt-1"
            color="primary"
            :disabled="!isStep4Editable"
            @click="step = 4"
          >
            Continue
          </v-btn>
        </v-stepper-content>
        <v-stepper-content step="4">
          <div v-if="treeWithUpdatedMountActions && beginDate">
            <ReuseSubmitOverview
              :selected-configuration="selectedConfiguration"
              :selected-mount-tree="treeWithUpdatedMountActions"
              :begin-date="beginDate"
              :end-date="endDate"
            />
            <v-row>
              <v-col>
                <v-btn
                  class="mt-1"
                  color="secondary"
                  @click="step = 3"
                >
                  Previous
                </v-btn>
              </v-col>
              <v-spacer />
              <v-col cols="1">
                <ReuseSaveMountActions
                  v-model="hasSaved"
                  :current-configuration-id="configurationId"
                  :selected-mount-tree="treeWithUpdatedMountActions"
                  :begin-date="beginDate"
                  :end-date="endDate"
                  class="mt-1"
                />
              </v-col>
            </v-row>
          </div>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="true"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'
import { DateTime } from 'luxon'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import BaseList from '@/components/shared/BaseList.vue'
import ConfigurationsListItem from '@/components/configurations/ConfigurationsListItem.vue'
import { Configuration } from '@/models/Configuration'
import DateTimePicker from '@/components/DateTimePicker.vue'
import {
  ConfigurationsState,
  LoadMountingActionsAction, MountActionDateItemsGetter, SetSelectedDateAction
} from '@/store/configurations'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import MountActionEditForm from '@/components/configurations/MountActionEditForm.vue'
import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'
import ReuseConfigurationSearch from '@/components/configurations/reuseMounts/ReuseConfigurationSearch.vue'
import ReuseSelectMount from '@/components/configurations/reuseMounts/ReuseSelectMount.vue'
import ReuseUpdateMountInformation from '@/components/configurations/reuseMounts/ReuseUpdateMountInformation.vue'
import ReuseSubmitOverview from '@/components/configurations/reuseMounts/ReuseSubmitOverview.vue'
import ReuseSaveMountActions from '@/components/configurations/reuseMounts/ReuseSaveMountActions.vue'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

@Component({
  components: {
    ReuseSaveMountActions,
    ReuseSubmitOverview,
    ReuseUpdateMountInformation,
    ReuseSelectMount,
    ReuseConfigurationSearch,
    MountActionDetailsForm,
    MountActionEditForm,
    ConfigurationsTreeView,
    DateTimePicker,
    ConfigurationsListItem,
    BaseList,
    NavigationGuardDialog
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', [
      'configurations',
      'selectedDate',
      'pageNumber',
      'configurationMountingActionsForDate'
    ]),
    ...mapState('contacts', ['contacts']),
    ...mapGetters('configurations', ['mountActionDateItems'])
  },
  methods: {
    ...mapActions('configurations', [
      'searchConfigurationsPaginated',
      'setPageNumber',
      'setSelectedDate',
      'loadMountingActions', // must be done to get mountActionDateItems
      'loadMountingConfigurationForDate',
      'addDeviceMountAction',
      'addPlatformMountAction'
    ])
  }
})
export default class ConfigurationCopyPlatformsAndDevicesPage extends Vue {
  // Stepper
  private step = 1
  // Navigation guard
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private hasSaved = false

  private selectedConfiguration: Configuration | null = null
  private selectedMountTree: ConfigurationsTree | null = null
  private treeWithUpdatedMountActions: ConfigurationsTree | null = null
  private beginDate: DateTime | null = null
  private endDate: DateTime | null = null

  private hasUpdateMountInformationFormErrors = false

  // vuex
  private loadMountingActions!: LoadMountingActionsAction
  private mountActionDateItems!: MountActionDateItemsGetter
  private selectedDate!: ConfigurationsState['selectedDate']
  private setSelectedDate!: SetSelectedDateAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isStep2Editable () {
    return this.selectedConfiguration !== null
  }

  get isStep3Editable () {
    return this.isStep2Editable && this.selectedMountTree !== null
  }

  get isStep4Editable () {
    return this.isStep2Editable && this.isStep3Editable && this.beginDate !== null && !this.hasUpdateMountInformationFormErrors
  }

  async loadMountActions (): Promise<void> {
    if (!this.selectedConfiguration) {
      return
    }
    try {
      await this.loadMountingActions(this.selectedConfiguration.id)
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    }
  }

  async selectConfiguration (configuration: Configuration) {
    this.selectedConfiguration = configuration
    await this.loadMountActions()
    this.presetDate()

    this.step = 2
  }

  presetDate () {
    if (this.mountActionDateItems.length > 0) {
      const result = this.mountActionDateItems.reduce((previous: { text: string, value: DateTime }, current: {
        text: string,
        value: DateTime
      }) => {
        if (this.selectedDate !== null) {
          const diffA = current.value.diff(this.selectedDate, 'seconds').toObject().seconds
          const diffB = previous.value.diff(this.selectedDate, 'seconds').toObject().seconds

          if (diffA && diffB) {
            const absoluteDiffA = Math.abs(diffA)
            const absoluteDiffB = Math.abs(diffB)

            return absoluteDiffA - absoluteDiffB < 0 ? current : previous
          }
        }
        return previous
      })
      this.setSelectedDate(result.value)
    }
  }

  async selectMount (mount: ConfigurationsTree | null) {
    this.selectedMountTree = mount

    if (mount == null) {
      this.treeWithUpdatedMountActions = null
    }

    await this.$nextTick()
    if (this.$refs.reuseUpdateMountInformation) {
      const reuseUpdateMountInformation = this.$refs.reuseUpdateMountInformation as Vue & { checkAvailabilityOfSelectedMountTree: () => Promise<void>,
        setSelectedMountNode: (node: DeviceNode | PlatformNode | null) => void
      }
      await reuseUpdateMountInformation.checkAvailabilityOfSelectedMountTree()
      reuseUpdateMountInformation.setSelectedMountNode(null)
    }
  }

  updateMountInformation (info: { beginDate: DateTime | null, endDate: DateTime | null, tree: ConfigurationsTree }) {
    const { beginDate, endDate, tree } = info
    this.treeWithUpdatedMountActions = tree
    this.beginDate = beginDate
    this.endDate = endDate
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (!this.hasSaved) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }
}
</script>

<style scoped>

</style>
