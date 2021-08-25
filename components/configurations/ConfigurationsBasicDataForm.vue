<template>
  <v-form
    ref="basicDataForm"
    @submit.prevent
  >
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.label"
          :rules="[rules.labelProvided]"
          label="Label"
          :readonly="readonly"
          @input="update('label',$event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="value.status"
          :items="configurationStates"
          label="Status"
          :readonly="readonly"
          @input="update('status',$event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="value.projectName"
          :items="projectNames"
          label="Project"
          :readonly="readonly"
          @input="update('projectName',$event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <date-time-picker
          :value="value.startDate"
          label="Start date"
          placeholder="e.g. 2000-01-31 12:00"
          :rules="[rules.startDate]"
          :readonly="readonly"
          @input="update('startDate',$event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <date-time-picker
          :value="value.endDate"
          label="End date"
          placeholder="e.g. 2001-01-31 12:00"
          :rules="[rules.endDate]"
          :readonly="readonly"
          @input="update('endDate',$event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          v-model="locationType"
          label="Location type"
          :items="[LOCATION_TYPE_STATIONARY, LOCATION_TYPE_DYNAMIC]"
          :readonly="readonly"
          clearable
        />
      </v-col>
    </v-row>
    <div v-if="locationType === LOCATION_TYPE_STATIONARY">
      <stationary-location-row
        :configuration="value"
        :readonly="readonly"
      />
      <v-row>
        <v-col cols="12" md="6">
          <location-map
            v-model="value.location"
            :readonly="readonly"
          />
        </v-col>
      </v-row>
    </div>
    <div v-if="locationType === LOCATION_TYPE_DYNAMIC">
      <dynamic-location-row
        :configuration="value"
        :readonly="readonly"
        @input="$emit('input', $event)"
      />
    </div>
  </v-form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'
import { DynamicLocation, LocationType, StationaryLocation } from '@/models/Location'

import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'
import StationaryLocationRow from '@/components/configurations/StationaryLocationRow.vue'
import LocationMap from '@/components/configurations/LocationMap.vue'
import DynamicLocationRow from '@/components/configurations/DynamicLocationRow.vue'

@Component({
  components: {
    DynamicLocationRow,
    LocationMap,
    StationaryLocationRow,
    DateTimePicker
  }
})
export default class ConfigurationsBasicDataForm extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!:Configuration

  readonly LOCATION_TYPE_STATIONARY = 'Stationary'
  readonly LOCATION_TYPE_DYNAMIC = 'Dynamic'

  async mounted () {
    await Promise.all([
      this.$store.dispatch('configurations/loadProjects'),
      this.$store.dispatch('configurations/loadConfigurationsStates')
    ])
  }

  get configurationStates () { return this.$store.state.configurations.configurationStates }
  get projectNames () { return this.$store.getters['configurations/projectNames'] }
  // @ts-ignore
  update (key:string, value:any) {
    // @ts-ignore
    if (typeof this.value[key] !== 'undefined') {
      const newObj = Configuration.createFromObject(this.value)
      // @ts-ignore
      newObj[key] = value
      this.$emit('input', newObj)
    }
  }

  get rules (): Object {
    return {
      startDate: Validator.validateInputForStartDate(this.value),
      endDate: Validator.validateInputForEndDate(this.value),
      labelProvided: Validator.mustBeProvided('label')
    }
  }

  get locationType (): string | null {
    switch (true) {
      case (this.value.location instanceof StationaryLocation):
        return LocationType.Stationary
      case (this.value.location instanceof DynamicLocation):
        return LocationType.Dynamic
      default:
        return null
    }
  }

  set locationType (locationType: string | null) {
    switch (locationType) {
      case LocationType.Stationary:
        if (!(this.value.location instanceof StationaryLocation)) {
          this.value.location = new StationaryLocation()
        }
        break
      case LocationType.Dynamic:
        if (!(this.value.location instanceof DynamicLocation)) {
          this.value.location = new DynamicLocation()
        }
        break
      default:
        this.value.location = null
    }
  }

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style scoped>

</style>
