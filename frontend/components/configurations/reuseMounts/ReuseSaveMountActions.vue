<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-btn
    color="accent"
    @click="saveCopiedMountActions"
  >
    Save
  </v-btn>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import { mapActions } from 'vuex'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Contact } from '@/models/Contact'
import { AddDeviceMountActionAction, AddPlatformMountActionAction } from '@/store/configurations'
import { SetLoadingAction } from '@/store/progressindicator'

@Component(
  {
    methods: {
      ...mapActions('configurations', [
        'addDeviceMountAction',
        'addPlatformMountAction'
      ]),
      ...mapActions('progressindicator', ['setLoading'])
    }
  }
)
export default class ReuseSaveMountActions extends Vue {
  addDeviceMountAction!: AddDeviceMountActionAction
  addPlatformMountAction!: AddPlatformMountActionAction

  @Prop({
    required: true
  })
    value!: boolean

  @Prop({
    required: true
  })
    currentConfigurationId!: string

  @Prop({
    required: true,
    type: Object
  })
    selectedMountTree!: ConfigurationsTree

  @Prop({
    default: null,
    required: true,
    type: Object
  })
    beginDate!: DateTime

  @Prop({
    default: null,
    required: true
  })
    endDate!: DateTime | null

  // vuex
  private setLoading!: SetLoadingAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async saveCopiedMountActions () {
    // check if tree is available
    if (!this.selectedMountTree || !this.beginDate) {
      return
    }
    // create lists for new mount actions
    const { listOfNewPlatformMounts, listOfNewDeviceMounts } = this.createListsOfCopiedMountActionsInOrderToBeMounted()

    // Order does matter
    // platforms needs to be created first as they can be parents of other (device) mounts
    try {
      this.setLoading(true)
      await this.createNewPlatformActions(listOfNewPlatformMounts)
      await this.createNewDeviceActions(listOfNewDeviceMounts)

      this.$store.commit('snackbar/setSuccess', 'Save successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add new mount actions')
    } finally {
      // update v-model value
      this.$emit('input', true)

      this.setLoading(false)
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    }
  }

  createListsOfCopiedMountActionsInOrderToBeMounted () {
    const listOfNewDeviceMounts = []
    const listOfNewPlatformMounts = []

    for (const node of this.selectedMountTree.getAllNodesAsList()) {
      if (node.isPlatform()) {
        const platformMountAction = node.unpack() as PlatformMountAction
        const newPlatformMountAction = this.createCopyOfPlatformMountAction(platformMountAction)
        listOfNewPlatformMounts.push(newPlatformMountAction)
      }

      if (node.isDevice()) {
        const deviceMountAction = node.unpack() as DeviceMountAction
        const newDeviceMountAction = this.createCopyOfDeviceMountAction(deviceMountAction)

        listOfNewDeviceMounts.push(newDeviceMountAction)
      }
    }

    return { listOfNewPlatformMounts, listOfNewDeviceMounts }
  }

  private createCopyOfDeviceMountAction (action: DeviceMountAction) {
    const device = action.device
    const parentPlatform = action.parentPlatform
    const parentDevice = action.parentDevice

    return DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform,
      parentDevice,
      beginDate: this.beginDate,
      endDate: this.endDate,
      offsetX: action.offsetX,
      offsetY: action.offsetY,
      offsetZ: action.offsetZ,
      epsgCode: action.epsgCode,
      x: action.x,
      y: action.y,
      z: action.z,
      elevationDatumName: action.elevationDatumName,
      elevationDatumUri: action.elevationDatumUri,
      beginContact: action.beginContact,
      endContact: action.endContact ? action.endContact : null,
      beginDescription: action.beginDescription,
      endDescription: action.endDescription,
      label: action.label
    })
  }

  private createCopyOfPlatformMountAction (action: PlatformMountAction) {
    const parentPlatform = action.parentPlatform
    const platform = action.platform

    return PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform,
      beginDate: this.beginDate,
      endDate: this.endDate,
      offsetX: action.offsetX,
      offsetY: action.offsetY,
      offsetZ: action.offsetZ,
      epsgCode: action.epsgCode,
      x: action.x,
      y: action.y,
      z: action.z,
      elevationDatumName: action.elevationDatumName,
      elevationDatumUri: action.elevationDatumUri,
      beginContact: Contact.createFromObject(action.beginContact!),
      endContact: action.endContact ? Contact.createFromObject(action.endContact) : null,
      beginDescription: action.beginDescription,
      endDescription: action.endDescription,
      label: action.label
    })
  }

  private async createNewDeviceActions (list: DeviceMountAction[]) {
    if (!this.currentConfigurationId || !this.beginDate) {
      return
    }
    for (const item of list) {
      await this.addDeviceMountAction({
        configurationId: this.currentConfigurationId,
        deviceMountAction: item
      })
    }
  }

  private async createNewPlatformActions (list: PlatformMountAction[]) {
    if (!this.currentConfigurationId || !this.beginDate) {
      return
    }
    for (const item of list) {
      await this.addPlatformMountAction({
        configurationId: this.currentConfigurationId,
        platformMountAction: item
      })
    }
  }
}
</script>

<style scoped>

</style>
