<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-timeline dense>
    <v-timeline-item
      v-for="(action, index) in value"
      :key="index"
      :color="action.color"
      :icon="action.icon"
      class="mb-4"
    >
      <slot v-if="action.isGenericAction" name="generic-action" :action="action" :index="index" />
      <slot v-if="action.isSoftwareUpdateAction" name="software-update-action" :action="action" :index="index" />
      <slot v-if="action.isDeviceCalibrationAction" name="calibration-action" :action="action" :index="index" />
      <slot v-if="action.isDeviceMountAction" name="device-mount-action" :action="action.inner" :index="index" />
      <slot v-if="action.isDeviceUnmountAction" name="device-unmount-action" :action="action.inner" :index="index" />
      <slot v-if="action.isParameterChangeAction" name="parameter-change-action" :action="action" :index="index" />
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'

/**
 * A component to display Device related actions in a timeline
 *
 * The component offers the following properties:
 *
 * * value - an Array of actions
 *
 * @augments Vue
 */
@Component({})
export default class DeviceActionTimeline extends Vue {
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly value!: IActionCommonDetails[]
}
</script>
