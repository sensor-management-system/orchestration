<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      v-model="isFormValid"
      @submit.prevent
    >
      <v-row justify="start" class="mb-6">
        <v-col cols="6" md="6">
          <DateTimePicker
            v-model="beginDate"
            placeholder="e.g. 2000-01-31 12:00"
            label="Select mount date"
            hint="Mount date"
            required
            class="required"
            :rules="[...[rules.required], ...beginDateExtraRules]"
            @input="emitUpdate"
          />
        </v-col>
        <v-col cols="6">
          <DateTimePicker
            v-model="endDate"
            placeholder="Open End"
            label="Select unmount date"
            :rules="endDateExtraRules"
            @input="emitUpdate"
          />
        </v-col>
      </v-row>
    </v-form>
    <v-alert
      :value="treeHasErrors"
      type="error"
      text
      dismissible
      transition="scroll-y-reverse-transition"
    >
      <p>
        Some devices or platforms can't be used for the selected dates. You can click on the nodes marked with
        <v-icon class="error--text">
          mdi-alert
        </v-icon>
        to see detailed information. You can exchange these using the
        <v-icon class="black--text">
          mdi-swap-horizontal-circle-outline
        </v-icon>
        button.
      </p>
      <p />
    </v-alert>
    <v-scroll-y-reverse-transition>
      <div v-show="selectedMountTree && beginDate">
        <v-row>
          <v-col col="12" md="6">
            <v-card>
              <v-card-text>
                <configurations-tree-view
                  v-model="selectedMountNode"
                  :tree="treeCopy"
                  :disable-per-node="true"
                >
                  <template #append="{item}">
                    <v-tooltip
                      top
                    >
                      <template #activator="{ on, attrs }">
                        <v-btn
                          v-if="item.isDevice()"
                          icon
                          small
                          v-bind="attrs"
                          :disabled="isExchangeButtonDisabled()"
                          @click.stop="openDeviceExchangeDialog(item)"
                          v-on="on"
                        >
                          <v-icon>
                            mdi-swap-horizontal-circle-outline
                          </v-icon>
                        </v-btn>
                        <v-btn
                          v-if="item.isPlatform()"
                          icon
                          small
                          v-bind="attrs"
                          :disabled="isExchangeButtonDisabled()"
                          @click.stop="openPlatformExchangeDialog(item)"
                          v-on="on"
                        >
                          <v-icon>
                            mdi-swap-horizontal-circle-outline
                          </v-icon>
                        </v-btn>
                      </template>
                      <span v-if="item.isDevice()">Exchange device</span>
                      <span v-if="item.isPlatform()">Exchange platform</span>
                    </v-tooltip>
                  </template>
                </configurations-tree-view>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col v-show="selectedMountNode && !selectedMountNode.hasErrors && isFormValid" v-if="selectedMountNode">
            <v-card class="mb-6">
              <v-card-title>Edit Mounting info for {{ selectedMountNode.name }}</v-card-title>
              <v-card-text>
                <v-form
                  ref="form"
                  @submit.prevent
                >
                  <mount-action-details-form
                    ref="detailsForm"
                    v-model="mountActionInformationDTO"
                    :value="selectedMountNode.node"
                    :parent-offsets="parentOffsets"
                    :contacts="contacts"
                    :with-dates="false"
                  />
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col v-show="selectedMountNode && selectedMountNode.hasErrors" v-if="selectedMountNode">
            <v-alert v-if="selectedMountNode.hasErrors" text type="error">
              <div v-for="(errorMessage, i) in selectedMountNode.errors" :key="i" class="error--text">
                {{ errorMessage }}
              </div>
            </v-alert>
          </v-col>
        </v-row>
      </div>
    </v-scroll-y-reverse-transition>
    <ReuseDeviceExchangeDialog
      v-if="beginDate"
      ref="reuseDeviceExchangeDialog"
      v-model="showDeviceExchangeDialog"
      :begin-date="beginDate"
      :end-date="endDate"
      :devices-used-in-tree="devicesInTree"
      @selected="exchangeDevice"
      @cancel="showDeviceExchangeDialog=false"
    />
    <ReusePlatformExchangeDialog
      v-if="beginDate"
      ref="reusePlatformExchangeDialog"
      v-model="showPlatformExchangeDialog"
      :begin-date="beginDate"
      :end-date="endDate"
      :platforms-used-in-tree="platformsInTree"
      @selected="exchangePlatform"
      @cancel="showPlatformExchangeDialog=false"
    />
  </div>
</template>

<script lang="ts">
import { mapActions, mapGetters, mapState } from 'vuex'
import { Component, Prop, Watch, PropSync, mixins } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'
import { ContactsState } from '@/store/contacts'
import { IOffsets, MountActionInformationDTO } from '@/utils/configurationInterfaces'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { Contact } from '@/models/Contact'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import BaseMountList from '@/components/shared/BaseMountList.vue'
import { Device } from '@/models/Device'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { Platform } from '@/models/Platform'
import DeviceBasicSearch from '@/components/devices/DeviceBasicSearch.vue'
import DevicePageSizeSelect from '@/components/devices/DevicePageSizeSelect.vue'
import DevicePagination from '@/components/devices/DevicePagination.vue'
import ReuseDeviceExchangeList from '@/components/configurations/reuseMounts/ReuseDeviceExchangeList.vue'
import ReuseDeviceExchangeDialog from '@/components/configurations/reuseMounts/ReuseDeviceExchangeDialog.vue'
import ReusePlatformExchangeDialog from '@/components/configurations/reuseMounts/ReusePlatformExchangeDialog.vue'
import { sumOffsets } from '@/utils/configurationsTreeHelper'
import { LoadPlatformAvailabilitiesAction } from '@/store/platforms'
import { LoadDeviceAvailabilitiesAction } from '@/store/devices'
import { SetLoadingAction } from '@/store/progressindicator'
import { availabilityReason } from '@/utils/mountHelper'
import { Availability } from '@/models/Availability'
import { Rules } from '@/mixins/Rules'
import Validator from '@/utils/validator'

@Component({
  components: {
    ReusePlatformExchangeDialog,
    ReuseDeviceExchangeDialog,
    ReuseDeviceExchangeList,
    DevicePagination,
    DevicePageSizeSelect,
    DeviceBasicSearch,
    ExtendedItemName,
    BaseMountList,
    PageSizeSelect,
    MountActionDetailsForm,
    ConfigurationsTreeView,
    DateTimePicker
  },
  computed: {
    ...mapState('contacts', ['contacts']),
    ...mapGetters('platforms', { getPlatformAvailability: 'getAvailability' }),
    ...mapGetters('devices', { getDeviceAvailability: 'getAvailability' })
  },
  methods: {
    ...mapActions('platforms', ['loadPlatformAvailabilities']),
    ...mapActions('devices', ['loadDeviceAvailabilities']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ReuseUpdateMountInformation extends mixins(Rules) {
  @Prop({
    required: true,
    type: Object
  })
    selectedMountTree!: ConfigurationsTree

  @PropSync(
    'hasFormErrors',
    {
      type: Boolean,
      default: false
    })
    syncHasFormErrors!: boolean

  private treeCopy = new ConfigurationsTree()

  private showDeviceExchangeDialog = false
  private showPlatformExchangeDialog = false

  private beginDate: DateTime | null = null
  private endDate: DateTime | null = null
  private contacts!: ContactsState['contacts']

  private selectedMountNode: DeviceNode | PlatformNode | null = null

  private deviceNodeToExchange: DeviceNode | null = null
  private platformNodeToExchange: PlatformNode | null = null

  // This only validates the dates
  private isFormValid: boolean = false

  // vuex type definitions
  loadPlatformAvailabilities!: LoadPlatformAvailabilitiesAction
  loadDeviceAvailabilities!: LoadDeviceAvailabilitiesAction
  setLoading!: SetLoadingAction
  getPlatformAvailability!: (platform: Platform) => Availability | null
  getDeviceAvailability!: (device: Device) => Availability | null

  createTreeCopy (val: ConfigurationsTree) {
    this.treeCopy = ConfigurationsTree.createFromObject(val)
  }

  get devicesInTree () {
    return this.treeCopy.getAllDeviceNodesAsList().map((node: DeviceNode) => {
      return node.unpack().device
    })
  }

  get platformsInTree () {
    return this.treeCopy.getAllPlatformNodesAsList().map((node: PlatformNode) => {
      return node.unpack().platform
    })
  }

  get treeHasErrors () {
    return this.treeCopy.root.hasErrors || this.treeCopy.root.hasChildErrors
  }

  get mountActionInformationDTO () {
    if (this.selectedMountNode) {
      const mountInfo = this.selectedMountNode.unpack()
      return {
        beginDate: mountInfo.beginDate,
        endDate: mountInfo.endDate,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        epsgCode: mountInfo.epsgCode,
        x: mountInfo.x,
        y: mountInfo.y,
        z: mountInfo.z,
        elevationDatumName: mountInfo.elevationDatumName,
        elevationDatumUri: mountInfo.elevationDatumUri,
        beginContact: mountInfo.beginContact,
        endContact: mountInfo.endContact,
        beginDescription: mountInfo.beginDescription,
        endDescription: mountInfo.endDescription,
        label: mountInfo.label
      }
    }
    return null
  }

  set mountActionInformationDTO (newValue: MountActionInformationDTO | null) {
    this.update(newValue)
  }

  get parentOffsets (): IOffsets {
    if (!this.selectedMountNode) {
      return {
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0
      }
    }
    const parents = this.treeCopy.getParents(this.selectedMountNode)
    return sumOffsets(parents)
  }

  get beginDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.beginDate, this.endDate)
    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.beginDate, this.endDate)
    ]
  }

  public setSelectedMountNode (node: DeviceNode | PlatformNode | null) {
    this.selectedMountNode = node
  }

  isExchangeButtonDisabled () {
    return this.beginDate === null || !this.isFormValid
  }

  update (mountActionInformationDTO: MountActionInformationDTO | null) {
    if (!mountActionInformationDTO) {
      return
    }

    if (!this.selectedMountNode || !this.treeCopy) {
      return
    }

    if (!mountActionInformationDTO.beginDate || !mountActionInformationDTO.beginContact) {
      return null
    }

    if (this.selectedMountNode.id != null) {
      const nodeInTree = this.treeCopy.getById(this.selectedMountNode.id) as DeviceNode | PlatformNode | null

      if (nodeInTree) {
        const originalAction = nodeInTree.unpack()
        this.updateAction(originalAction, mountActionInformationDTO)
        this.emitUpdate()
      }
    }
  }

  emitUpdate () {
    this.$emit('update', {
      beginDate: this.beginDate,
      endDate: this.endDate,
      tree: this.treeCopy
    })
  }

  openDeviceExchangeDialog (node: DeviceNode) {
    this.showDeviceExchangeDialog = true
    this.showPlatformExchangeDialog = false

    this.deviceNodeToExchange = node
  }

  openPlatformExchangeDialog (node: PlatformNode) {
    this.showDeviceExchangeDialog = false
    this.showPlatformExchangeDialog = true

    this.platformNodeToExchange = node
  }

  exchangeDevice (selection: Device) {
    if (!this.deviceNodeToExchange) {
      return
    }
    const action = this.deviceNodeToExchange.unpack() as DeviceMountAction
    action.device = selection

    for (const child of this.deviceNodeToExchange.children) {
      // a device node can only have other device nodes as child, never a platform node nor configuration node
      const childAction = child.unpack() as DeviceMountAction
      childAction.parentDevice = selection
    }

    this.emitUpdate()

    this.deviceNodeToExchange.removeErrors()

    this.showDeviceExchangeDialog = false
    this.deviceNodeToExchange = null
    this.selectedMountNode = null
  }

  exchangePlatform (selection: Platform) {
    if (!this.platformNodeToExchange) {
      return
    }

    const action = this.platformNodeToExchange.unpack() as PlatformMountAction
    action.platform = selection

    // Each child needs to update its parent platform
    for (const child of this.platformNodeToExchange.children) {
      const childAction = child.unpack()
      childAction.parentPlatform = selection
    }

    this.emitUpdate()
    this.platformNodeToExchange.removeErrors()
    this.showPlatformExchangeDialog = false
    this.platformNodeToExchange = null
    this.selectedMountNode = null
  }

  updateAction (originalAction: PlatformMountAction | DeviceMountAction, mountActionInformationDTO: MountActionInformationDTO) {
    if (!mountActionInformationDTO.beginDate || !mountActionInformationDTO.beginContact) {
      return null
    }
    originalAction.beginDate = mountActionInformationDTO.beginDate
    originalAction.endDate = mountActionInformationDTO.endDate
    originalAction.offsetX = mountActionInformationDTO.offsetX
    originalAction.offsetY = mountActionInformationDTO.offsetY
    originalAction.offsetZ = mountActionInformationDTO.offsetZ
    originalAction.epsgCode = mountActionInformationDTO.epsgCode
    originalAction.x = mountActionInformationDTO.x
    originalAction.y = mountActionInformationDTO.y
    originalAction.z = mountActionInformationDTO.z
    originalAction.elevationDatumName = mountActionInformationDTO.elevationDatumName
    originalAction.elevationDatumUri = mountActionInformationDTO.elevationDatumUri
    originalAction.beginDescription = mountActionInformationDTO.beginDescription
    originalAction.endDescription = mountActionInformationDTO.endDescription
    originalAction.label = mountActionInformationDTO.label
    originalAction.beginContact = Contact.createFromObject(mountActionInformationDTO.beginContact)
    originalAction.endContact = mountActionInformationDTO.endContact ? Contact.createFromObject(mountActionInformationDTO.endContact) : null
  }

  public async checkAvailabilityOfSelectedMountTree () {
    try {
      if (this.canCheckForAvailability()) {
        this.setLoading(true)

        const deviceIdsUsedInTree = this.treeCopy.getAllDeviceNodesAsList().map(node => node.unpack().device.id)
        const platformIdsUsedInTree = this.treeCopy.getAllPlatformNodesAsList().map(node => node.unpack().platform.id)

        await Promise.all([
          this.loadPlatformAvailabilities({
            ids: platformIdsUsedInTree,
            from: this.beginDate!,
            until: this.endDate
          }),
          this.loadDeviceAvailabilities({ ids: deviceIdsUsedInTree, from: this.beginDate!, until: this.endDate })
        ])

        for (const node of this.treeCopy.getAllPlatformNodesAsList()) {
          const platformOfNode = node.unpack().platform
          const platformAvailability = this.getPlatformAvailability(platformOfNode)
          if (platformAvailability && !platformAvailability.available) {
            const reason = availabilityReason(platformAvailability)
            node.errors = [reason]
          } else {
            node.removeErrors()
          }
        }

        for (const node of this.treeCopy.getAllDeviceNodesAsList()) {
          const deviceOfNode = node.unpack().device
          const deviceAvailability = this.getDeviceAvailability(deviceOfNode)
          if (deviceAvailability && !deviceAvailability.available) {
            const reason = availabilityReason(deviceAvailability)
            node.errors = [reason]
          } else {
            node.removeErrors()
          }
        }
      }
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of availabilities for the selected mount setup failed')
    } finally {
      this.setLoading(false)
    }
  }

  canCheckForAvailability () {
    if (this.beginDate) {
      if (this.endDate) {
        return this.beginDate < this.endDate
      }
      return true
    }
    return false
  }

  updateSyncHasFormErrors () {
    this.syncHasFormErrors = !this.isFormValid || this.treeHasErrors
  }

  @Watch('selectedMountTree', { immediate: true, deep: true })
  onValueChanged (val: ConfigurationsTree) {
    this.createTreeCopy(val)
  }

  @Watch('beginDate', { immediate: true, deep: true })
  async onBeginDateChanged () {
    await this.checkAvailabilityOfSelectedMountTree()
    this.selectedMountNode = null
  }

  @Watch('endDate', { immediate: true, deep: true })
  async onEndDateChanged () {
    await this.checkAvailabilityOfSelectedMountTree()
    this.selectedMountNode = null
  }

  @Watch('isFormValid')
  onIsFormValidChanged () {
    this.updateSyncHasFormErrors()
  }

  @Watch('treeHasErrors')
  onTreeHasErrorsChanged () {
    this.updateSyncHasFormErrors()
  }
}
</script>

<style scoped>

</style>
