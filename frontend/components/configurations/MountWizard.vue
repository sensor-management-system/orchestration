<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-stepper
      v-model="step"
      vertical
    >
      <v-stepper-step
        editable
        :complete="!!selectedDate"
        :rules="[rules.validateMountingDates, rules.validateMountingTimeRange]"
        step="1"
      >
        Select a date
        <small v-if="rules.validateMountingDates() !== true">{{ rules.validateMountingDates() }}</small>
        <small v-else-if="rules.validateMountingTimeRange() !== true">{{ rules.validateMountingTimeRange() }}</small>
        <small v-else>The referenced time zone is UTC. </small>
      </v-stepper-step>

      <v-stepper-content step="1">
        <v-container>
          <mount-action-date-form
            ref="mountActionDateForm"
            v-model="mountActionDateDTO"
            :begin-date-rules="beginDateRules"
            :end-date-rules="endDateRules"
            :end-required="selectedNodeEndDate !== null"
          />
          <v-row class="mb-6">
            <v-btn
              color="primary"
              :disabled="!selectedDate"
              @click="step++"
            >
              Continue
            </v-btn>
          </v-row>
        </v-container>
      </v-stepper-content>

      <v-stepper-step
        :complete="isStep2Complete() && (!isSelectedNodeAlreadyArchived())"
        editable
        step="2"
        :rules="[rules.validateMountingTimeRange]"
      >
        Choose parent platform
      </v-stepper-step>

      <v-stepper-content step="2">
        <v-container>
          <mount-wizard-node-select
            v-if="tree"
            :selected-node.sync="selectedNode"
            :tree="tree"
          />
          <v-row class="mb-6">
            <v-btn
              color="primary"
              :disabled="!isStep2Complete() || isSelectedNodeAlreadyArchived()"
              @click="step++"
            >
              Continue
            </v-btn>
            <div v-if="isSelectedNodeAlreadyArchived()">
              <v-tooltip right>
                <template #activator="{ on, attrs }">
                  <v-icon v-bind="attrs" v-on="on">
                    mdi-alert
                  </v-icon>
                </template>
                <span>The selected parent platform is already archived.</span>
              </v-tooltip>
            </div>
            <div v-if="isTryingToMountPlatformdUnderDevices()">
              <v-tooltip right>
                <template #activator="{ on, attrs }">
                  <v-icon v-bind="attrs" v-on="on">
                    mdi-alert
                  </v-icon>
                </template>
                <span>Platforms can't be mounted under devices.</span>
              </v-tooltip>
            </div>
          </v-row>
        </v-container>
      </v-stepper-content>

      <v-stepper-step
        :editable="selectedDate && selectedEntities.length > 0"
        :rules="[()=>!!selectedDate]"
        :complete="selectedEntities.length > 0"
        step="3"
      >
        Select
        <small>Choose platforms or devices for mounting</small>
      </v-stepper-step>

      <v-stepper-content step="3">
        <v-container>
          <mount-wizard-entity-select
            :selected-devices.sync="selectedDevices"
            :selected-platforms.sync="selectedPlatforms"
            :devices-to-mount.sync="devicesToMount"
            :platforms-to-mount.sync="platformsToMount"
            :platform-selection-disabled="selectedNode?.isDevice()"
          />
          <v-row>
            <v-col>
              <v-btn
                color="primary"
                :disabled="selectedEntities.length === 0 || isTryingToMountPlatformdUnderDevices()"
                @click="confirmSelection(); step++"
              >
                Confirm selection
              </v-btn>
              <span v-if="isTryingToMountPlatformdUnderDevices()">
                <v-tooltip right>
                  <template #activator="{ on, attrs }">
                    <v-icon v-bind="attrs" v-on="on">
                      mdi-alert
                    </v-icon>
                  </template>
                  <span>Platforms can't be mounted under devices.</span>
                </v-tooltip>
              </span>
              <v-btn text @click="clearSelection()">
                Clear selection
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-stepper-content>

      <v-stepper-step
        :rules="[() => isMountInformationStepValid]"
        :editable="selectedDevices.length > 0 || selectedPlatforms.length > 0"
        :complete="platformsToMount.length > 0 || devicesToMount.length > 0"
        step="4"
      >
        Add mount information
      </v-stepper-step>

      <v-stepper-content step="4">
        <v-container>
          <mount-wizard-mount-form
            ref="mountActionMountDevicesForm"
            v-model="devicesToMount"
            prefix="devices-mount-info"
            :parent-offsets="parentOffsets"
          />
          <mount-wizard-mount-form
            ref="mountActionMountPlatformsForm"
            v-model="platformsToMount"
            prefix="platforms-mount-info"
            :parent-offsets="parentOffsets"
          />
          <v-row class="mb-6">
            <v-btn
              color="primary"
              @click="validateMountInformationStep"
            >
              Continue
            </v-btn>
          </v-row>
        </v-container>
      </v-stepper-content>
      <v-stepper-step
        :editable="isSubmitStepEditable"
        step="5"
      >
        Submit
        <small>Confirm your inputs</small>
      </v-stepper-step>
      <v-stepper-content step="5">
        <v-container>
          <v-subheader>Preview</v-subheader>
          <configurations-tree-view
            :tree="treePreview"
            :value="null"
          />
          <mount-wizard-submit-overview
            :devices-to-mount.sync="devicesToMount"
            :platforms-to-mount.sync="platformsToMount"
            :parent-offsets="parentOffsets"
          />
          <v-row>
            <v-col>
              <v-btn
                block
                color="primary"
                @click="mount"
              >
                Submit
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-stepper-content>
    </v-stepper>
  </div>
</template>

<script lang="ts">
import { Component, Vue, ProvideReactive, PropSync, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DateTime } from 'luxon'

import {
  LoadConfigurationAction,
  AddPlatformMountActionAction,
  AddDeviceMountActionAction,
  LoadMountingConfigurationForDateAction
} from '@/store/configurations'
import { ContactsState } from '@/store/contacts'
import { ClearDeviceAvailabilitiesAction } from '@/store/devices'
import { ClearPlatformAvailabilitiesAction } from '@/store/platforms'

import { MountAction } from '@/models/MountAction'
import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { PlatformNode } from '@/viewmodels/PlatformNode'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'

import Validator from '@/utils/validator'
import { MountActionValidator, MountActionValidationResultOp } from '@/utils/MountActionValidator'
import { MountActionInformationDTO, MountActionDateDTO, IOffsets } from '@/utils/configurationInterfaces'
import { sumOffsets } from '@/utils/configurationsTreeHelper'

import MountActionDateForm from '@/components/configurations/MountActionDateForm.vue'
import MountWizardNodeSelect from '@/components/configurations/MountWizardNodeSelect.vue'
import MountWizardEntitySelect from '@/components/configurations/MountWizardEntitySelect.vue'
import MountWizardMountForm from '@/components/configurations/MountWizardMountForm.vue'
import MountWizardSubmitOverview from '@/components/configurations/MountWizardSubmitOverview.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import MountActionDetailsForm from '@/components/configurations/MountActionDetailsForm.vue'
import { DeviceNode } from '@/viewmodels/DeviceNode'

@Component({
  components: {
    ConfigurationsTreeView,
    MountActionDetailsForm,
    MountActionDateForm,
    MountWizardNodeSelect,
    MountWizardEntitySelect,
    MountWizardMountForm,
    MountWizardSubmitOverview
  },
  computed: {
    ...mapState('configurations', ['configuration', 'configurationMountingActionsForDate']),
    ...mapState('contacts', ['contacts'])
  },
  methods: {
    ...mapActions('devices', ['clearDeviceAvailabilities']),
    ...mapActions('platforms', ['clearPlatformAvailabilities']),
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('configurations', ['addDeviceMountAction', 'addPlatformMountAction', 'loadConfiguration', 'loadMountingConfigurationForDate'])
  }
})
export default class MountWizard extends Vue {
  @PropSync('hasSaved', {
    required: false,
    type: Boolean
  })
    syncedHasSaved!: boolean

  private step = 1

  private tree: ConfigurationsTree = new ConfigurationsTree()

  @ProvideReactive() private selectedNode: ConfigurationsTreeNode | null = null
  @ProvideReactive() private selectedDate: DateTime | null = DateTime.utc()
  @ProvideReactive() private selectedEndDate: DateTime | null = null

  private platformsToMount: { entity: Platform, mountInfo: MountActionInformationDTO }[] = []
  private selectedPlatforms: Platform[] = []

  private devicesToMount: { entity: Device, mountInfo: MountActionInformationDTO }[] = []
  private selectedDevices: Device[] = []

  private beginDateErrorMessage: string = ''
  private endDateErrorMessage: string = ''

  private parentOffsets: IOffsets = { offsetX: 0, offsetY: 0, offsetZ: 0 }

  private isMountInformationStepValid = true
  private hasMountInformationStepBeenValidated = false

  // vuex definition for typescript check
  contacts!: ContactsState['contacts']
  configuration!: Configuration
  loadConfiguration!: LoadConfigurationAction
  addDeviceMountAction!: AddDeviceMountActionAction
  addPlatformMountAction!: AddPlatformMountActionAction
  loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  configurationMountingActionsForDate!: ConfigurationsTree
  clearDeviceAvailabilities!: ClearDeviceAvailabilitiesAction
  clearPlatformAvailabilities!: ClearPlatformAvailabilitiesAction
  setLoading!: SetLoadingAction

  async created () {
    this.syncedHasSaved = false
    // prefill the begin date with the selected date by the user
    this.selectedDate = this.$store.state.configurations.selectedDate
    this.selectedEndDate = this.configuration.endDate
    await this.createTree()
  }

  async createTree () {
    await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
    this.createTreeWithConfigAsRootNode()
  }

  get mountActionDateDTO (): MountActionDateDTO {
    return {
      beginDate: this.selectedDate,
      endDate: this.selectedEndDate
    }
  }

  set mountActionDateDTO (value: MountActionDateDTO) {
    this.selectedDate = value.beginDate
    this.selectedEndDate = value.endDate
  }

  get configurationId (): string {
    return this.$route.params.configurationId
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

  get selectedNodeBeginDate (): DateTime | null {
    if (this.selectedNode && 'beginDate' in this.selectedNode.unpack()) {
      return (this.selectedNode.unpack() as DeviceMountAction | PlatformMountAction).beginDate
    } else {
      return null
    }
  }

  get selectedNodeEndDate (): DateTime | null {
    if (this.selectedNode && 'endDate' in this.selectedNode.unpack()) {
      return (this.selectedNode.unpack() as DeviceMountAction | PlatformMountAction).endDate
    } else if (this.configuration) {
      return this.configuration.endDate
    } else {
      return null
    }
  }

  createTreeWithConfigAsRootNode () {
    if (this.configuration) {
      // construct the configuration as the root node of the tree
      const rootNode = new ConfigurationNode(new ConfigurationMountAction(this.configuration))
      rootNode.children = ConfigurationsTree.createFromObject(this.configurationMountingActionsForDate).toArray()
      this.tree = ConfigurationsTree.fromArray([rootNode])
    }
  }

  async mount () {
    if (!this.validateAllForms()) {
      this.$store.commit('snackbar/setError', 'Please correct your inputs')
      return
    }

    this.devicesToMount.forEach((deviceMount) => {
      try {
        this.mountDevice(deviceMount!.entity, deviceMount!.mountInfo)
      } catch (e) {
        this.$store.commit('snackbar/setError', `Mounting of device ${deviceMount.entity.shortName} failed`)
      }
    })

    this.platformsToMount.forEach((platformMount) => {
      try {
        this.mountPlatform(platformMount!.entity, platformMount!.mountInfo)
      } catch (e) {
        this.$store.commit('snackbar/setError', `Mounting of platform ${platformMount.entity.shortName} failed`)
      }
    })

    this.clearDeviceAvailabilities()
    this.clearPlatformAvailabilities()

    this.syncedHasSaved = true
    await this.loadConfiguration(this.configurationId)
    await this.loadMountingConfigurationForDate({ id: this.configurationId, timepoint: this.selectedDate })
    this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
  }

  async mountDevice (device: Device, mountInfo: MountActionInformationDTO) {
    try {
      if (this.selectedNode && !this.selectedNode.canHaveChildren()) {
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      this.setLoading(true)

      let parentPlatform = null
      let parentDevice = null
      if (this.selectedNode && this.selectedNode.canHaveChildren() && !this.selectedNode.isConfiguration()) {
        if (this.selectedNode.isPlatform()) {
          parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
        } else if (this.selectedNode.isDevice()) {
          parentDevice = (this.selectedNode as DeviceNode).unpack().device
        }
      }

      const newDeviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform,
        parentDevice,
        beginDate: mountInfo.beginDate!,
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
        beginContact: Contact.createFromObject(mountInfo.beginContact!),
        endContact: mountInfo.endContact ? Contact.createFromObject(mountInfo.endContact) : null,
        beginDescription: mountInfo.beginDescription,
        endDescription: mountInfo.endDescription,
        label: mountInfo.label
      })

      await this.addDeviceMountAction({
        configurationId: this.configurationId,
        deviceMountAction: newDeviceMountAction
      })
      this.$store.commit('snackbar/setSuccess', 'Save successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add device mount action')
    } finally {
      this.setLoading(false)
    }
  }

  async mountPlatform (platform: Platform, mountInfo: MountActionInformationDTO) {
    try {
      if (this.selectedNode && !this.selectedNode.canHaveChildren()) {
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      let parentPlatform = null

      this.setLoading(true)

      if (this.selectedNode && this.selectedNode.canHaveChildren() && !this.selectedNode.isConfiguration()) {
        parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
      }

      const newPlatformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform,
        beginDate: mountInfo.beginDate!,
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
        beginContact: Contact.createFromObject(mountInfo.beginContact!),
        endContact: mountInfo.endContact ? Contact.createFromObject(mountInfo.endContact) : null,
        beginDescription: mountInfo.beginDescription,
        endDescription: mountInfo.endDescription,
        label: mountInfo.label
      })

      await this.addPlatformMountAction({
        configurationId: this.configurationId,
        platformMountAction: newPlatformMountAction
      })
      this.$store.commit('snackbar/setSuccess', 'Save successful')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add platform mount action')
    } finally {
      this.setLoading(false)
    }
  }

  get selectedEntities () {
    return [...this.selectedPlatforms, ...this.selectedDevices]
  }

  get rules (): { [index: string]: () => string | boolean } {
    return {
      validateMountingDates: this.validateMountingDates.bind(this),
      validateMountingTimeRange: this.validateMountingTimeRange.bind(this)
    }
  }

  get treePreview (): ConfigurationsTree {
    const copyOfTheTree = ConfigurationsTree.createFromObject(this.tree)
    if (!this.selectedNode) {
      return copyOfTheTree
    }
    const currentParent = copyOfTheTree.getById(this.selectedNode!.id!)

    let children: ConfigurationsTreeNode[] = []
    let parentPlatform: Platform | null = null
    let parentDevice: Device | null = null
    if (currentParent instanceof PlatformNode) {
      children = currentParent.children
      parentPlatform = currentParent.unpack().platform
    } else if (currentParent instanceof DeviceNode) {
      children = currentParent.children
      parentDevice = currentParent.unpack().device
    } else if (currentParent instanceof ConfigurationNode) {
      children = currentParent.children
    }
    for (const entry of this.platformsToMount) {
      const entity = entry.entity
      const mountInfo = entry.mountInfo
      children.push(new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform: entity,
        parentPlatform,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        epsgCode: mountInfo.epsgCode,
        x: mountInfo.x,
        y: mountInfo.y,
        z: mountInfo.z,
        elevationDatumName: mountInfo.elevationDatumName,
        elevationDatumUri: mountInfo.elevationDatumUri,
        beginDate: mountInfo.beginDate!,
        beginContact: mountInfo.beginContact!,
        endDate: mountInfo.endDate,
        endContact: mountInfo.endContact,
        beginDescription: mountInfo.beginDescription,
        endDescription: mountInfo.endDescription,
        label: mountInfo.label
      })))
    }
    for (const entry of this.devicesToMount) {
      const entity = entry.entity
      const mountInfo = entry.mountInfo
      children.push(new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device: entity,
        parentPlatform,
        parentDevice,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        epsgCode: mountInfo.epsgCode,
        x: mountInfo.x,
        y: mountInfo.y,
        z: mountInfo.z,
        elevationDatumName: mountInfo.elevationDatumName,
        elevationDatumUri: mountInfo.elevationDatumUri,
        beginDate: mountInfo.beginDate!,
        beginContact: mountInfo.beginContact!,
        endDate: mountInfo.endDate,
        endContact: mountInfo.endContact,
        beginDescription: mountInfo.beginDescription,
        endDescription: mountInfo.endDescription,
        label: mountInfo.label
      })))
    }

    return copyOfTheTree
  }

  validateMountInformationStep () {
    this.isMountInformationStepValid = this.validateAllForms()
    this.hasMountInformationStepBeenValidated = true
    if (this.isMountInformationStepValid) {
      this.step++
    }
  }

  validateAllForms (): boolean {
    return Object.values(this.$refs).every(
      ref => (ref as Vue & { validateForm: () => boolean }).validateForm()
    )
  }

  validateMountingDates (): string | boolean {
    return Validator.validateMountingDates(this.selectedDate, this.selectedEndDate)
  }

  validateMountingTimeRange (): string | boolean {
    const mountBeginDate = this.selectedDate
    const mountEndDate = this.selectedEndDate
    const parentBeginDate = this.selectedNodeBeginDate || this.configuration.startDate
    const parentEndDate = this.selectedNodeEndDate || this.configuration.endDate

    if (!mountBeginDate) { return false }

    if (parentBeginDate) {
      const error = MountActionValidator.actionConflictsWith(
        new MountAction(
          'new node',
          null,
          mountBeginDate,
          mountEndDate,
          0,
          0,
          0,
          '',
          null,
          null,
          null,
          '',
          '',
          new Contact(),
          null,
          '',
          null,
          ''
        ),
        new MountAction(
          'parent node',
          null,
          parentBeginDate,
          parentEndDate,
          0,
          0,
          0,
          '',
          null,
          null,
          null,
          '',
          '',
          new Contact(),
          null,
          '',
          null,
          ''
        )
      )
      if (typeof error === 'object') {
        let message = MountActionValidator.buildErrorMessage(error)
        if (error.op !== MountActionValidationResultOp.EMPTY) {
          if (this.selectedNode) {
            message += ' of parent'
          } else {
            message += ' of configuration'
          }
        }
        if (error.property === 'mountDate') {
          this.beginDateErrorMessage = message
          this.endDateErrorMessage = ''
        } else {
          this.beginDateErrorMessage = ''
          this.endDateErrorMessage = message
        }
        return message
      }
      this.beginDateErrorMessage = ''
      this.endDateErrorMessage = ''
    }
    return true
  }

  confirmSelection () {
    type creatorFunc = <T>(entity: T) => { entity: T, mountInfo: MountActionInformationDTO }
    const createNew: creatorFunc = (entity) => {
      return {
        entity,
        mountInfo: {
          beginContact: this.currentUserAsContact || new Contact(),
          beginDate: this.selectedDate,
          endContact: this.selectedEndDate ? this.currentUserAsContact : null,
          endDate: this.selectedEndDate || null,
          beginDescription: '',
          endDescription: '',
          offsetX: 0,
          offsetY: 0,
          offsetZ: 0,
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
          label: ''
        }
      }
    }
    this.devicesToMount = this.selectedDevices.map(i => createNew<Device>(i))
    this.platformsToMount = this.selectedPlatforms.map(i => createNew<Platform>(i))
  }

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  get currentUserAsContact (): Contact | null {
    if (this.currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === this.currentUserMail)
      if (userIndex > -1) {
        return this.contacts[userIndex]
      }
    }
    return null
  }

  get isSubmitStepEditable () {
    return (this.hasMountInformationStepBeenValidated && this.isMountInformationStepValid) && (this.devicesToMount.length > 0 || this.platformsToMount.length > 0)
  }

  clearSelection () {
    this.selectedDevices = []
    this.selectedPlatforms = []
    this.devicesToMount = []
    this.platformsToMount = []
  }

  // TODO: fix this form validation
  // the form field that needs to be validated is in MountWizardDateSelect (endDate)
  // because we need the end date of the selected node for validation,
  // we have to trigger the date input's validate function from MountWizardNodeSelect, whenever the selected node changes
  // but how?
  async checkEndDateOfDatePicker () {
    await this.$nextTick()
    return true
    // return (this.$refs.form as Vue & { validate: () => boolean }).validate()
  }

  isStep2Complete (): boolean {
    return this.selectedNode !== null && this.rules.validateMountingTimeRange() === true && this.rules.validateMountingDates() === true && (!this.isTryingToMountPlatformdUnderDevices())
  }

  isTryingToMountPlatformdUnderDevices (): boolean {
    if (this.selectedNode && this.selectedNode.isDevice()) {
      if (this.platformsToMount.length > 0) {
        return true
      }
      if (this.selectedPlatforms.length > 0) {
        return true
      }
    }
    return false
  }

  isSelectedNodeAlreadyArchived (): boolean {
    if (this.selectedNode !== null) {
      if (this.selectedNode.isPlatform() && this.selectedNode.unpack().platform.archived) {
        return true
      }
      if (this.selectedNode.isDevice() && this.selectedNode.unpack().device.archived) {
        return true
      }
    }
    return false
  }

  @Watch('selectedDate', {
    immediate: true
  })
  onSelectedDateChange (_date: DateTime) {
    this.createTree()
  }

  @Watch('selectedNode', {
    immediate: true
  })
  onSelectedNodeChange (value: ConfigurationsTreeNode | null) {
    if (value === null) {
      this.parentOffsets = { offsetX: 0, offsetY: 0, offsetZ: 0 }
      return
    }
    if (value.isConfiguration()) {
      return
    }
    const parents = this.tree.getParents(value)
    this.parentOffsets = sumOffsets([...parents, value])
  }
}
</script>

<style scoped>
</style>
