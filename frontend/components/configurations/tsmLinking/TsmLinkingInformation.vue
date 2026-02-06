<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <template
      v-for="(actionGroup, aIndex) in linkingsGroupedByAction"
    >
      <v-card
        :key="`title-${actionGroup.action.id}`"
        class="ma-2"
        elevation="1"
      >
        <v-card-title>
          <ExtendedItemName
            :value="actionGroup.action.device"
          />
        </v-card-title>

        <v-card-text>
          <template v-for="(linking, lIndex) in actionGroup.linkings">
            <TsmLinkingFormItem
              :id="linking.identifier"
              :key="linking.identifier"
              :ref="linking.identifier"
              v-model="linking.newLinking"
              class="mb-1"
              :devices="devices"
              :new-linkings="internalLinkings"
              :show-next-button="!(aIndex == linkingsGroupedByAction.length -1 && lIndex == actionGroup.linkings.length -1)"
              @input="update"
              @next="closeAndOpenNext(linking.identifier)"
            />
          </template>
        </v-card-text>
      </v-card>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import TsmLinkingFormItem from '@/components/configurations/tsmLinking/TsmLinkingFormItem.vue'
import { TsmLinking } from '@/models/TsmLinking'
import { Device } from '@/models/Device'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import TsmLinkingFormItemHeader from '@/components/configurations/tsmLinking/TsmLinkingFormItemHeader.vue'
import TsmLinkingForm from '@/components/configurations/tsmLinking/TsmLinkingForm.vue'

@Component({
  components: {
    TsmLinkingForm,
    TsmLinkingFormItemHeader,
    ExtendedItemName,
    TsmLinkingFormItem,
    BaseExpandableListItem
  }
})
export default class TsmLinkingInformation extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  readonly value!: TsmLinking[]

  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  // Create a local copy of the value that we'll manage
  private internalLinkings: TsmLinking[] = []

  created () {
    // Initialize the internal copy
    this.internalLinkings = this.value.map(item => TsmLinking.createFromObject(item))
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get formRefNames () {
    return this.internalLinkings.map(item => this.generateLinkingFormIdentifier(item))
  }

  get linkingsGroupedByAction (): {action: DeviceMountAction, linkings: {newLinking: TsmLinking, identifier: string}[]}[] {
    // Group by action directly
    const groups: Record<string, { action: any; linkings: { newLinking: TsmLinking, identifier: string }[] }> = {}

    this.internalLinkings.forEach((item) => {
      const actionId = item.deviceMountAction?.id || 'no-action'
      if (!groups[actionId]) {
        groups[actionId] = {
          action: item.deviceMountAction,
          linkings: []
        }
      }
      groups[actionId].linkings.push({ newLinking: item, identifier: this.generateLinkingFormIdentifier(item) })
    })

    return Object.values(groups)
  }

  generateLinkingFormIdentifier (newLinking: TsmLinking) {
    return `linking-form-item-${newLinking.deviceMountAction!.id}-${newLinking.deviceProperty!.id}`
  }

  update (linking: TsmLinking) {
    // Find and update the linking in our internal array
    const index = this.internalLinkings.findIndex(l =>
      l.deviceMountAction?.id === linking.deviceMountAction?.id &&
      l.deviceProperty?.id === linking.deviceProperty?.id
    )

    if (index !== -1) {
      this.internalLinkings.splice(index, 1, linking)
      this.$emit('input', [...this.internalLinkings]) // Emit a new array reference
    }
  }

  async closeAndOpenNext (refName: string) {
    const index = this.formRefNames.indexOf(refName)
    if (index === -1) { return }

    const nextRefName = this.formRefNames[index + 1]
    if (!nextRefName) { return }

    await this.closeAndOpenTarget(nextRefName)
  }

  public async closeAndOpenTarget (targetRefName: string) {
    const targetIndex = this.formRefNames.indexOf(targetRefName)
    if (targetIndex === -1) { return }

    // close all others
    this.formRefNames.forEach((refName) => {
      if (refName !== targetRefName) {
        this.getFormRef(refName)?.close()
      }
    })

    // open target
    const targetRef = this.getFormRef(targetRefName)
    targetRef?.open()

    await this.$nextTick()

    this.$vuetify.goTo(
      `#${targetRefName}`,
      {
        offset: 850
      }
    )
  }

  getFormRef (refName: string): TsmLinkingFormItem | undefined {
    const ref = this.$refs[refName] as unknown
    if (Array.isArray(ref)) {
      return ref[0] as TsmLinkingFormItem
    }
    return ref as TsmLinkingFormItem
  }

  public validateForm (): boolean {
    const formsArray = this.formRefNames.map(refName => this.getFormRef(refName)) as TsmLinkingFormItem[]
    return formsArray.every(el => el.validateForm())
  }

  // Watch for external changes to the value prop
  @Watch('value', { deep: true })
  onValueChanged (newValue: TsmLinking[]) {
    this.internalLinkings = newValue.map(item => TsmLinking.createFromObject(item))
  }
}
</script>

<style scoped>
</style>
