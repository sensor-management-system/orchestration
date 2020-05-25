<template>
  <div>
    <v-autocomplete
      v-if="!readonly"
      :items="allPersonsExceptSelected"
      :item-text="(x) => x.name"
      :item-value="(x) => x.id"
      label="add a person"
      @change="addPerson"
    />
    <v-chip
      v-for="person in selectedPersons"
      :key="person.id"
      class="ma-2"
      color="indigo"
      text-color="white"
      :close="!readonly"
      @click:close="removePerson(person.id)"
    >
      <v-avatar left>
        <v-icon>mdi-account-circle</v-icon>
      </v-avatar>
      {{ person.name }}
    </v-chip>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select persons
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import Person from '../models/Person'
import PersonService from '../services/PersonService'

/**
 * A class component to select persons
 * @extends Vue
 */
@Component
// @ts-ignore
export default class PersonSelect extends Vue {
  private persons: Person[] = []
  private localSelectedPersons: Person[] = []

  @Prop({
    default: () => [] as Person[],
    required: true,
    type: Array
  })
  // @ts-ignore
  selectedPersons!: Person[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * copies the selectedPersons property to the local instance variable
   *
   * @constructor
   */
  constructor () {
    super()
    this.localSelectedPersons = this.selectedPersons
  }

  /**
   * fetches all available persons from the PersonsService
   *
   * @async
   */
  async fetch () {
    this.persons = await PersonService.findAllPersons()
  }

  /**
   * adds a person to the sensors responsiblePersons property
   *
   * @param {string} somePersonId - the id of the person to add
   */
  addPerson (somePersonId: string) {
    const selectedPerson: Person | undefined = this.persons.find(p => p.id === parseInt(somePersonId))
    if (selectedPerson) {
      this.localSelectedPersons.push(selectedPerson)
    }
  }

  /**
   * removes a person from the sensors responsiblePersons property
   *
   * @param {number} somePersonId - the id of the person to remove
   */
  removePerson (somePersonId: number) {
    const personIndex = this.localSelectedPersons.findIndex(p => p.id === somePersonId)
    this.localSelectedPersons.splice(personIndex, 1)
  }

  /**
   * returns all persons except the ones that have already been selected
   *
   * @return {Person[]} an array of persons
   */
  get allPersonsExceptSelected (): Person[] {
    return this.persons.filter(p => !this.localSelectedPersons.find(rp => rp.id === p.id))
  }

  /**
   * triggers an update event for the selectedPersons property
   *
   * @param {Person[]} selectedPersons - the changed persons array
   * @fires PersonSelect#update:selectedPersons
   */
  @Watch('localSelectedPersons', { immediate: true, deep: true })
  // @ts-ignore
  localSelectedPersonsChanged (selectedPersons: Person[]) {
    /**
     * Update event
     * @event PersonSelect#update:selectedPersons
     * @type Person[]
     */
    this.$emit('update:selectedPersons', selectedPersons)
  }
}
</script>
