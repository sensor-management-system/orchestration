<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <v-container>
    <v-row>
      <v-col>
        <v-select
          v-model="selectedActionTypes"
          multiple
          label="Action type filter"
          hint="Please select an action type"
          :items="configurationActionTypeItemsIncludingMounts"
          :item-text="(x) => x.name"
          return-object
          clearable
          @input="update"
        >
          <template #selection="{ item, index }">
            <MultipleSelectionAbbrevation :index="index" :item-text="item.name" :selection="selectedActionTypes" />
          </template>
        </v-select>
      </v-col>
      <v-col>
        <v-select
          v-model="selectedYears"
          multiple
          label="Year filter"
          hint="Please select a year"
          :items="availableYearsOfActions"
          clearable
          @input="update"
        >
          <template #selection="{ item, index }">
            <MultipleSelectionAbbrevation :index="index" :item-text="item.toString()" :selection="selectedYears" />
          </template>
        </v-select>
      </v-col>
      <v-col>
        <v-select
          v-model="selectedContacts"
          multiple
          label="Contact filter"
          hint="Please select a contact"
          :items="availableContactsOfActions"
          clearable
          @input="update"
        >
          <template #selection="{ item, index }">
            <MultipleSelectionAbbrevation :index="index" :item-text="item" :selection="selectedContacts" />
          </template>
        </v-select>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'
import { IOptionsForActionType } from '@/store/devices'
import { ConfigurationFilter } from '@/store/configurations'
import MultipleSelectionAbbrevation from '@/components/shared/MultipleSelectionAbbrevation.vue'

@Component({
  components: { MultipleSelectionAbbrevation },
  computed: {
    ...mapGetters('vocabulary', ['configurationActionTypeItemsIncludingMounts']),
    ...mapGetters('configurations', ['availableContactsOfActions', 'availableYearsOfActions'])
  }
})
export default class ConfigurationActionsFilter extends Vue {
  private selectedActionTypes: IOptionsForActionType[] = []
  private selectedYears: number[] = []
  private selectedContacts: string [] = []

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: ConfigurationFilter

  get filter () {
    return {
      selectedActionTypes: this.selectedActionTypes,
      selectedYears: this.selectedYears,
      selectedContacts: this.selectedContacts
    }
  }

  update () {
    this.$emit('input', this.filter)
  }
}
</script>

<style scoped>

</style>
