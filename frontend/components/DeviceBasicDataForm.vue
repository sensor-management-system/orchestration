<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <v-form
    ref="basicForm"
    @submit.prevent
  >
    <v-row>
      <v-col cols="12" md="6">
        <visibility-switch
          :value="value.visibility"
          :rules="privateRules"
          :readonly="readonly"
          :entity-name="entityName"
          @input="update('visibility', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <permission-group-select
          :value="value.permissionGroups"
          :readonly="readonly"
          :entity-name="entityName"
          :rules="[pageRules.validatePermissionGroups]"
          @input="update('permissionGroups', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="deviceURN"
          label="URN"
          readonly
          disabled
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.persistentIdentifier"
          readonly
          disabled
          label="Persistent identifier (PID)"
          :placeholder="persistentIdentifierPlaceholder"
        >
          <template #append>
            <a
              v-if="value.persistentIdentifier"
              :href="persistentIdentifierUrl"
              target="_blank"
              class="text-decoration-none"
            >
              <v-icon small> mdi-open-in-new </v-icon>
            </a>
          </template>
        </v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <autocomplete-text-input
          :value="value.shortName"
          :readonly="readonly"
          :disabled="readonly"
          label="Short name"
          required
          class="required"
          :rules="[rules.required]"
          endpoint="device-short-names"
          @input="update('shortName', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <autocomplete-text-input
          :value="value.longName"
          :readonly="readonly"
          :disabled="readonly"
          label="Long name"
          endpoint="device-long-names"
          @input="update('longName', $event)"
        />
      </v-col>
    </v-row>

    <v-row align="center">
      <v-col v-if="deviceAttachments.length > 0" cols="12">
        <AttachmentImagesForm
          :attachments="deviceAttachments"
          :value="value.images"
          :download-attachment="downloadAttachment"
          :proxy-url="proxyUrl"
          @input="update('images', $event)"
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <combobox
          :value="valueDeviceTypeItem"
          item-text="name"
          :items="devicetypes"
          :readonly="readonly"
          :disabled="readonly"
          label="Device type"
          @input="updateDeviceType($event)"
        >
          <template #append-outer>
            <v-tooltip
              v-if="itemHasDefinition(valueDeviceTypeItem)"
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
              <span>{{ valueDeviceTypeItem.definition }}</span>
            </v-tooltip>
            <v-btn icon @click="showNewDeviceTypeDialog = true">
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
      <v-col cols="12" md="3">
        <combobox
          :value="valueManufacturerItem"
          item-text="name"
          :items="manufacturers"
          :readonly="readonly"
          :disabled="readonly"
          label="Manufacturer"
          @input="updateManufacturer($event)"
        >
          <template #append-outer>
            <v-tooltip
              v-if="itemHasDefinition(valueManufacturerItem)"
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
              <span>{{ valueManufacturerItem.definition }}</span>
            </v-tooltip>
            <v-btn icon @click="showNewManufacturerDialog = true">
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
      <v-col cols="12" md="3">
        <autocomplete-text-input
          :value="value.model"
          :readonly="readonly"
          :disabled="readonly"
          label="Model"
          endpoint="device-models"
          :filters="{manufacturer_name: value.manufacturerName}"
          @input="update('model', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <combobox
          :value="value.country"
          :items="countryNames"
          :readonly="readonly"
          :disabled="readonly"
          :clearable="!readonly"
          label="Country of origin"
          placeholder="Country"
          @input="update('country', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <combobox
          :items="equipmentstatus"
          item-text="name"
          :value="valueStatusItem"
          :readonly="readonly"
          :disabled="readonly"
          label="Status"
          clearable
          @input="updateStatus($event)"
        >
          <template #append-outer>
            <v-tooltip
              v-if="itemHasDefinition(valueStatusItem)"
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
              <span>{{ valueStatusItem.definition }}</span>
            </v-tooltip>
            <v-btn icon @click="showNewStatusDialog = true">
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
    <v-divider
      class="my-4"
    />
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
    <v-row>
      <v-col cols="12" md="9">
        <v-text-field
          :value="value.website"
          :readonly="readonly"
          :disabled="readonly"
          label="Website"
          placeholder="https://"
          type="url"
          @input="update('website', $event)"
        >
          <template slot="append">
            <a v-if="value.website.length > 0" :href="value.website" target="_blank">
              <v-icon
                small
              >
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
        </v-text-field>
      </v-col>
    </v-row>
    <v-divider
      class="my-4"
    />
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.serialNumber"
          :readonly="readonly"
          :disabled="readonly"
          label="Serial number"
          :hint="serialNumberHint"
          persistent-hint
          :placeholder="serialNumberPlaceholder"
          @input="update('serialNumber', $event)"
        >
          <v-icon v-if="serialNumberHint" slot="append" color="warning">
            mdi-alert
          </v-icon>
        </v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.inventoryNumber"
          :readonly="readonly"
          :disabled="readonly"
          label="Inventory number"
          :placeholder="inventoryNumberPlaceholder"
          @input="update('inventoryNumber', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <label>Keywords</label>
        <v-chip-group>
          <v-chip v-for="keyword, idx in value.keywords" :key="idx" close small @click:close="removeKeyword(keyword)">
            {{ keyword }}
          </v-chip>
        </v-chip-group>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <autocomplete-text-input
          ref="newKeywordField"
          :search-input.sync="newKeyword"
          label="New keyword"
          endpoint="keywords"
          @keyup.enter="addNewKeyword"
        >
          <template #append>
            <v-btn icon :disabled="!newKeyword" @click="addNewKeywordAndBlurNewKeywordField">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </autocomplete-text-input>
      </v-col>
    </v-row>
    <device-type-dialog
      v-model="showNewDeviceTypeDialog"
      :initial-term="valueDeviceTypeItem?.name"
      @aftersubmit="updateDeviceType"
    />
    <status-dialog
      v-model="showNewStatusDialog"
      :initial-term="valueStatusItem?.name"
      @aftersubmit="updateStatus"
    />
    <manufacturer-dialog
      v-model="showNewManufacturerDialog"
      :initial-term="valueManufacturerItem?.name"
      @aftersubmit="updateManufacturer"
    />
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Image } from '@/models/Image'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { DetailedUserInfo } from '@/models/UserInfo'
import { ICvSelectItem, hasDefinition } from '@/models/CvSelectItem'

import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'
import DeviceTypeDialog from '@/components/devices/DeviceTypeDialog.vue'
import ManufacturerDialog from '@/components/shared/ManufacturerDialog.vue'
import StatusDialog from '@/components/shared/StatusDialog.vue'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import AttachmentImagesForm from '@/components/shared/AttachmentImagesForm.vue'

import Combobox from '@/components/shared/Combobox.vue'

import { createDeviceUrn } from '@/modelUtils/urnBuilders'

import Validator from '@/utils/validator'
import { LoadDevicetypesAction, LoadEquipmentstatusAction, LoadManufacturersAction, VocabularyState } from '@/store/vocabulary'
import { DownloadAttachmentAction, DevicesState } from '@/store/devices'
import { ProxyUrlAction } from '@/store/proxy'

type StatusSelectValue = Status | string | undefined
type DeviceTypeSelectValue = DeviceType | string | undefined
type ManufacturerSelectValue = Manufacturer | string | undefined

@Component({
  computed: {
    ...mapState('vocabulary', ['devicetypes', 'manufacturers', 'equipmentstatus']),
    ...mapState('devices', ['deviceAttachments'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadDevicetypes', 'loadManufacturers', 'loadEquipmentstatus']),
    ...mapActions('devices', ['downloadAttachment']),
    ...mapActions('proxy', ['proxyUrl'])
  },
  components: {
    DeviceTypeDialog,
    ManufacturerDialog,
    PermissionGroupSelect,
    StatusDialog,
    VisibilitySwitch,
    AutocompleteTextInput,
    Combobox,
    AttachmentImagesForm
  }
})
export default class DeviceBasicDataForm extends mixins(Rules) {
  private permissionGroups: PermissionGroup[] = []
  private userInfo: DetailedUserInfo | null = null
  private entityName: string = 'device'
  private showNewDeviceTypeDialog = false
  private showNewStatusDialog = false
  private showNewManufacturerDialog = false
  private devicetypes!: VocabularyState['devicetypes']
  private manufacturers !: VocabularyState['manufacturers']
  private equipmentstatus !: VocabularyState['equipmentstatus']
  private serialNumbersInUse: string[] = []
  private initialSerialNumber = ''
  private newKeyword = ''

  // vuex definition for typescript check
  deviceAttachments!: DevicesState['deviceAttachments']
  downloadAttachment!: DownloadAttachmentAction
  proxyUrlAction!: ProxyUrlAction
  loadDevicetypes !: LoadDevicetypesAction
  loadManufacturers !: LoadManufacturersAction
  loadEquipmentstatus !: LoadEquipmentstatusAction

  @Prop({
    required: true,
    type: Device
  })
  readonly value!: Device

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: () => null,
    type: String
  })
  readonly inventoryNumberPlaceholder!: string | null

  @Prop({
    default: () => null,
    type: String
  })
  readonly serialNumberPlaceholder!: string | null

  @Prop({
    default: () => null,
    type: String
  })
  readonly persistentIdentifierPlaceholder!: string | null

  @Prop({
    default: () => [] as string[],
    required: true,
    type: Array
  })
  readonly countryNames!: string[]

  created () {
    this.initialSerialNumber = this.value.serialNumber
  }

  get pageRules (): {[index: string]: (a: any) => (boolean | string)} {
    return {
      validatePermissionGroups: Validator.validatePermissionGroups(this.value.isPrivate, this.entityName)
    }
  }

  get privateRules () {
    return [
      Validator.validateVisibility(this.value.visibility, this.value.permissionGroups, this.entityName)
    ]
  }

  async loadSerialNumbers (device: Device | null = null) {
    if (!device) {
      device = this.value
    }
    const deviceId = device?.id
    const params: any = {
      manufacturerName: device?.manufacturerName,
      model: device?.model
    }
    if (deviceId) {
      params.ignore = deviceId
    }
    this.serialNumbersInUse = await this.$api.autocomplete.getDeviceSerialNumbers(params)
  }

  get isSerialNumberInUse (): boolean {
    return this.serialNumbersInUse.includes(this.value.serialNumber)
  }

  get serialNumberHint () {
    return this.isSerialNumberInUse ? 'Another device already has an equal serial number.' : ''
  }

  async fetch () {
    try {
      await Promise.all([
        this.loadSerialNumbers(),
        this.loadEquipmentstatus(),
        this.loadManufacturers(),
        this.loadDevicetypes()
      ])
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of controlled vocabulary failed')
    }
  }

  update (key: string, value: any) {
    const newObj = Device.createFromObject(this.value)
    // We use a check for already inserted serial numbers.
    // For that we can filter by manufacturer & model, as we expect
    // to have collisions between different manufacturers & series.
    // We store those fields in the serialNumbersInUse variable.
    //
    // In case we change the manufacturer or the model, we also want
    // to update this list with that we check for those collisions.
    let updateSerialNumberCheck = false

    switch (key) {
      case 'shortName':
        newObj.shortName = value as string
        break
      case 'longName':
        newObj.longName = value as string
        break
      case 'country':
        newObj.country = value as string || ''
        break
      case 'model':
        newObj.model = value as string
        updateSerialNumberCheck = true
        break
      case 'description':
        newObj.description = value as string
        break
      case 'images':
        newObj.images = value as Image[]
        break
      case 'website':
        newObj.website = value as string
        break
      case 'serialNumber':
        newObj.serialNumber = value as string
        break
      case 'inventoryNumber':
        newObj.inventoryNumber = value as string
        break
      case 'permissionGroups':
        newObj.permissionGroups = value as PermissionGroup[]
        break
      case 'visibility':
        switch (value) {
          case Visibility.Private:
            newObj.visibility = Visibility.Private
            break
          case Visibility.Internal:
            newObj.visibility = Visibility.Internal
            break
          case Visibility.Public:
            newObj.visibility = Visibility.Public
            break
        }
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', newObj)
    if (updateSerialNumberCheck) {
      this.loadSerialNumbers(newObj)
    }
  }

  /**
   * updates the status
   *
   * @param {StatusSelectValue} value - an object as provided by the combobox
   * @fires DeviceBasicDataForm#input
   */
  updateStatus (value: StatusSelectValue): void {
    const newObj = Device.createFromObject(this.value)
    newObj.statusName = ''
    newObj.statusUri = ''

    if (value) {
      if (typeof value === 'string') {
        newObj.statusName = value
        newObj.statusUri = ''
        const state = this.equipmentstatus.find(s => s.name === value)
        if (state) {
          newObj.statusUri = state.uri
        }
      } else {
        newObj.statusName = value.name
        newObj.statusUri = value.uri
      }
    }
    /**
     * input event
     * @event DeviceBasicDataForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  updateDeviceType (value: DeviceTypeSelectValue): void {
    const newObj = Device.createFromObject(this.value)
    newObj.deviceTypeName = ''
    newObj.deviceTypeUri = ''
    if (value) {
      if (typeof value === 'string') {
        newObj.deviceTypeName = value
        newObj.deviceTypeUri = ''
        const deviceType = this.devicetypes.find(d => d.name === value)
        if (deviceType) {
          newObj.deviceTypeUri = deviceType.uri
        }
      } else {
        newObj.deviceTypeName = value.name
        newObj.deviceTypeUri = value.uri
      }
    }
    this.$emit('input', newObj)
  }

  updateManufacturer (value: ManufacturerSelectValue): void {
    const newObj = Device.createFromObject(this.value)
    newObj.manufacturerName = ''
    newObj.manufacturerUri = ''
    if (value) {
      if (typeof value === 'string') {
        newObj.manufacturerName = value
        newObj.manufacturerUri = ''
        const manufacturer = this.manufacturers.find(m => m.name === value)
        if (manufacturer) {
          newObj.manufacturerUri = manufacturer.uri
        }
      } else {
        newObj.manufacturerName = value.name
        newObj.manufacturerUri = value.uri
      }
    }
    this.$emit('input', newObj)
    this.loadSerialNumbers(newObj)
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.statusName and value.statusUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valueStatusItem (): ICvSelectItem | null {
    if (!this.value.statusName && !this.value.statusUri) {
      return null
    }
    const status = this.equipmentstatus.find(c => c.uri === this.value.statusUri)
    if (status) {
      return status
    }
    return {
      name: this.value.statusName,
      uri: this.value.statusUri,
      definition: '',
      id: null
    }
  }

  get valueDeviceTypeItem (): ICvSelectItem | null {
    if (!this.value.deviceTypeName && !this.value.deviceTypeUri) {
      return null
    }
    const deviceType = this.devicetypes.find(d => d.uri === this.value.deviceTypeUri)
    if (deviceType) {
      return deviceType
    }
    return {
      name: this.value.deviceTypeName,
      uri: this.value.deviceTypeUri,
      definition: '',
      id: null
    }
  }

  get valueManufacturerItem (): ICvSelectItem | null {
    if (!this.value.manufacturerName && !this.value.manufacturerUri) {
      return null
    }
    const manufacturer = this.manufacturers.find(m => m.uri === this.value.manufacturerUri)
    if (manufacturer) {
      return manufacturer
    }
    return {
      name: this.value.manufacturerName,
      uri: this.value.manufacturerUri,
      definition: '',
      id: null
    }
  }

  get deviceURN () {
    return createDeviceUrn(this.value, this.manufacturers)
  }

  get persistentIdentifierUrl (): string {
    if (!this.value.persistentIdentifier) {
      return ''
    }
    const pidBaseUrl = process.env.pidBaseUrl
    if (!pidBaseUrl) {
      return ''
    }
    return pidBaseUrl + '/' + this.value.persistentIdentifier
  }

  /**
   * validates the user input
   *
   * Note: we can't use 'validate' as a method name, so I used 'validateForm'
   *
   * @return {boolean} true when input is valid, otherwise false
   */
  public validateForm (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
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

  addNewKeyword () {
    if (!this.newKeyword) {
      return
    }
    const newObj = Device.createFromObject(this.value)
    if (!newObj.keywords.includes(this.newKeyword)) {
      newObj.keywords.push(this.newKeyword)
    }

    this.newKeyword = ''
    this.$emit('input', newObj)
  }

  addNewKeywordAndBlurNewKeywordField () {
    this.addNewKeyword()
    this.$nuxt.$nextTick(() => {
      (this.$refs.newKeywordField as Vue & { blur: () => void }).blur()
    })
  }

  removeKeyword (keyword: string) {
    const newObj = Device.createFromObject(this.value)
    newObj.keywords = newObj.keywords.filter(k => k !== keyword)
    this.$emit('input', newObj)
  }
}
</script>
