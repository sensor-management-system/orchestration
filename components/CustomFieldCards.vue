<template>
  <v-form ref="customFieldsForm">
    <v-btn
      v-if="!readonly"
      small
      color="primary"
      data-role="add-field"
      @click="addField"
    >
      add Custom Field
    </v-btn>
    <br><br>
    <template
      v-for="(item, index) in value"
    >
      <v-card
        :key="'customfield-' + index"
      >
        <v-card-text>
          <CustomFieldForm
            v-model="value[index]"
            :readonly="readonly"
          >
            <template v-slot:actions>
              <v-btn
                v-if="!readonly"
                icon
                color="error"
                data-role="delete-field"
                @click="removeField(index)"
              >
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </template>
          </CustomFieldForm>
        </v-card-text>
      </v-card>
      <br
        :key="'br-' + index"
      >
    </template>
  </v-form>
</template>

<script lang="ts">
/**
 * @file provides a component for collections of CustomFieldForms
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import CustomFieldForm from '@/components/CustomFieldForm.vue'

import { CustomTextField } from '@/models/CustomTextField'

/**
 * A class component that lists CustomFieldForms as Cards
 * @extends Vue
 */
@Component({
  components: { CustomFieldForm }
})
// @ts-ignore
export default class CustomFieldCards extends Vue {
  @Prop({
    default: () => [] as CustomTextField[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: CustomTextField[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * adds a new CustomTextField instance
   *
   * @fires CustomFieldCards#input
   */
  addField () {
    /**
     * Update event
     * @event CustomFieldCards#input
     * @type CustomTextField[]
     */
    this.$emit('input', [
      ...this.value,
      new CustomTextField()
    ] as CustomTextField[])
  }

  /**
   * removes a CustomTextField instance
   *
   * @param {CustomTextField} index - the index of the property to remove
   * @fires CustomFieldCards#input
   */
  removeField (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as CustomTextField[]
      properties.splice(index, 1)
      /**
      * Update event
      * @event CustomFieldCards#input
      * @type CustomTextField[]
      */
      this.$emit('input', properties)
    }
  }
}
</script>
