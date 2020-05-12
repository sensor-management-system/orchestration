<template>
  <div>
    <v-autocomplete
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
      :close="true"
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import Person from '../models/Person'
import PersonService from '../services/PersonService'

@Component
export default class PersonSelect extends Vue {
  private persons: Person[] = []

  @Prop()
  selectedPersons: Person[]

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
      this.selectedPersons.push(selectedPerson)
    }
  }

  /**
   * removes a person from the sensors responsiblePersons property
   *
   * @param {number} somePersonId - the id of the person to remove
   */
  removePerson (somePersonId: number) {
    const personIndex = this.selectedPersons.findIndex(p => p.id === somePersonId)
    this.selectedPersons.splice(personIndex, 1)
  }

  /**
   * returns all persons except the ones that have already been selected
   *
   * @return {Person[]} an array of persons
   */
  get allPersonsExceptSelected (): Person[] {
    return this.persons.filter(p => !this.selectedPersons.find(rp => rp.id === p.id))
  }

}
</script>
