<!--
 SPDX-FileCopyrightText: 2020 - 2025

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <v-alert :icon="false" border="left" colored-border elevation="1" type="warning">
          Applying these settings will overwrite the existing settings
          of all current linking forms in the next step.
          <br>
          Please ensure you have the correct values before proceeding.
        </v-alert>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <combobox
          v-model="predefinedLicense"
          :items="licenseItems"
          clearable
          item-text="name"
          label="License"
        >
          <template #item="{ item }">
            <template v-if="typeof item !== 'object'">
              <v-item-content>
                {{ item }}
              </v-item-content>
            </template>
            <template v-else>
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.name }}
                  <v-tooltip v-if="item.definition" bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon color="primary" small v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>{{ item.definition }}</span>
                  </v-tooltip>
                </v-list-item-title>
              </v-list-item-content>
            </template>
          </template>
        </combobox>
      </v-col>
      <v-col align-self="center">
        <v-btn v-if="isPredefinedLicenseAppliedForAllLinkings" disabled>
          <v-icon left>
            mdi-check
          </v-icon>
          Applied
        </v-btn>
        <v-btn
          v-else
          :disabled="!predefinedLicense"
          color="primary"
          @click="applyLicense"
        >
          Apply License
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-model="predefinedAggregationPeriod"
          label="Aggregation period in seconds"
          step="any"
          type="number"
          @wheel.prevent
        />
      </v-col>
      <v-col align-self="center">
        <v-btn
          v-if="isPredefinedAggregationPeriodAppliedForAllLinkings"
          disabled
        >
          <v-icon left>
            mdi-check
          </v-icon>
          Applied
        </v-btn>
        <v-btn
          v-else
          :disabled="!predefinedAggregationPeriod"
          color="primary"
          @click="applyAggregationPeriod"
        >
          Apply aggregation period
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-autocomplete
          v-model="predefinedEndpoint"
          :items="tsmEndpoints"
          :menu-props="{ closeOnContentClick: true }"
          clearable
          item-text="name"
          label="Select endpoint"
          return-object
        >
          <template #item="{ item }">
            <v-list-item-content>
              <v-list-item-title>
                {{ item.name }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ item.url }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col align-self="center">
        <v-btn v-if="isPredefinedEndpointAppliedForAllLinkings" disabled>
          <v-icon left>
            mdi-check
          </v-icon>
          Applied
        </v-btn>
        <v-btn
          v-else
          :disabled="!predefinedEndpoint"
          color="primary"
          @click="applyEndpoint"
        >
          Apply endpoint
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-autocomplete
          v-model="predefinedDatasource"
          :disabled="datasourceSelectionDisabled"
          :hint="datasourceSelectionDisabled ? 'Select an endpoint first' : ''"
          :items="datasourcesForEndpoint(predefinedEndpoint)"
          :loading="isLoadingDatasource"
          :menu-props="{ closeOnContentClick: true }"
          clearable
          item-text="id"
          label="Select datasource"
          persistent-hint
          return-object
        >
          <template #item="{ item }">
            <v-list-item-content>
              <v-list-item-title>
                {{ item.name }}
              </v-list-item-title>
            </v-list-item-content>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col align-self="center">
        <v-btn v-if="isPredefinedDatasourceAppliedForAllLinkings" disabled>
          <v-icon left>
            mdi-check
          </v-icon>
          Applied
        </v-btn>
        <v-btn
          v-else
          :disabled="datasourceSelectionDisabled || !predefinedDatasource"
          color="primary"
          @click="applyDatasource"
        >
          Apply datasource
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-autocomplete
          v-model="predefinedThing"
          :disabled="thingSelectionDisabled"
          :hint="thingSelectionDisabled ? 'Select a datasource first' : ''"
          :items="thingsForDatasource(predefinedDatasource)"
          :loading="isLoadingThings"
          :menu-props="{ closeOnContentClick: true }"
          clearable
          item-text="name"
          label="Select thing"
          persistent-hint
          return-object
        />
      </v-col>
      <v-col align-self="center">
        <v-btn v-if="isPredefinedThingAppliedForAllLinkings" disabled>
          <v-icon left>
            mdi-check
          </v-icon>
          Applied
        </v-btn>
        <v-btn
          v-else
          :disabled="thingSelectionDisabled || !predefinedThing"
          color="primary"
          @click="applyThing"
        >
          Apply thing
        </v-btn>
        <v-tooltip v-if="thingSelectionDisabled" bottom>
          <template #activator="{ on, attrs }">
            <v-icon v-bind="attrs" v-on="on">
              mdi-help-circle
            </v-icon>
          </template>
          You have to select a datasource before selecting a thing
        </v-tooltip>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import Combobox from '@/components/shared/Combobox.vue'
import { License } from '@/models/License'
import { TsmEndpoint } from '@/models/TsmEndpoint'
import {
  DatasourcesForEndpointGetter,
  LoadDatasourcesAction,
  LoadDatastreamsForDatasourceAndThingAction,
  LoadThingsForDatasourceAction,
  ThingsForDatasourceGetter
} from '@/store/tsmLinking'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { VocabularyState } from '@/store/vocabulary'
import { TsmdlThing } from '@/models/TsmdlThing'
import { SetLoadingAction } from '@/store/progressindicator'
import { TsmLinking } from '@/models/TsmLinking'

@Component({
  components: { Combobox, BaseExpandableListItem },
  computed: {
    ...mapState('vocabulary', ['licenses']),
    ...mapState('tsmLinking', ['tsmEndpoints']),
    ...mapGetters('tsmLinking', [
      'datasourcesForEndpoint',
      'thingsForDatasource',
      'tsmEndpoints'
    ])
  },
  methods: {
    ...mapActions('tsmLinking', [
      'loadDatasources',
      'loadThingsForDatasource',
      'loadDatastreamsForDatasourceAndThing'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class TsmLinkingFormPredefinedSettings extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  readonly value!: TsmLinking[]

  // vuex definition for typescript check
  licenses!: VocabularyState['licenses']
  loadDatasources!: LoadDatasourcesAction
  loadThingsForDatasource!: LoadThingsForDatasourceAction
  loadDatastreamsForDatasourceAndThing!: LoadDatastreamsForDatasourceAndThingAction
  datasourcesForEndpoint!: DatasourcesForEndpointGetter
  thingsForDatasource!: ThingsForDatasourceGetter
  setLoading!: SetLoadingAction
  private predefinedLicense: License | null = null
  private predefinedAggregationPeriod: number | null = null
  private predefinedEndpoint: TsmEndpoint | null = null
  private predefinedDatasource: TsmdlDatasource | null = null
  private predefinedThing: TsmdlThing | null = null
  private isLoadingDatasource = false
  private isLoadingThings = false

  get datasourceSelectionDisabled (): boolean {
    return this.datasourcesForEndpoint(this.predefinedEndpoint).length === 0 ||
      !this.isPredefinedEndpointAppliedForAllLinkings
  }

  get thingSelectionDisabled (): boolean {
    return this.thingsForDatasource(this.predefinedDatasource).length === 0 || !this.isPredefinedDatasourceAppliedForAllLinkings
  }

  get usedEndpointIdsInForm (): Set<string> {
    const usedIds = new Set<string>()

    for (const linking of this.value) {
      usedIds.add(linking.tsmEndpoint?.id ?? '')
    }

    return usedIds
  }

  get isPredefinedEndpointAppliedForAllLinkings (): boolean {
    return !!(
      this.predefinedEndpoint &&
      this.usedEndpointIdsInForm.size === 1 &&
      this.usedEndpointIdsInForm.has(this.predefinedEndpoint.id)
    )
  }

  get usedDatasourceIdsInForm (): Set<string> {
    const usedIds = new Set<string>()

    for (const linking of this.value) {
      usedIds.add(linking.datasource?.id ?? '')
    }

    return usedIds
  }

  get isPredefinedDatasourceAppliedForAllLinkings (): boolean {
    return !!(
      this.predefinedDatasource &&
      this.usedDatasourceIdsInForm.size === 1 &&
      this.usedDatasourceIdsInForm.has(this.predefinedDatasource.id)
    )
  }

  get usedThingIdsInForm (): Set<string> {
    const usedIds = new Set<string>()

    for (const linking of this.value) {
      usedIds.add(linking.thing?.id ?? '')
    }

    return usedIds
  }

  get isPredefinedThingAppliedForAllLinkings (): boolean {
    return !!(
      this.predefinedThing &&
      this.usedThingIdsInForm.size === 1 &&
      this.usedThingIdsInForm.has(this.predefinedThing.id)
    )
  }

  get usedLicenseUrisInForm (): Set<string> {
    const usedUris = new Set<string>()

    for (const linking of this.value) {
      usedUris.add(linking.licenseUri ?? '')
    }
    return usedUris
  }

  get isPredefinedLicenseAppliedForAllLinkings (): boolean {
    return !!(
      this.predefinedLicense &&
      this.usedLicenseUrisInForm.size === 1 &&
      this.usedLicenseUrisInForm.has(this.predefinedLicense.uri)
    )
  }

  get usedAggregationPeriodsInForm (): Set<number> {
    const usedPeriods = new Set<number>()

    for (const linking of this.value) {
      usedPeriods.add(linking.aggregationPeriod ?? -1)
    }
    return usedPeriods
  }

  get isPredefinedAggregationPeriodAppliedForAllLinkings (): boolean {
    return !!(
      this.predefinedAggregationPeriod &&
      this.usedAggregationPeriodsInForm.size === 1 &&
      this.usedAggregationPeriodsInForm.has(this.predefinedAggregationPeriod)
    )
  }

  get licenseItems (): License[] {
    // CC-BY-4.0 on top of list
    let items = this.licenses

    const licenseCCBY40 = this.licenses.find(el => el.name === 'CC-BY-4.0')
    if (licenseCCBY40) {
      const licensesThatAreNotCCBY40 = this.licenses.filter(
        el => el.name !== 'CC-BY-4.0'
      )
      items = [licenseCCBY40, ...licensesThatAreNotCCBY40]
    }

    return items
  }

  applyLicense () {
    const copyValue = this.value.slice()

    copyValue.forEach((newLinking) => {
      if (this.predefinedLicense) {
        newLinking.licenseUri = this.predefinedLicense.uri
        newLinking.licenseName = this.predefinedLicense.name
      } else {
        newLinking.licenseUri = ''
        newLinking.licenseName = ''
      }
    })

    this.$emit('input', copyValue)
    this.$store.commit('snackbar/setSuccess', 'License applied')
  }

  applyAggregationPeriod () {
    const copyValue = this.value.slice()
    copyValue.forEach((newLinking) => {
      newLinking.aggregationPeriod = this.predefinedAggregationPeriod
    })

    this.$emit('input', copyValue)
    this.$store.commit('snackbar/setSuccess', 'Aggregation period applied')
  }

  applyEndpoint () {
    const copyValue = this.value.slice()
    copyValue.forEach((newLinking) => {
      newLinking.tsmEndpoint = this.predefinedEndpoint
      newLinking.datasource = null
      newLinking.thing = null
      newLinking.datastream = null
    })
    this.$emit('input', copyValue)
    this.$store.commit('snackbar/setSuccess', 'Endpoint applied')
  }

  applyDatasource () {
    const copyValue = this.value.slice()
    copyValue.forEach((newLinking) => {
      newLinking.datasource = this.predefinedDatasource
      newLinking.thing = null
      newLinking.datastream = null
    })
    this.$emit('input', copyValue)
    this.$store.commit('snackbar/setSuccess', 'Datasource applied')
  }

  applyThing () {
    const copyValue = this.value.slice()
    copyValue.forEach((newLinking) => {
      newLinking.thing = this.predefinedThing
      newLinking.datastream = null
    })
    this.$emit('input', copyValue)
    this.$store.commit('snackbar/setSuccess', 'Thing applied')
  }

  @Watch('predefinedEndpoint.id')
  private async fetchDatasourcesForEndpoint () {
    if (!this.predefinedEndpoint) {
      this.predefinedDatasource = null
      return
    }

    try {
      this.isLoadingDatasource = true
      await this.loadDatasources({ endpoint: this.predefinedEndpoint })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load datasources')
    } finally {
      if (
        this.predefinedDatasource &&
        !this.datasourcesForEndpoint(this.predefinedEndpoint)
          .map(datasource => datasource.id)
          .includes(this.predefinedDatasource.id)
      ) {
        this.predefinedDatasource = null
      }
      this.isLoadingDatasource = false
    }
  }

  @Watch('predefinedDatasource.id')
  private async fetchThingsForDatasource () {
    if (!this.predefinedDatasource) {
      this.predefinedThing = null
      return
    }

    try {
      this.isLoadingThings = true
      await this.loadThingsForDatasource({
        endpoint: this.predefinedEndpoint!,
        datasource: this.predefinedDatasource!
      })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load things')
    } finally {
      if (
        this.predefinedThing &&
        !this.thingsForDatasource(this.predefinedDatasource)
          .map(thing => thing.id)
          .includes(this.predefinedThing.id)
      ) {
        this.predefinedThing = null
      }
      this.isLoadingThings = false
    }
  }

  @Watch('predefinedThing.id')
  private async fetchDatastreamsForThing () {
    if (!this.predefinedThing) {
      return
    }

    try {
      this.setLoading(true)

      await this.loadDatastreamsForDatasourceAndThing({
        endpoint: this.predefinedEndpoint!,
        datasource: this.predefinedDatasource!,
        thing: this.predefinedThing!
      })
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load datastreams')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped></style>
