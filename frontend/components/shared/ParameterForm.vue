<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      ref="parameterForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <autocomplete-text-input
            ref="label"
            label="Label"
            :value="value.label"
            :readonly="readonly"
            :disabled="readonly"
            class="required"
            :rules="[rules.required]"
            :endpoint="autoCompletionEndpoint"
            @input="update('label', $event)"
          />
        </v-col>
        <v-col cols="12" md="3">
          <combobox
            label="Unit"
            clearable
            :items="unitItems"
            item-text="name"
            :value="valueUnitItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateUnit"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueUnitItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valueUnitItem.definition }}</span>
              </v-tooltip>
              <a v-if="valueUnitItem && valueUnitItem.uri" target="_blank" :href="valueUnitItem.uri" style="line-height: 2;">
                <v-icon small>
                  mdi-open-in-new
                </v-icon>
              </a>
              <v-btn icon @click="showNewUnitDialog = true">
                <v-icon>
                  mdi-tooltip-plus-outline
                </v-icon>
              </v-btn>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </combobox>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="9">
          <v-textarea
            :value="value.description"
            :readonly="readonly"
            :disabled="readonly"
            label="Description"
            rows="3"
            @input="update('description', $event)"
          />
        </v-col>
      </v-row>
    </v-form>
    <unit-dialog
      v-model="showNewUnitDialog"
      @aftersubmit="updateUnit"
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component that renders a form for a parameter
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import Combobox from '@/components/shared/Combobox.vue'
import CvPropertyDialog from '@/components/devices/CvPropertyDialog.vue'
import UnitDialog from '@/components/devices/UnitDialog.vue'

import { Rules } from '@/mixins/Rules'

import { ICvSelectItem, hasDefinition } from '@/models/CvSelectItem'
import { Parameter } from '@/models/Parameter'
import { Unit } from '@/models/Unit'

type CvDictKeys = 'units'
type CvDictTypes = Unit
type UnitComboboxValue = Unit | string | undefined
type AutoCompletionEndpoint = 'device-parameter-labels' | 'platform-parameter-labels' | 'configuration-parameter-labels'

/**
 * A class component that renders a form for a device property
 * @extends Vue
 */
@Component({
  components: {
    AutocompleteTextInput,
    Combobox,
    CvPropertyDialog,
    UnitDialog
  }
})
export default class ParameterForm extends mixins(Rules) {
  private showNewUnitDialog = false

  /**
   * a Parameter
   */
  @Prop({
    default: () => new Parameter(),
    required: true,
    type: Parameter
  })
  readonly value!: Parameter

  @Prop({
    type: String,
    required: true
  })
  readonly autoCompletionEndpoint!: AutoCompletionEndpoint

  /**
   * a list of Units
   */
  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  readonly units!: Unit[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  readonly readonly!: boolean

  /**
   * returns the URI of an value
   *
   * @param {CvDictKeys} key - the name of the dictionary to look in
   * @param {string|null} value - the value to look for
   * @returns {string} the URI of the found object or an empty string
   */
  private getUriByValue (key: CvDictKeys, value: string | null): string {
    return this.getCvObjectByValue(key, value)?.uri || ''
  }

  /**
   * returns the object of an value
   *
   * @param {CvDictKeys} key - the name of the dictionary to look in
   * @param {string | null} value - the value to look for
   * @returns {CvDictTypes | null} the found object or null
   */
  private getCvObjectByValue (key: CvDictKeys, value: string | null): CvDictTypes | null {
    if (!(key in this)) {
      return null
    }
    if (value === null) {
      value = ''
    }
    const index = this[key].findIndex((x: CvDictTypes) => x.name === value)
    if (index === -1) {
      return null
    }
    return this[key][index]
  }

  /**
   * updates the unit
   *
   * @param {UnitComboboxValue} value - an object as provided by the combobox
   * @fires ParameterForm#input
   */
  updateUnit (value: UnitComboboxValue): void {
    const newObj: Parameter = Parameter.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.unitName = value
        newObj.unitUri = this.getUriByValue('units', value)
      } else {
        newObj.unitName = value.name
        newObj.unitUri = value.uri
      }
    } else {
      newObj.unitName = ''
      newObj.unitUri = ''
    }
    /**
     * input event
     * @event ParameterForm#input
     * @type {Parameter}
     */
    this.$emit('input', newObj)
  }

  /**
   * update a copy of the internal model at a given key and trigger an event
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires ParameterForm#input
   */
  update (key: string, value: string) {
    const newObj: Parameter = Parameter.createFromObject(this.value)

    switch (key) {
      case 'label':
        newObj.label = value
        break
      case 'description':
        newObj.description = value
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event ParameterForm#input
     * @type {Parameter}
     */
    this.$emit('input', newObj)
  }

  /**
   * returns a list of unit objects
   *
   * @returns {Unit[]} list of units
   */
  get unitItems (): Unit[] {
  // restrict the list of measuredQuantityUnits based on the choosen property
    return this.units
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.unitName and value.unitUri can be found in the list
   * of CV units. Returns the found unit, otherwise constructs one from the
   * name and the uri. Returns null if both fields are empty.
   *
   * @returns {ICvSelectItem|null} the unit, a constructed one or null
   */
  get valueUnitItem (): ICvSelectItem | null {
    if (!this.value.unitName && !this.value.unitUri) {
      return null
    }
    const unit = this.units.find(u => u.uri === this.value.unitUri)
    if (unit) {
      return unit
    }
    return {
      name: this.value.unitName,
      uri: this.value.unitUri,
      definition: '',
      id: null
    }
  }

  /**
   * checks wheter the item has a non-empty definition property
   *
   * @param {ICvSelectItem} item - the item to check for
   * @returns {boolean} returns true when the definition property exists and is not falsy
   */
  itemHasDefinition (item: ICvSelectItem): boolean {
    return hasDefinition(item)
  }

  focus (): void {
    (this.$refs.label as Vue & { focus: () => void }).focus()
  }

  /**
   * validates the user input
   *
   * Note: we can't use 'validate' as a method name, so I used 'validateForm'
   *
   * @return {boolean} true when input is valid, otherwise false
   */
  public validateForm (): boolean {
    return (this.$refs.parameterForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
