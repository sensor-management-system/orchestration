<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  </v-form>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { mapActions, mapState, mapGetters } from 'vuex'
import { Configuration } from '@/models/Configuration'

import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'

@Component({
  components: {
    DateTimePicker
  },
  computed: {
    ...mapState('configurations', ['configurationStates']),
    ...mapGetters('configurations', ['projectNames'])
  },
  methods: mapActions('configurations', ['loadConfigurationsStates', 'loadProjects'])
})
export default class ConfigurationsBasicDataForm extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

  readonly LOCATION_TYPE_STATIONARY = 'Stationary'
  readonly LOCATION_TYPE_DYNAMIC = 'Dynamic'

  // vuex definition for typescript check
  loadConfigurationsStates!: ()=> void;
  loadProjects!: ()=> void;

  async created () {
    await this.loadConfigurationsStates()
    await this.loadProjects()
  }

  get configurationStates () { return this.$store.state.configurations.configurationStates }
  get projectNames () { return this.$store.getters['configurations/projectNames'] }
  // @ts-ignore
  update (key: string, value: any) {
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

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style scoped>

</style>
