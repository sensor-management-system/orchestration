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
          <DevicePropertyForm v-model="value[index]" :readonly="readonly" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for collections of DevicePropertyForms
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '../models/DeviceProperty'

// @ts-ignore
import DevicePropertyForm from './DevicePropertyForm.vue'

/**
 * A class component that lists DevicePropertyForms as ExpansionPanels
 * @extends Vue
 */
@Component({
  components: { DevicePropertyForm }
})
// @ts-ignore
export default class DevicePropertyExpansionPanels extends Vue {
  @Prop({
    default: () => [] as DeviceProperty[],
    required: true,
    type: Array
  })
  // @ts-ignore
  value!: DeviceProperty[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * adds a new DeviceProperty instance
   *
   * @fires DevicePropertyExpansionPanels#input
   */
  addProperty () {
    /**
     * Update event
     * @event DevicePropertyExpansionPanels#input
     * @type DeviceProperty[]
     */
    this.$emit('input', [
      ...this.value,
      new DeviceProperty()
    ] as DeviceProperty[])
  }

  /**
   * removes a DeviceProperty instance
   *
   * @param {DeviceProperty} index - the index of the property to remove
   * @fires DevicePropertyExpansionPanels#input
   */
  removeProperty (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as DeviceProperty[]
      properties.splice(index, 1)
      /**
      * Update event
      * @event DevicePropertyExpansionPanels#input
      * @type DeviceProperty[]
      */
      this.$emit('input', properties)
    }
  }

  /**
   * copies a DevicceProperty instance
   *
   * @param {DeviceProperty} index - the index of the property to copy
   * @fires DevicePropertyExpansionPanels#input
   */
  copyProperty (index: number) {
    if (this.value[index]) {
      const newProperty = DeviceProperty.createFromObject(this.value[index])
      newProperty.label += ' (copy)'

      /**
       * Update event
       * @event DevicePropertyExpansionPanels#input
       * @type DeviceProperty[]
       */
      this.$emit('input', [
        ...this.value,
        newProperty
      ] as DeviceProperty[])
    }
  }
}
</script>
