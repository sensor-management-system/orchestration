<template>
  <div>
    <v-autocomplete
      v-if="!readonly"
      :items="allManufacturersExceptSelected"
      :item-text="(x) => x"
      :item-value="(x) => x.id"
      label="Add a manufacturer"
      @change="addManufacturer"
    />
    <v-chip
      v-for="manufacturer in selectedManufacturers"
      :key="manufacturer.id"
      class="ma-2"
      color="brown"
      text-color="white"
      :close="!readonly"
      @click:close="removeManufacturer(manufacturer.id)"
    >
      {{ manufacturer }}
    </v-chip>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select manufacturers
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import Manufacturer from '../models/Manufacturer'
import CVService from '../services/CVService'

/**
 * A class component to select manufacturers
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ManufacturerSelect extends Vue {
  private manufacturers: Manufacturer[] = []
  private currentlySelectedManufacturer: Manufacturer | null = null

  @Prop({
    default: () => [] as Manufacturer[],
    required: true,
    type: Array
  })
  // @ts-ignore
  selectedManufacturers!: Manufacturer[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * fetches all available manufacturers from the CVService
   *
   * @async
   */
  async fetch () {
    this.manufacturers = await CVService.findAllManufacturers()
  }

  /**
   * adds a manufacturer to the manufacturers property
   *
   * @param {string} someManufacturerId - the id of the manufacturer to add
   * @fires ManufacturerSelect#update:selectedManufacturers
   */
  addManufacturer (someManufacturerId: string) {
    const selectedManufacturer: Manufacturer | undefined = this.manufacturers.find(m => m.id === parseInt(someManufacturerId))
    this.currentlySelectedManufacturer = null
    if (selectedManufacturer) {
      /**
       * Update event
       * @event ManufacturerSelect#update:selectedManufacturers
       * @type Manufacturer[]
       */
      this.$emit('update:selectedManufacturers', [
        ...this.selectedManufacturers,
        selectedManufacturer
      ] as Manufacturer[])
    }
  }

  /**
   * removes a manufacturer from the manufacturers property
   *
   * @param {number} someManufacturerId - the id of the manufacturer to remove
   * @fires ManufacturerSelect#update:selectedManufacturers
   */
  removeManufacturer (someManufacturerId: number) {
    const manufacturerIndex: number = this.selectedManufacturers.findIndex(m => m.id === someManufacturerId)
    if (manufacturerIndex > -1) {
      /**
       * Update event
       * @event ManufacturerSelect#update:selectedManufacturers
       * @type Manufacturer[]
       */
      const selectedManufacturers = [...this.selectedManufacturers] as Manufacturer[]
      selectedManufacturers.splice(manufacturerIndex, 1)
      this.$emit('update:selectedManufacturers', selectedManufacturers)
    }
  }

  /**
   * returns all manufacturers except the ones that have already been selected
   *
   * @return {Manufacturer[]} an array of manufacturers
   */
  get allManufacturersExceptSelected (): Manufacturer[] {
    return this.manufacturers.filter(m => !this.selectedManufacturers.find(rm => rm.id === m.id))
  }
}
</script>
