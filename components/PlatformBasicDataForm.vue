<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
          required
          @input="update('permissionGroups', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="platformURN"
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
        >
          <template #append>
            <a
              v-if="value.persistentIdentifier"
              :href="value.persistentIdentifierUrl"
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
          endpoint="platform-short-names"
          @input="update('shortName', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <autocomplete-text-input
          :value="value.longName"
          :readonly="readonly"
          :disabled="readonly"
          label="Long name"
          endpoint="platform-long-names"
          @input="update('longName', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
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
      <v-col cols="12" md="3">
        <combobox
          :value="platformTypeName"
          :items="platformTypeNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Platform type"
          @input="update('platformTypeName', $event)"
        >
          <template #append-outer>
            <v-btn icon @click="showNewPlatformTypeDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
        </combobox>
      </v-col>
      <v-col cols="12" md="3">
        <combobox
          :value="platformManufacturerName"
          :items="manufacturerNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Manufacturer"
          @input="update('manufacturerName', $event)"
        >
          <template #append-outer>
            <v-btn icon @click="showNewManufacturerDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
        </combobox>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.model"
          :readonly="readonly"
          :disabled="readonly"
          label="Model"
          @input="update('model', $event)"
        />
      </v-col>
    </v-row>
    <v-divider class="my-4" />
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
    <v-divider class="my-4" />
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
    <platform-type-dialog
      v-model="showNewPlatformTypeDialog"
      :initial-term="platformTypeName"
      @aftersubmit="setPlatformType"
    />
    <status-dialog
      v-model="showNewStatusDialog"
      :initial-term="platformStatusName"
      @aftersubmit="updateStatus"
    />
    <manufacturer-dialog
      v-model="showNewManufacturerDialog"
      :initial-term="platformManufacturerName"
      @aftersubmit="setManufacturer"
    />
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { Rules } from '@/mixins/Rules'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { DetailedUserInfo } from '@/models/UserInfo'
import { ICvSelectItem, hasDefinition } from '@/models/CvSelectItem'

import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'
import PlatformTypeDialog from '@/components/platforms/PlatformTypeDialog.vue'
import ManufacturerDialog from '@/components/shared/ManufacturerDialog.vue'
import StatusDialog from '@/components/shared/StatusDialog.vue'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'
import Combobox from '@/components/shared/Combobox.vue'

import { createPlatformUrn } from '@/modelUtils/urnBuilders'

import Validator from '@/utils/validator'
import { LoadEquipmentstatusAction, LoadManufacturersAction, LoadPlatformtypesAction, VocabularyState } from '@/store/vocabulary'

type StatusSelectValue = Status | string | undefined

@Component({
  components: {
    ManufacturerDialog,
    PermissionGroupSelect,
    PlatformTypeDialog,
    StatusDialog,
    VisibilitySwitch,
    AutocompleteTextInput,
    Combobox
  },
  computed: {
    ...mapGetters('permissions', ['userGroups']),
    ...mapState('vocabulary', ['platformtypes', 'manufacturers', 'equipmentstatus'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadPlatformtypes', 'loadManufacturers', 'loadEquipmentstatus'])
  }
})
export default class PlatformBasicDataForm extends mixins(Rules) {
  private permissionGroups: PermissionGroup[] = []
  private isPermissionGroupsLoaded: boolean = false
  private userInfo: DetailedUserInfo | null = null
  private entityName = 'platform'
  private platformtypes!: VocabularyState['platformtypes']
  private manufacturers !: VocabularyState['manufacturers']
  private equipmentstatus !: VocabularyState['equipmentstatus']
  private showNewPlatformTypeDialog = false
  private showNewStatusDialog = false
  private showNewManufacturerDialog = false
  private serialNumbersInUse: string[] = []
  private initialSerialNumber = ''

  loadPlatformtypes !: LoadPlatformtypesAction
  loadManufacturers !: LoadManufacturersAction
  loadEquipmentstatus !: LoadEquipmentstatusAction

  @Prop({
    required: true,
    type: Platform
  })
  readonly value!: Platform

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

  get isSerialNumberInUse (): boolean {
    return this.serialNumbersInUse.includes(this.value.serialNumber)
  }

  get serialNumberHint () {
    return this.isSerialNumberInUse ? 'Another platform already has an equal serial number.' : ''
  }

  async loadSerialNumbers (platform: Platform | null = null) {
    if (!platform) {
      platform = this.value
    }
    const platformId = platform?.id
    const params: any = {
      manufacturerName: platform?.manufacturerName,
      model: platform?.model
    }
    if (platformId) {
      params.ignore = platformId
    }
    this.serialNumbersInUse = await this.$api.autocomplete.getPlatformSerialNumbers(params)
  }

  async fetch () {
    try {
      await Promise.all([
        this.loadSerialNumbers(),
        this.loadEquipmentstatus(),
        this.loadManufacturers(),
        this.loadPlatformtypes()
      ])
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of controlled vocabulary failed')
    }
  }

  setPlatformType (platformType: PlatformType) {
    this.update('platformTypeName', platformType.name)
  }

  setManufacturer (manufacturer: Manufacturer) {
    this.update('manufacturerName', manufacturer.name)
  }

  update (key: string, value: any) {
    const newObj = Platform.createFromObject(this.value)
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
        newObj.shortName = value
        break
      case 'longName':
        newObj.longName = value
        break
      case 'platformTypeName':
        newObj.platformTypeName = value
        {
          const platformTypeIndex = this.platformtypes.findIndex(t => t.name === value)
          if (platformTypeIndex > -1) {
            newObj.platformTypeUri = this.platformtypes[platformTypeIndex].uri
          } else {
            newObj.platformTypeUri = ''
          }
        }
        break
      case 'manufacturerName':
        newObj.manufacturerName = value || ''
        {
          const manufacturerIndex = this.manufacturers.findIndex(m => m.name === value)
          if (manufacturerIndex > -1) {
            newObj.manufacturerUri = this.manufacturers[manufacturerIndex].uri
          } else {
            newObj.manufacturerUri = ''
          }
        }
        updateSerialNumberCheck = true
        break
      case 'model':
        newObj.model = value
        updateSerialNumberCheck = true
        break
      case 'description':
        newObj.description = value
        break
      case 'website':
        newObj.website = value
        break
      case 'serialNumber':
        newObj.serialNumber = value
        break
      case 'inventoryNumber':
        newObj.inventoryNumber = value
        break
      case 'permissionGroups':
        newObj.permissionGroups = value
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
    const newObj = Platform.createFromObject(this.value)
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

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get statusNames (): string[] {
    return this.equipmentstatus.map(s => s.name)
  }

  get platformTypeNames (): string[] {
    return this.platformtypes.map(t => t.name)
  }

  get platformManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get platformStatusName () {
    const statusIndex = this.equipmentstatus.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.equipmentstatus[statusIndex].name
    }
    return this.value.statusName
  }

  get platformTypeName () {
    const platformTypeIndex = this.platformtypes.findIndex(t => t.uri === this.value.platformTypeUri)
    if (platformTypeIndex > -1) {
      return this.platformtypes[platformTypeIndex].name
    }
    return this.value.platformTypeName
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

  get platformURN () {
    return createPlatformUrn(this.value, this.platformtypes)
  }

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
}
</script>
