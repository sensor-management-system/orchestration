<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
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
      <v-col cols="12" md="6">
        <visibility-switch
          :value="value.visibility"
          :disabled-options="[visibilityPrivateValue]"
          :readonly="readonly"
          :entity-name="entityName"
          @input="update('visibility', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <permission-group-select
          :value="value.permissionGroup"
          :readonly="readonly"
          :entity-name="entityName"
          :multiple="false"
          :rules="[rules.validatePermissionGroup]"
          required
          label="Permission group"
          @input="update('permissionGroup', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.label"
          :rules="[rules.labelProvided]"
          label="Label"
          :readonly="readonly"
          class="required"
          @input="update('label',$event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          :value="value.status"
          :items="configurationStates"
          label="Status"
          :readonly="readonly"
          @input="update('status',$event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          :item-value="(x) => x.id"
          :item-text="(x) => x.label"
          :items="sites"
          label="Site"
          :readonly="readonly"
          @input="update('siteId',$event)"
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

import { mapActions, mapState } from 'vuex'

import { Configuration } from '@/models/Configuration'
import { Visibility } from '@/models/Visibility'

import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'
import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'
import { SearchSitesAction, SitesState } from '@/store/sites'

@Component({
  components: {
    VisibilitySwitch,
    PermissionGroupSelect,
    DateTimePicker
  },
  computed: {
    ...mapState('configurations', ['configurationStates']),
    ...mapState('sites', ['sites'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfigurationsStates']),
    ...mapActions('sites', ['searchSites'])
  }
})
export default class ConfigurationsBasicDataForm extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

  private entityName: string = 'configuration'

  // vuex definition for typescript check
  loadConfigurationsStates!: () => void
  sites!: SitesState['sites']
  searchSites!: SearchSitesAction

  async created () {
    try {
      await this.loadConfigurationsStates()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load configuration states')
    }
    try {
      await this.searchSites()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load sites')
    }
  }

  get configurationStates () {
    return this.$store.state.configurations.configurationStates
  }

  update (
    key: keyof Pick<Configuration, 'visibility' | 'permissionGroup' | 'label' | 'status' | 'startDate' | 'endDate' | 'siteId'>,
    value: any
  ) {
    if (key in this.value) {
      const newObj = Configuration.createFromObject(this.value)
      newObj[key] = value
      this.$emit('input', newObj)
    }
  }

  get rules (): Object {
    return {
      startDate: Validator.validateInputForStartDate(this.value),
      endDate: Validator.validateInputForEndDate(this.value),
      labelProvided: Validator.mustBeProvided('label'),
      validatePermissionGroup: Validator.validatePermissionGroup(false)
    }
  }

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }

  get visibilityPrivateValue (): Visibility {
    return Visibility.Private
  }
}
</script>

<style lang="scss">
@import '@/assets/styles/_forms.scss';
</style>
