<template>
  <v-row>
    <v-col cols="12" md="3">
      <v-text-field
        label="key"
        :value="value.key"
        :readonly="readonly"
        :disabled="readonly"
        @input="update('key', $event)"
      />
    </v-col>
    <v-col cols="12" md="3">
      <v-text-field
        label="value"
        :value="value.value"
        :readonly="readonly"
        :disabled="readonly"
        @input="update('value', $event)"
      />
    </v-col>
    <v-col cols="12" md="3">
      <slot name="actions" />
    </v-col>
  </v-row>
</template>

<script lang="ts">
/**
 * @file provides a component for a custom field
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { CustomTextField } from '../models/CustomTextField'

/**
 * A class component for a custom field
 * @extends Vue
 */
@Component
// @ts-ignore
export default class CustomFieldForm extends Vue {
  @Prop({
    default: () => new CustomTextField(),
    required: true,
    type: CustomTextField
  })
  // @ts-ignore
  value!: CustomTextField

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  /**
   * update the internal model at a given key
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires CustomFieldForm#input
   */
  update (key: string, value: string) {
    const newObj: CustomTextField = CustomTextField.createFromObject(this.value)
    newObj.setPath(key, value)

    /**
     * input event
     * @event CustomTextFieldForm#input
     * @type CustomTextField
     */
    this.$emit('input', newObj)
  }
}
</script>
