<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-expansion-panels v-model="expansionPanelOpen">
    <v-expansion-panel>
      <v-expansion-panel-header>
        <TsmLinkingFormItemHeader
          :selected-device-action="value.deviceMountAction"
          :selected-measured-quantity="value.deviceProperty"
        />
        <v-icon v-if="formIsValid" class="formValidationIcon">
          mdi-check
        </v-icon>
        <v-icon v-else-if="formWasClosed" color="red" class="formValidationIcon">
          mdi-alert
        </v-icon>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <TsmLinkingForm
          ref="tsmLinkingFormItemForm"
          v-model="copyValue"
          :devices="devices"
          :new-linkings="newLinkings"
          @input="update"
        />
        <v-btn v-if="showNextButton" class="primary ma-3" :disabled="!formIsValid" @click="next">
          Next
        </v-btn>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import TsmLinkingForm from '@/components/configurations/tsmLinking/TsmLinkingForm.vue'
import { TsmLinking } from '@/models/TsmLinking'
import TsmLinkingFormItemHeader from '@/components/configurations/tsmLinking/TsmLinkingFormItemHeader.vue'
import { Device } from '@/models/Device'

@Component({
  components: { TsmLinkingFormItemHeader, TsmLinkingForm }
})
export default class TsmLinkingFormItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: TsmLinking

  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  @Prop({
    required: true,
    type: Array
  })
  private newLinkings!: TsmLinking[]

  @Prop({
    default: true
  })
  private showNextButton!: boolean

  private copyValue: TsmLinking = TsmLinking.createFromObject(this.value)

  private formWasClosed = false

  private expansionPanelOpen: number | undefined = -1

  get formIsValid (): boolean {
    if (!this.copyValue) { return false }
    if (this.copyValue.tsmEndpoint && this.copyValue.datasource && this.copyValue.thing && this.copyValue.datastream) {
      return this.validateForm()
    }
    return false
  }

  update (linking: TsmLinking) {
    this.$emit('input', linking)
  }

  next () {
    this.$emit('next')
    this.validateForm()
  }

  public validateForm (): boolean {
    if (!this.$refs.tsmLinkingFormItemForm) {
      return false
    }

    return (this.$refs.tsmLinkingFormItemForm as Vue & { validateForm: () => boolean }).validateForm()
  }

  public open () {
    this.expansionPanelOpen = 0
  }

  public close () {
    this.expansionPanelOpen = undefined
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChanged (newValue: TsmLinking) {
    this.copyValue = TsmLinking.createFromObject(newValue)
  }

  @Watch('expansionPanelOpen')
  onExpansionPanelOpen (_newValue: number | undefined, _oldValue: number | undefined) {
    // a transition from oldValue: 0 to newValue: undefined means that the expansion panel was closed
    if (_oldValue === 0 && _newValue === undefined) {
      this.formWasClosed = true
    }
  }
}
</script>

<style scoped>
.formValidationIcon {
  position: absolute;
  right: 1em;
  top: 1em;
}
</style>
