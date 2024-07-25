<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="primary white--text">
          Mounted devices and platforms
        </v-card-title>
        <v-card-text>
          <ConfigurationsTreeView
            v-if="tree.length > 0"
            ref="treeView"
            :value="selectedNode"
            :tree="tree"
            disable-per-node
            show-detailed-name
            :activatable="false"
            @input="$emit('select', $event)"
          />
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="12" md="6">
      <v-card class="mb-6">
        <v-card-title>Edit Mounting info for {{ mountActionName }}</v-card-title>
        <v-card-text>
          <v-form
            ref="form"
            @submit.prevent
          >
            <mount-action-details-form
              ref="detailsForm"
              v-model="mountActionInformationDTO"
              :value="value"
              :contacts="contacts"
              :begin-date-rules="beginDateRules"
              :end-date-rules="endDateRules"
              :unmount-required="getUnmountRequired()"
              :parent-offsets="parentOffsets"
              with-unmount
            />
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import { DevicesState, LoadDeviceAvailabilitiesAction } from '@/store/devices'
import { PlatformsState, LoadPlatformAvailabilitiesAction } from '@/store/platforms'
import { ConfigurationsState, LoadConfigurationDynamicLocationActionsAction } from '@/store/configurations'

import { Contact } from '@/models/Contact'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { Availability } from '@/models/Availability'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

import { MountActionValidator, MountActionValidationResultOp } from '@/utils/MountActionValidator'
import { IOffsets, MountActionInformationDTO } from '@/utils/configurationInterfaces'

import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'
import { sumOffsets } from '@/utils/configurationsTreeHelper'

@Component({
  components: {
    ConfigurationsTreeView,
    MountActionDetailsForm
  },
  computed: {
    ...mapState('devices', ['deviceAvailabilities']),
    ...mapState('platforms', ['platformAvailabilities']),
    ...mapState('configurations', ['configurationDynamicLocationActions'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceAvailabilities']),
    ...mapActions('platforms', ['loadPlatformAvailabilities']),
    ...mapActions('configurations', ['loadConfigurationDynamicLocationActions'])
  }
})
export default class MountActionEditForm extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: DeviceMountAction | PlatformMountAction

  @Prop({
    default: null,
    required: false,
    type: Object
  })
  readonly originalAction!: DeviceMountAction | PlatformMountAction

  @Prop({
    required: true,
    type: Object
  })
  readonly tree!: ConfigurationsTree

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  private selectedNode!: DeviceNode | PlatformNode | null

  private beginDateErrorMessage: string = ''
  private endDateErrorMessage: string = ''

  private deviceAvailabilities!: DevicesState['deviceAvailabilities']
  private loadDeviceAvailabilities!: LoadDeviceAvailabilitiesAction
  private platformAvailabilities!: PlatformsState['platformAvailabilities']
  private loadPlatformAvailabilities!: LoadPlatformAvailabilitiesAction
  private configurationDynamicLocationActions!: ConfigurationsState['configurationDynamicLocationActions']
  private loadConfigurationDynamicLocationActions!: LoadConfigurationDynamicLocationActionsAction

  async fetch () {
    try {
      await Promise.all([
        this.loadConfigurationDynamicLocationActions(this.configurationId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch resources')
    }
  }

  get mountActionInformationDTO () {
    return {
      beginDate: this.value.beginDate,
      endDate: this.value.endDate,
      offsetX: this.value.offsetX,
      offsetY: this.value.offsetY,
      offsetZ: this.value.offsetZ,
      epsgCode: this.value.epsgCode,
      x: this.value.x,
      y: this.value.y,
      z: this.value.z,
      elevationDatumName: this.value.elevationDatumName,
      elevationDatumUri: this.value.elevationDatumUri,
      beginContact: this.value.beginContact,
      endContact: this.value.endContact,
      beginDescription: this.value.beginDescription,
      endDescription: this.value.endDescription,
      label: this.value.label
    }
  }

  set mountActionInformationDTO (newValue: MountActionInformationDTO) {
    this.update(newValue)
  }

  get mountActionName (): string {
    if ('isDeviceMountAction' in this.value && this.value.isDeviceMountAction()) {
      return this.value.device.shortName
    }
    return this.value.platform.shortName
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get deviceMountActionId (): string {
    return this.$route.params.actionId
  }

  get beginDateRules (): ((value: string | null) => string | boolean)[] {
    return [
      (_date: string | null) => this.beginDateErrorMessage || true
    ]
  }

  get endDateRules (): ((value: string | null) => string | boolean)[] {
    return [
      (_date: string | null) => this.endDateErrorMessage || true
    ]
  }

  async update (mountActionInformationDTO: MountActionInformationDTO) {
    if (!this.selectedNode) {
      return
    }

    if (!mountActionInformationDTO.beginDate || !mountActionInformationDTO.beginContact) {
      return
    }

    let newMountAction: DeviceMountAction | PlatformMountAction
    let newNode: DeviceNode | PlatformNode

    if ('isDeviceMountAction' in this.value && this.value.isDeviceMountAction()) {
      newMountAction = new DeviceMountAction(
        this.value.id,
        this.value.device,
        this.value.parentPlatform,
        this.value.parentDevice,
        mountActionInformationDTO.beginDate,
        mountActionInformationDTO.endDate,
        mountActionInformationDTO.offsetX,
        mountActionInformationDTO.offsetY,
        mountActionInformationDTO.offsetZ,
        mountActionInformationDTO.epsgCode,
        mountActionInformationDTO.x,
        mountActionInformationDTO.y,
        mountActionInformationDTO.z,
        mountActionInformationDTO.elevationDatumName,
        mountActionInformationDTO.elevationDatumUri,
        Contact.createFromObject(mountActionInformationDTO.beginContact),
        mountActionInformationDTO.endContact ? Contact.createFromObject(mountActionInformationDTO.endContact) : null,
        mountActionInformationDTO.beginDescription,
        mountActionInformationDTO.endDescription,
        mountActionInformationDTO.label
      )
      newNode = new DeviceNode(newMountAction)
    } else {
      newMountAction = new PlatformMountAction(
        this.value.id,
        this.value.platform,
        this.value.parentPlatform,
        mountActionInformationDTO.beginDate,
        mountActionInformationDTO.endDate,
        mountActionInformationDTO.offsetX,
        mountActionInformationDTO.offsetY,
        mountActionInformationDTO.offsetZ,
        mountActionInformationDTO.epsgCode,
        mountActionInformationDTO.x,
        mountActionInformationDTO.y,
        mountActionInformationDTO.z,
        mountActionInformationDTO.elevationDatumName,
        mountActionInformationDTO.elevationDatumUri,
        Contact.createFromObject(mountActionInformationDTO.beginContact),
        mountActionInformationDTO.endContact ? Contact.createFromObject(mountActionInformationDTO.endContact) : null,
        mountActionInformationDTO.beginDescription,
        mountActionInformationDTO.endDescription,
        mountActionInformationDTO.label
      )
      newNode = new PlatformNode(newMountAction)
    }

    // we create a new tree from the old one and replace the node with the updated one
    const newTree: ConfigurationsTree = ConfigurationsTree.fromArray(this.tree.toArray())
    newTree.replace(this.selectedNode, newNode)

    // only if the dates have changed we will validate the treeS
    const datesChanged = this.value.beginDate !== newMountAction.beginDate || this.value.endDate !== newMountAction.endDate
    if (datesChanged) {
      await this.validateTree(newTree, newNode)
    }

    this.$nextTick(() => this.validateForm())
    this.$emit('input', newMountAction)
  }

  validateForm (): boolean {
    if (this.$refs.detailsForm) {
      return (this.$refs.detailsForm as MountActionDetailsForm).validateForm()
    }
    return false
  }

  async validateTree (tree: ConfigurationsTree, selected: DeviceNode | PlatformNode): Promise<boolean> {
    const validator = new MountActionValidator(tree)

    // validate parent
    const error1 = validator.nodeIsWithinParentRange(selected)
    if (typeof error1 === 'object') {
      const message = MountActionValidator.buildErrorMessage(error1) + (error1.op !== MountActionValidationResultOp.EMPTY ? ' of parent' : '')
      if (error1.property === 'mountDate') {
        this.beginDateErrorMessage = message
        this.endDateErrorMessage = ''
      } else {
        this.beginDateErrorMessage = ''
        this.endDateErrorMessage = message
      }
      return false
    }

    // validate children
    const error2 = validator.nodeChildrenAreWithinRange(selected)
    if (typeof error2 === 'object') {
      const message = MountActionValidator.buildErrorMessage(error2) + (error2.op !== MountActionValidationResultOp.EMPTY ? ' of parent' : '')
      if (error2.property === 'mountDate') {
        this.beginDateErrorMessage = message
        this.endDateErrorMessage = ''
      } else {
        this.beginDateErrorMessage = ''
        this.endDateErrorMessage = message
      }
      return false
    }

    // check availabilities
    let loadAvailabilities: LoadDeviceAvailabilitiesAction | LoadPlatformAvailabilitiesAction
    let ids: (string | null)[]

    if (selected.isDevice()) {
      loadAvailabilities = this.loadDeviceAvailabilities
      ids = [selected.unpack().device.id]
    } else {
      loadAvailabilities = this.loadPlatformAvailabilities
      ids = [selected.unpack().platform.id]
    }

    await loadAvailabilities({
      ids,
      from: selected.unpack().beginDate,
      until: null
    })

    const availabilities: Availability[] = selected.isDevice() ? this.deviceAvailabilities : this.platformAvailabilities
    // we have to ignore the current mount action
    const availabilitiesWithoutSelectedMountAction = availabilities.filter(i => i.mountID !== selected.unpack().id)

    const error3 = MountActionValidator.actionAvailableIn(selected.unpack(), availabilitiesWithoutSelectedMountAction)
    if (typeof error3 === 'object') {
      const message = MountActionValidator.buildErrorMessage(error3) + (error3.op !== MountActionValidationResultOp.EMPTY ? ' of next mounting action' : '')
      if (error3.property === 'mountDate') {
        this.beginDateErrorMessage = message
        this.endDateErrorMessage = ''
      } else {
        this.beginDateErrorMessage = ''
        this.endDateErrorMessage = message
      }
      return false
    }

    // check device mount actions against dynamic location actions
    if (selected.isDevice()) {
      const dynamicLocationActions = this.getRelatedDynamicLocationActions()
      const error4 = MountActionValidator.isDeviceMountActionCompatibleWithMultipleDynamicLocationActions(selected.unpack(), dynamicLocationActions)
      if (typeof error4 === 'object') {
        const message = MountActionValidator.buildErrorMessage(error4) + ' of dynamic location action'
        if (error4.property === 'mountDate') {
          this.beginDateErrorMessage = message
          this.endDateErrorMessage = ''
        } else {
          this.beginDateErrorMessage = ''
          this.endDateErrorMessage = message
        }
        return false
      }
    }

    // if we have no errors at all, clear the error messages
    this.beginDateErrorMessage = ''
    this.endDateErrorMessage = ''
    return true
  }

  getRelatedDynamicLocationActions (): DynamicLocationAction[] {
    if (!this.originalAction || !('device' in this.originalAction)) {
      return []
    }
    // filter all dynamic location actions, that are within the original time range
    return MountActionValidator.getRelatedDynamicLocationActions(this.originalAction, this.configurationDynamicLocationActions)
  }

  getUnmountRequired (): boolean {
    if (!this.selectedNode) {
      return false
    }
    const parent = this.tree.getParent(this.selectedNode)
    if (parent && parent.unpack().endDate) {
      return true
    }
    return false
  }

  get parentOffsets (): IOffsets {
    if (!this.selectedNode) {
      return {
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0
      }
    }
    const parents = this.tree.getParents(this.selectedNode)
    return sumOffsets(parents)
  }

  @Watch('value', {
    deep: true,
    immediate: true
  })
  onValueChanged (mountAction: DeviceMountAction | PlatformMountAction) {
    if (mountAction) {
      if ('isDeviceMountAction' in mountAction && mountAction.isDeviceMountAction()) {
        this.selectedNode = this.tree.getAllDeviceNodesAsList().find(i => i.unpack().id === mountAction.id) || null
        return
      }
      this.selectedNode = this.tree.getAllPlatformNodesAsList().find(i => i.unpack().id === mountAction.id) || null
    }
  }
}
</script>
