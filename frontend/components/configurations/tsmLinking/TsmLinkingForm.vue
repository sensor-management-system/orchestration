<!--
SPDX-FileCopyrightText: 2020 - 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-form
      ref="tsmLinkingForm"
      @submit.prevent
    >
      <v-card flat>
        <v-card-title>Linking</v-card-title>
        <v-container>
          <v-row
            dense
          >
            <v-col
              cols="12"
            >
              <v-autocomplete
                :items="tsmEndpoints"
                :menu-props="{closeOnContentClick: true}"
                :rules="[rules.required]"
                :value="copyValue.tsmEndpoint"
                class="required"
                clearable
                item-text="name"
                label="Select endpoint"
                required
                return-object
                @input="update('endpoint',$event)"
              >
                <template #item="data">
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ data.item.name }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ data.item.url }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </template>
                <template v-if="suggestedTsmEndpoint" #prepend-item>
                  <v-list-item @click="update('endpoint', suggestedTsmEndpoint)">
                    <v-list-item-content>
                      <label>
                        Suggested Data Endpoint
                        <v-tooltip top>
                          <template #activator="{ on }">
                            <v-icon
                              small
                              v-on="on"
                            >
                              mdi-information-outline
                            </v-icon>
                          </template>
                          This endpoint is suggested based on recent selected endpoints for this device.
                        </v-tooltip>
                      </label>
                      <v-list-item-title>
                        {{ suggestedTsmEndpoint.name }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        {{ suggestedTsmEndpoint.url }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider class="mt-2" />
                </template>
              </v-autocomplete>
            </v-col>
            <v-col
              cols="12"
            >
              <v-autocomplete
                :disabled="datasourceSelectionDisabled"
                :items="datasourcesForEndpoint(copyValue.tsmEndpoint)"
                :loading="isLoadingDatasource"
                :menu-props="{closeOnContentClick: true}"
                :rules="[rules.required]"
                :value="copyValue.datasource"
                class="required"
                clearable
                item-text="id"
                label="Select datasource"
                required
                return-object
                @input="update('datasource',$event)"
              >
                <template #item="data">
                  <v-list-item @click="update('datasource', data.item)">
                    <v-list-item-title>
                      {{ data.item.name }}
                    </v-list-item-title>
                  </v-list-item>
                </template>
                <template v-if="suggestedDatasource" #prepend-item>
                  <v-list-item @click="update('datasource', suggestedDatasource)">
                    <v-list-item-title>
                      <label>
                        Suggested Datasource
                        <v-tooltip top>
                          <template #activator="{ on }">
                            <v-icon
                              small
                              v-on="on"
                            >
                              mdi-information-outline
                            </v-icon>
                          </template>
                          This datasource is suggested based on recent selected datasources for this device.
                        </v-tooltip>
                      </label>
                      {{ suggestedDatasource.id }}
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider class="mt-2" />
                </template>
              </v-autocomplete>
            </v-col>
            <v-col
              cols="12"
            >
              <v-autocomplete
                :disabled="thingSelectionDisabled"
                :items="thingsForDatasource(copyValue.datasource)"
                :loading="isLoadingThing"
                :menu-props="{closeOnContentClick: true}"
                :rules="[rules.required]"
                :value="copyValue.thing"
                class="required"
                clearable
                item-text="name"
                label="Select thing"
                required
                return-object
                @input="update('thing',$event)"
              >
                <template v-if="suggestedThing" #prepend-item>
                  <v-list-item @click="update('thing', suggestedThing)">
                    <v-list-item-title>
                      <label>
                        Suggested Thing
                        <v-tooltip top>
                          <template #activator="{ on }">
                            <v-icon
                              small
                              v-on="on"
                            >
                              mdi-information-outline
                            </v-icon>
                          </template>
                          This thing is suggested based on recent selected things for this device.
                        </v-tooltip>
                      </label>
                      {{ suggestedThing.name }}
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider class="mt-2" />
                </template>
              </v-autocomplete>
            </v-col>

            <v-col
              class="nowrap-truncate"
              cols="12"
            >
              <v-autocomplete
                :disabled="datastreamSelectionDisabled"
                :items="filteredDatastreams"
                :loading="isLoadingDatastream"
                :rules="[rules.required]"
                :value="copyValue.datastream"
                class="required"
                clearable
                item-text="name"
                label="Select datastream"
                required
                return-object
                @input="update('datastream',$event)"
              >
                <template #prepend-item>
                  <v-list-item>
                    <v-list-item-title>
                      <v-radio-group v-model="datastreamFilter" row>
                        <v-radio label="All datastreams" value="all" />
                        <v-radio label="Unused datastreams only" value="unused" />
                        <v-radio label="Used datastreams only" value="used" />
                      </v-radio-group>
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider class="mt-2" />
                </template>
                <template #item="{ item }">
                  <div class="d-flex align-center">
                    {{ item.name }}
                    <v-tooltip
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-chip
                          v-show="isDatastreamUsedInForm(item)"
                          class="ml-2"
                          color="secondary"
                          label
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          Used
                          <v-icon right small>
                            mdi-information-outline
                          </v-icon>
                        </v-chip>
                      </template>
                      This datastream is already used in another linking
                    </v-tooltip>
                  </div>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col
              lg="6"
              md="12"
              xl="6"
            >
              <DateTimePicker
                :max-date="dateToString(copyValue.deviceMountAction.endDate)"
                :min-date="dateToString(copyValue.deviceMountAction.beginDate)"
                :required="true"
                :rules="[rules.required,...startDateExtraRules]"
                :value="copyValue.startDate"
                hint="Start date"
                label="Select begin date"
                @input="update('startDate',$event)"
              />
            </v-col>
            <v-col
              lg="6"
              md="12"
              xl="6"
            >
              <DateTimePicker
                :max-date="dateToString(copyValue.deviceMountAction.endDate)"
                :min-date="dateToString(copyValue.deviceMountAction.beginDate)"
                :rules="[...endDateExtraRules]"
                :value="copyValue.endDate"
                hint="Optional. Leave blank for open end"
                label="Select end date"
                placeholder="Open End"
                @input="update('endDate',$event)"
              />
            </v-col>
            <v-col
              class="nowrap-truncate"
              cols="12"
            >
              <combobox
                :items="licenseItems"
                :value="valueLicense"
                clearable
                item-text="name"
                label="License"
                @input="updateLicense"
              >
                <template v-if="suggestedLicense" #prepend-item>
                  <v-list-item @click="updateLicense(suggestedLicense)">
                    <v-list-item-title>
                      <label>
                        Suggested license
                        <v-tooltip top>
                          <template #activator="{ on }">
                            <v-icon
                              small
                              v-on="on"
                            >
                              mdi-information-outline
                            </v-icon>
                          </template>
                          This license is suggested based on recent selected licenses for this device.
                        </v-tooltip>
                      </label>
                      {{ suggestedLicense }}
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider class="mt-2" />
                </template>
                <template #append-outer>
                  <v-tooltip
                    v-if="valueLicenseDefinition"
                    right
                  >
                    <template #activator="{ on, attrs }">
                      <v-icon
                        color="primary"
                        small
                        v-bind="attrs"
                        v-on="on"
                      >
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>{{ valueLicenseDefinition }}</span>
                  </v-tooltip>
                  <a
                    v-if="valueLicense && valueLicense.uri"
                    :href="valueLicense.uri"
                    style="line-height: 2;"
                    target="_blank"
                  >
                    <v-icon small>
                      mdi-open-in-new
                    </v-icon>
                  </a>
                  <v-btn icon @click="showNewLicenseDialog = true">
                    <v-icon>
                      mdi-tooltip-plus-outline
                    </v-icon>
                  </v-btn>
                </template>
                <template #item="data">
                  <template v-if="(typeof data.item) !== 'object'">
                    <v-item-content>
                      {{ data.item }}
                    </v-item-content>
                  </template>
                  <template v-else>
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ data.item.name }}
                        <v-tooltip
                          v-if="data.item.definition"
                          bottom
                        >
                          <template #activator="{ on, attrs }">
                            <v-icon
                              color="primary"
                              small
                              v-bind="attrs"
                              v-on="on"
                            >
                              mdi-help-circle-outline
                            </v-icon>
                          </template>
                          <span>{{ data.item.definition }}</span>
                        </v-tooltip>
                      </v-list-item-title>
                    </v-list-item-content>
                  </template>
                </template>
              </combobox>
            </v-col>
            <v-col
              lg="6"
              md="12"
              xl="6"
            >
              <v-text-field
                :label="aggregationPeriodLabel"
                :value="copyValue.aggregationPeriod"
                step="any"
                type="number"
                @change="update('aggregationPeriod', $event)"
                @wheel.prevent
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <label>
                Involved devices
                <v-tooltip
                  bottom
                >
                  <template #activator="{ on, attrs }">
                    <v-icon
                      small
                      v-bind="attrs"
                      v-on="on"
                    >
                      mdi-help-circle
                    </v-icon>
                  </template>
                  Devices that are involved in the measurement (like loggers, multiplexers). These must be mounted in
                  the current configuration.
                </v-tooltip>
              </label>
              <tsm-linking-device-select
                v-model="selectedDevices"
                :devices="devicesWithoutCurrent"
                :linkings="[value]"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-form>
    <license-dialog
      v-model="showNewLicenseDialog"
      :initial-term="valueLicense ? valueLicense.name : null"
      @aftersubmit="updateLicense"
    />
  </div>
</template>
<script lang="ts">
import { Component, mixins, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapGetters, mapState, mapActions } from 'vuex'
import DateTimePicker from '@/components/DateTimePicker.vue'
import LicenseDialog from '@/components/devices/LicenseDialog.vue'
import Combobox from '@/components/shared/Combobox.vue'
import Validator from '@/utils/validator'
import { Rules } from '@/mixins/Rules'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlThing } from '@/models/TsmdlThing'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import {
  DatasourcesForEndpointGetter,
  DatasourcesGetter,
  DatastreamsForThingGetter,
  DatastreamsGetter,
  LoadDatasourcesAction,
  LoadDatastreamsForDatasourceAndThingAction,
  LoadThingsForDatasourceAction,
  SuggestedDatasourceIdGetter,
  SuggestedLicenseNameGetter,
  SuggestedThingIdGetter,
  SuggestedTsmEndpointIdGetter,
  ThingsForDatasourceGetter,
  ThingsGetter,
  TsmEndpointsGetter
} from '@/store/tsmLinking'
import { dateToString } from '@/utils/dateHelper'
import { TsmEndpoint } from '@/models/TsmEndpoint'
import { License } from '@/models/License'
import { VocabularyState } from '@/store/vocabulary'
import { CvSelectItem, ICvSelectItem } from '@/models/CvSelectItem'
import { Device } from '@/models/Device'
import TsmLinkingDeviceSelect from '@/components/configurations/tsmLinking/TsmLinkingDeviceSelect.vue'
import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'

type LicenseComboboxValue = License | string | undefined

@Component({
  components: {
    Combobox,
    DateTimePicker,
    LicenseDialog,
    TsmLinkingDeviceSelect
  },
  computed: {
    ...mapGetters('tsmLinking', [
      'datasources',
      'things',
      'datastreams',
      'suggestedThingId',
      'suggestedDatasourceId',
      'suggestedTsmEndpointId',
      'suggestedLicenseName',
      'datastreamsForThing',
      'datasourcesForEndpoint',
      'thingsForDatasource',
      'tsmEndpoints'
    ]),
    ...mapState('vocabulary', ['licenses'])
  },
  methods: {
    dateToString,
    ...mapActions('tsmLinking', ['loadDatasources', 'loadThingsForDatasource', 'loadDatastreamsForDatasourceAndThing'])
  }
})
export default class TsmLinkingForm extends mixins(Rules) {
  @Prop({
    required: true
  })
  readonly value!: TsmLinking

  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  @Prop({
    required: true,
    type: Array
  })
  private newLinkings!: TsmLinking[]

  // vuex definition for typescript check
  tsmEndpoints!: TsmEndpointsGetter
  licenses!: VocabularyState['licenses']
  datasources!: DatasourcesGetter
  things!: ThingsGetter
  datastreams!: DatastreamsGetter
  suggestedThingId!: SuggestedThingIdGetter
  suggestedDatasourceId!: SuggestedDatasourceIdGetter
  suggestedTsmEndpointId!: SuggestedTsmEndpointIdGetter
  suggestedLicenseName!: SuggestedLicenseNameGetter
  datasourcesForEndpoint!: DatasourcesForEndpointGetter
  thingsForDatasource!: ThingsForDatasourceGetter
  datastreamsForThing!: DatastreamsForThingGetter
  loadDatasources!: LoadDatasourcesAction
  loadThingsForDatasource!: LoadThingsForDatasourceAction
  loadDatastreamsForDatasourceAndThing!: LoadDatastreamsForDatasourceAndThingAction

  private copyValue: TsmLinking = TsmLinking.createFromObject(this.value)
  private datastreamFilter = 'all'
  private isLoadingDatasource = false
  private isLoadingThing = false
  private isLoadingDatastream = false
  private showNewLicenseDialog = false

  get selectedDevices (): Device[] {
    return this.copyValue.filterInvolvedDevices(this.devices)
  }

  set selectedDevices (newSelectedDevices: Device[]) {
    const newObj = TsmLinking.createFromObject(this.copyValue)
    const newInvolvedDevices = []
    let orderIndex = 0
    for (const device of newSelectedDevices) {
      newInvolvedDevices.push(TsmLinkingInvolvedDevice.createFromObject({
        id: null,
        deviceId: device.id,
        orderIndex
      }))
      orderIndex += 1
    }
    newObj.involvedDevices = newInvolvedDevices
    this.$emit('input', newObj)
  }

  get devicesWithoutCurrent (): Device[] {
    return this.devices.filter(d => d.id !== this.copyValue.deviceMountAction?.device.id)
  }

  get startDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.copyValue.startDate, this.copyValue.endDate),
      Validator.startDateMustBeAfterStartOfMountAction(this.copyValue.startDate, this.copyValue.deviceMountAction!)
    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.copyValue.startDate, this.copyValue.endDate),
      Validator.endDateMustBeBeforeEndOfMountAction(this.copyValue.endDate, this.copyValue.deviceMountAction!)
    ]
  }

  get suggestedThing (): TsmdlThing | null {
    const thingId = this.suggestedThingId(this.copyValue.deviceMountAction!, this.newLinkings)
    if (thingId === null) {
      return null
    }
    return this.things.find(thing => thing.id === thingId) ?? null
  }

  get suggestedDatasource (): TsmdlDatasource | null {
    const datasourceId = this.suggestedDatasourceId(this.copyValue.deviceMountAction!, this.newLinkings)
    if (datasourceId === null) {
      return null
    }
    return this.datasources.find(datasource => datasource.id === datasourceId) ?? null
  }

  get suggestedTsmEndpoint (): TsmEndpoint | null {
    const endpointId = this.suggestedTsmEndpointId(this.copyValue.deviceMountAction!, this.newLinkings)
    if (endpointId === null) {
      return null
    }
    return this.tsmEndpoints.find(endpoint => endpoint.id === endpointId) ?? null
  }

  get suggestedLicense (): License | null {
    const licenseName = this.suggestedLicenseName(this.copyValue.deviceMountAction!, this.newLinkings)
    if (licenseName === null) {
      return null
    }
    return this.licenses.find(license => license.name === licenseName) ?? null
  }

  get datasourceSelectionDisabled (): boolean {
    return (!this.copyValue.tsmEndpoint || !this.datasources)
  }

  get thingSelectionDisabled (): boolean {
    return (!this.copyValue.datasource || !this.things)
  }

  get datastreamSelectionDisabled (): boolean {
    return (!this.copyValue.thing || !this.datastreams)
  }

  get filteredDatastreams (): TsmdlDatastream[] {
    const allDatastreams = this.datastreamsForThing(this.copyValue.thing)

    // Always keep the currently selected item, even if it doesn't match filter
    let isCurrentSelectionUsed = false
    if (this.copyValue.datastream) {
      isCurrentSelectionUsed = this.isDatastreamUsedInForm(this.copyValue.datastream)
    }

    const keptItem = this.datastreamFilter === 'unused' && isCurrentSelectionUsed
      ? [this.copyValue.datastream!]
      : []

    let filtered: TsmdlDatastream[] = []
    if (this.datastreamFilter === 'all') {
      filtered = allDatastreams
    } else if (this.datastreamFilter === 'used') {
      filtered = allDatastreams.filter((ds) => {
        return this.isDatastreamUsedInForm(ds)
      })
    } else if (this.datastreamFilter === 'unused') {
      filtered = allDatastreams.filter((ds) => {
        return !this.isDatastreamUsedInForm(ds)
      })
    }

    return [...keptItem, ...filtered]
  }

  get aggregationPeriodLabel (): string {
    if (this.copyValue.deviceProperty?.aggregationTypeName) {
      return `Aggregation period in seconds - ${this.copyValue.deviceProperty?.aggregationTypeName}`
    }
    return 'Aggregation period in seconds'
  }

  get licenseItems (): License[] {
    // CC-BY-4.0 on top of list
    let items = this.licenses

    const licenseCCBY40 = this.licenses.find(el => el.name === 'CC-BY-4.0')
    if (licenseCCBY40) {
      const licensesThatAreNotCCBY40 = this.licenses.filter(el => el.name !== 'CC-BY-4.0')
      items = [licenseCCBY40, ...licensesThatAreNotCCBY40]
    }

    const licenseIndex = this.licenses.findIndex(l => l.uri === this.copyValue.licenseUri)
    if (licenseIndex > -1 || (!this.valueLicense)) {
      return items
    }
    const additionalLicense = License.createFromObject({
      id: '',
      name: this.copyValue.licenseName,
      definition: '',
      provenance: '',
      provenanceUri: '',
      category: '',
      note: '',
      uri: this.copyValue.licenseUri,
      globalProvenanceId: null
    })

    return [additionalLicense, ...items]
  }

  get valueLicense (): ICvSelectItem | null {
    if (!this.copyValue.licenseName && !this.copyValue.licenseUri) {
      return null
    }
    const license = this.licenses.find(l => l.uri === this.copyValue.licenseUri)
    if (license) {
      return license
    }
    return new CvSelectItem({
      name: this.copyValue.licenseName,
      uri: this.copyValue.licenseUri,
      definition: '',
      id: null
    })
  }

  get valueLicenseDefinition (): string {
    return this.valueLicense?.definition || ''
  }

  get usedDatastreamIdsInForm (): Set<string> {
    const usedIds = new Set<string>()

    if (!this.newLinkings || !Array.isArray(this.newLinkings)) {
      return usedIds
    }

    this.newLinkings.forEach((linking: TsmLinking) => {
      // Skip the current linking itself to avoid self-referencing
      if (linking !== this.value && linking.datastream?.id) {
        usedIds.add(linking.datastream.id)
      }
    })

    return usedIds
  }

  isDatastreamUsedInForm (datastream: TsmdlDatastream): boolean {
    return this.usedDatastreamIdsInForm.has(datastream.id)
  }

  generatePropertyTitle (measuredQuantity: DeviceProperty) {
    if (measuredQuantity) {
      const propertyName = measuredQuantity.propertyName ?? ''
      const label = measuredQuantity.label ?? ''
      const unit = measuredQuantity.unitName ?? ''
      return `${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
    }
    return ''
  }

  public validateForm (): boolean {
    return (this.$refs.tsmLinkingForm as Vue & { validate: () => boolean }).validate()
  }

  async stall (stallTime = 3000) {
    await new Promise(resolve => setTimeout(resolve, stallTime))
  }

  updateLicense (value: LicenseComboboxValue) {
    const newObj = TsmLinking.createFromObject(this.copyValue)
    if (value) {
      if (typeof value === 'string') {
        newObj.licenseName = value
        const licenseIndex = this.licenses.findIndex(l => l.name === value)
        if (licenseIndex > -1) {
          newObj.licenseUri = this.licenses[licenseIndex].uri
        } else {
          newObj.licenseUri = ''
        }
      } else {
        newObj.licenseName = value.name
        newObj.licenseUri = value.uri
      }
    } else {
      newObj.licenseUri = ''
      newObj.licenseName = ''
    }
    this.$emit('input', newObj)
  }

  async update (key: string, result: any) {
    const newObj = TsmLinking.createFromObject(this.copyValue)
    switch (key) {
      case 'endpoint':
        newObj.tsmEndpoint = result
        newObj.datasource = null
        newObj.thing = null
        newObj.datastream = null
        if (this.datasourcesForEndpoint(result).length !== 0) {
          break
        }
        try {
          this.isLoadingDatasource = true
          await this.loadDatasources({ endpoint: result })
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Failed to load datasources')
        } finally {
          this.isLoadingDatasource = false
        }
        break
      case 'datasource':
        newObj.datasource = result
        newObj.thing = null
        newObj.datastream = null
        if (this.thingsForDatasource(result).length !== 0) {
          break
        }
        try {
          this.isLoadingThing = true
          await this.loadThingsForDatasource({
            endpoint: this.copyValue.tsmEndpoint!,
            datasource: result
          })
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Failed to load things')
        } finally {
          this.isLoadingThing = false
        }
        break
      case 'thing':
        newObj.thing = result
        newObj.datastream = null
        if (this.datastreamsForThing(result).length !== 0) {
          break
        }
        try {
          this.isLoadingDatastream = true
          await this.loadDatastreamsForDatasourceAndThing({
            endpoint: this.copyValue.tsmEndpoint!,
            datasource: this.copyValue.datasource!,
            thing: result
          })
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Failed to load datastreams')
        } finally {
          this.isLoadingDatastream = false
        }
        break
      case 'datastream':
        newObj.datastream = result
        break
      case 'startDate':
        newObj.startDate = result
        break
      case 'endDate':
        newObj.endDate = result
        break
      case 'aggregationPeriod':
        newObj.aggregationPeriod = result
        break
    }
    this.$emit('input', newObj)
  }

  public isValid (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChanged (newValue: TsmLinking) {
    this.copyValue = TsmLinking.createFromObject(newValue)
  }
}
</script>
