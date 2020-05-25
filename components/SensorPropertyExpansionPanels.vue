<template>
  <div>
    <v-btn
      v-if="!readonly"
      small
      color="primary"
      data-role="add-property"
      @click="addProperty"
    >
      add Property
    </v-btn>
    <br><br>
    <v-expansion-panels
      multiple
    >
      <v-expansion-panel
        v-for="(item, index) in value"
        :key="index"
      >
        <v-expansion-panel-header>
          <v-row no-gutters>
            <v-col cols="11">
              Property {{ index+1 }} {{ item.label ? ' - ' + item.label : '' }}
            </v-col>
            <v-col cols="1">
              <v-menu
                v-if="!readonly"
                right
                offset-y
              >
                <template v-slot:activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    v-on="on"
                  >
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-item
                    data-role="copy-property"
                    @click="copyProperty(index)"
                  >
                    <v-list-item-title>Copy</v-list-item-title>
                  </v-list-item>
                  <v-list-item
                    data-role="delete-property"
                    @click="removeProperty(index)"
                  >
                    <v-list-item-title>Delete</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <SensorPropertyForm v-model="value[index]" :readonly="readonly" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for collections of SensorPropertyForms
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { SensorProperty } from '../models/SensorProperty'

// @ts-ignore
import SensorPropertyForm from './SensorPropertyForm.vue'

/**
 * A class component that lists SensorPropertyForms as ExpansionPanels
 * @extends Vue
 */
@Component({
  components: { SensorPropertyForm }
})
// @ts-ignore
export default class SensorPropertyExpansionPanels extends Vue {
  @Prop({
    default: () => [] as SensorProperty[],
    required: true,
    type: Array
  })
  // @ts-ignore
  value!: SensorProperty[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * adds a new SensorProperty instance
   *
   * @fires SensorPropertyExpansionPanels#input
   */
  addProperty () {
    /**
     * Update event
     * @event SensorPropertyExpansionPanels#input
     * @type SensorProperty[]
     */
    this.$emit('input', [
      ...this.value,
      new SensorProperty()
    ] as SensorProperty[])
  }

  /**
   * removes a SensorProperty instance
   *
   * @param {SensorProperty} index - the index of the property to remove
   * @fires SensorPropertyExpansionPanels#input
   */
  removeProperty (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as SensorProperty[]
      properties.splice(index, 1)
      /**
      * Update event
      * @event SensorPropertyExpansionPanels#input
      * @type SensorProperty[]
      */
      this.$emit('input', properties)
    }
  }

  /**
   * copies a SensorProperty instance
   *
   * @param {SensorProperty} index - the index of the property to copy
   * @fires SensorPropertyExpansionPanels#input
   */
  copyProperty (index: number) {
    if (this.value[index]) {
      const newProperty = SensorProperty.createFromObject(this.value[index])
      newProperty.label += ' (copy)'

      /**
       * Update event
       * @event SensorPropertyExpansionPanels#input
       * @type SensorProperty[]
       */
      this.$emit('input', [
        ...this.value,
        newProperty
      ] as SensorProperty[])
    }
  }
}
</script>
