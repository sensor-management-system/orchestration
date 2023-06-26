<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
 - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
              :value="value.tsmEndpoint"
              label="Select endpoint"
              item-text="name"
              return-object
              required
              :rules="[rules.required]"
              clearable
              class="required"
              :menu-props="{closeOnContentClick: true}"
              @input="update('endpoint',$event)"
            >
              <template v-if="suggestedTsmEndpoint" #prepend-item>
                <v-list-item @click="update('endpoint', suggestedTsmEndpoint)">
                  <v-list-item-title>
                    <label>
                      Suggested TSMDL Endpoint
                      <v-tooltip top>
                        <template #activator="{ on }">
                          <v-icon
                            small
                            v-on="on"
                          >
                            mdi-information-outline
                          </v-icon>
                        </template>
                        This endpoint is suggested based on recent selected datasources for this device.
                      </v-tooltip>
                    </label>
                    {{ suggestedTsmEndpoint.name }}
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
              :items="datasources"
              :value="value.datasource"
              :loading="isLaodingDatasource"
              label="Select datasource"
              item-text="id"
              return-object
              required
              :rules="[rules.required]"
              clearable
              :disabled="datasourceSelectionDisabled"
              class="required"
              :menu-props="{closeOnContentClick: true}"
              @input="update('datasource',$event)"
            >
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
              :items="things"
              :value="value.thing"
              :loading="isLoadingThing"
              label="Select thing"
              item-text="name"
              return-object
              required
              :rules="[rules.required]"
              clearable
              class="required"
              :disabled="thingSelectionDisabled"
              :menu-props="{closeOnContentClick: true}"
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
            cols="12"
            class="nowrap-truncate"
          >
            <v-autocomplete
              :items="datastreams"
              :value="value.datastream"
              :loading="isLoadingDatastream"
              label="Select datastream"
              item-text="name"
              return-object
              required
              :rules="[rules.required]"
              clearable
              class="required"
              :disabled="datastreamSelectionDisabled"
              @input="update('datastream',$event)"
            />
          </v-col>
          <v-col
            md="12"
            lg="6"
            xl="6"
          >
            <DateTimePicker
              :value="value.startDate"
              :min-date="dateToString(selectedDeviceActionPropertyCombination.action.beginDate)"
              :max-date="dateToString(selectedDeviceActionPropertyCombination.action.endDate)"
              label="Select begin date"
              hint="Start date"
              :required="true"
              :rules="[rules.required,...startDateExtraRules]"
              @input="update('startDate',$event)"
            />
          </v-col>
          <v-col
            md="12"
            lg="6"
            xl="6"
          >
            <DateTimePicker
              :value="value.endDate"
              :min-date="dateToString(selectedDeviceActionPropertyCombination.action.beginDate)"
              :max-date="dateToString(selectedDeviceActionPropertyCombination.action.endDate)"
              placeholder="Open End"
              label="Select end date"
              :rules="[...endDateExtraRules]"
              hint="Optional. Leave blank for open end"
              @input="update('endDate',$event)"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-form>
</template>
<script lang="ts">
import { Component, mixins, Prop, Vue } from 'nuxt-property-decorator'
import { mapGetters, mapState, mapActions } from 'vuex'
import DateTimePicker from '@/components/DateTimePicker.vue'
import Validator from '@/utils/validator'
import { Rules } from '@/mixins/Rules'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlThing } from '@/models/TsmdlThing'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmDeviceMountPropertyCombination } from '@/utils/configurationInterfaces'
import {
  ITsmLinkingState,
  LoadDatasourcesAction,
  LoadDatastreamsForDatasourceAndThingAction,
  LoadThingsForDatasourceAction, SuggestedDatasourceIdGetter,
  SuggestedThingIdGetter, SuggestedTsmEndpointIdGetter
} from '@/store/tsmLinking'
import { dateToString } from '@/utils/dateHelper'
import { TsmEndpoint } from '@/models/TsmEndpoint'

@Component({
  components: { DateTimePicker },
  computed: {
    ...mapState('tsmLinking', ['datastreams', 'datasources', 'things', 'linkings', 'tsmEndpoints']),
    ...mapGetters('tsmLinking', ['suggestedThingId', 'suggestedDatasourceId', 'suggestedTsmEndpointId'])
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
    type: Object
  })
  readonly selectedDeviceActionPropertyCombination!: TsmDeviceMountPropertyCombination

  private isLaodingDatasource = false
  private isLoadingThing = false
  private isLoadingDatastream = false

  // vuex definition for typescript check
  datasources!: ITsmLinkingState['datasources']
  things!: ITsmLinkingState['things']
  datastreams!: ITsmLinkingState['datastreams']
  tsmEndpoints!: ITsmLinkingState['tsmEndpoints']
  suggestedThingId!: SuggestedThingIdGetter
  suggestedDatasourceId!: SuggestedDatasourceIdGetter
  suggestedTsmEndpointId!: SuggestedTsmEndpointIdGetter
  loadDatasources!: LoadDatasourcesAction
  loadThingsForDatasource!: LoadThingsForDatasourceAction
  loadDatastreamsForDatasourceAndThing!: LoadDatastreamsForDatasourceAndThingAction

  get startDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.value.startDate, this.value.endDate),
      Validator.startDateMustBeAfterStartOfMountAction(this.value.startDate, this.selectedDeviceActionPropertyCombination.action)
    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.value.startDate, this.value.endDate),
      Validator.endDateMustBeBeforeEndOfMountAction(this.value.endDate, this.selectedDeviceActionPropertyCombination.action)
    ]
  }

  get suggestedThing (): TsmdlThing | null {
    const thingId = this.suggestedThingId(this.selectedDeviceActionPropertyCombination)
    if (thingId === null) {
      return null
    }
    return this.things.find(thing => thing.id === thingId) ?? null
  }

  get suggestedDatasource (): TsmdlDatasource | null {
    const datasourceId = this.suggestedDatasourceId(this.selectedDeviceActionPropertyCombination)
    if (datasourceId === null) {
      return null
    }
    return this.datasources.find(datasource => datasource.id === datasourceId) ?? null
  }

  get suggestedTsmEndpoint (): TsmEndpoint | null {
    const endpointId = this.suggestedTsmEndpointId(this.selectedDeviceActionPropertyCombination)
    if (endpointId === null) {
      return null
    }
    return this.tsmEndpoints.find(endpoint => endpoint.id === endpointId) ?? null
  }

  get datasourceSelectionDisabled (): boolean {
    return (!this.value.tsmEndpoint || !this.datasources)
  }

  get thingSelectionDisabled (): boolean {
    return (!this.value.datasource || !this.things)
  }

  get datastreamSelectionDisabled (): boolean {
    return (!this.value.thing || !this.datastreams)
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

  async update (key: string, result: any) {
    const newObj = TsmLinking.createFromObject(this.value)
    switch (key) {
      case 'endpoint':
        newObj.tsmEndpoint = result
        newObj.datasource = null
        newObj.thing = null
        newObj.datastream = null

        try {
          this.isLaodingDatasource = true
          await this.loadDatasources({ endpoint: result })
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Failed to load datasources')
        } finally {
          this.isLaodingDatasource = false
        }
        break
      case 'datasource':
        newObj.datasource = result
        newObj.thing = null
        newObj.datastream = null
        try {
          this.isLoadingThing = true
          await this.loadThingsForDatasource({
            endpoint: this.value.tsmEndpoint!,
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
        try {
          this.isLoadingDatastream = true
          await this.loadDatastreamsForDatasourceAndThing({
            endpoint: this.value.tsmEndpoint!,
            datasource: this.value.datasource!,
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
    }
    this.$emit('input', newObj)
  }

  public isValid (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>
