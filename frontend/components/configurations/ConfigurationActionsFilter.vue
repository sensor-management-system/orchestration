<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
          :items="availableYearsOfActionsAndAlreadySelectedValues"
          clearable
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
          :items="availableContactsOfActionsAndAlreadySelectedValues"
          clearable
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
import { AvailableContactsOfActionsGetter, AvailableYearsOfActionsGetter, ConfigurationFilter } from '@/store/configurations'
import MultipleSelectionAbbrevation from '@/components/shared/MultipleSelectionAbbrevation.vue'

@Component({
  components: { MultipleSelectionAbbrevation },
  computed: {
    ...mapGetters('vocabulary', ['configurationActionTypeItemsIncludingMounts']),
    ...mapGetters('configurations', ['availableContactsOfActions', 'availableYearsOfActions'])
  }
})
export default class ConfigurationActionsFilter extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: ConfigurationFilter

  availableContactsOfActions!: AvailableContactsOfActionsGetter
  availableYearsOfActions!: AvailableYearsOfActionsGetter

  get selectedActionTypes (): IOptionsForActionType[] {
    return this.value.selectedActionTypes
  }

  set selectedActionTypes (newSelectedActionTypes: IOptionsForActionType[]) {
    const newFilter = {
      selectedActionTypes: newSelectedActionTypes,
      selectedYears: this.selectedYears,
      selectedContacts: this.selectedContacts
    }
    this.$emit('input', newFilter)
  }

  get selectedYears (): number[] {
    return this.value.selectedYears
  }

  set selectedYears (newSelectedYears: number[]) {
    const newFilter = {
      selectedActionTypes: this.selectedActionTypes,
      selectedYears: newSelectedYears,
      selectedContacts: this.selectedContacts
    }
    this.$emit('input', newFilter)
  }

  get selectedContacts (): string[] {
    return this.value.selectedContacts
  }

  set selectedContacts (newSelectedContacts: string[]) {
    const newFilter = {
      selectedActionTypes: this.selectedActionTypes,
      selectedYears: this.selectedYears,
      selectedContacts: newSelectedContacts
    }
    this.$emit('input', newFilter)
  }

  get availableYearsOfActionsAndAlreadySelectedValues (): number[] {
    const choicesBasedOnActions = this.availableYearsOfActions
    const alreadySelectedElementsThatAreNotPartOfActionChoices = this.selectedYears.filter(y => !choicesBasedOnActions.includes(y))
    return [...alreadySelectedElementsThatAreNotPartOfActionChoices, ...choicesBasedOnActions].sort((a, b) => (b - a))
  }

  get availableContactsOfActionsAndAlreadySelectedValues (): string[] {
    const choicesBasedOnActions = this.availableContactsOfActions
    const alreadySelectedElementsThatAreNotPartOfActionChoices = this.selectedContacts.filter(c => !choicesBasedOnActions.includes(c))
    return [...alreadySelectedElementsThatAreNotPartOfActionChoices, ...choicesBasedOnActions].sort()
  }
}
</script>

<style scoped>

</style>
