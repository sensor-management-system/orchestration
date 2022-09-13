<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
          :rules="[pageRules.validateVisibility]"
          :readonly="readonly"
          :entity-name="entityName"
          @input="update('visibility', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <permission-group-select
          v-show="!value.isPrivate"
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
          :readonly="readonly"
          :disabled="readonly"
          label="Persistent identifier (PID)"
          :placeholder="persistentIdentifierPlaceholder"
          @input="update('persistentIdentifier', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.shortName"
          :readonly="readonly"
          :disabled="readonly"
          label="Short name"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('shortName', $event)"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          :value="value.longName"
          :readonly="readonly"
          :disabled="readonly"
          label="Long name"
          @input="update('longName', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
          :items="states"
          item-name="name"
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
          </template>
          <template #item="data">
            <template v-if="typeof data.item !== 'object'">
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
        </v-combobox>
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="deviceTypeName"
          :items="deviceTypeNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Device type"
          @input="update('deviceTypeName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="deviceManufacturerName"
          :items="manufacturerNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Manufacturer"
          @input="update('manufacturerName', $event)"
        />
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
          :placeholder="serialNumberPlaceholder"
          @input="update('serialNumber', $event)"
        />
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
      <v-col cols="12" md="3">
        <v-checkbox
          :input-value="value.dualUse"
          :readonly="readonly"
          :disabled="readonly"
          label="Dual use"
          hint="can be used for military aims"
          :persistent-hint="true"
          color="red darken-3"
          @change="update('dualUse', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Device } from '@/models/Device'
import { DeviceType } from '@/models/DeviceType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { DetailedUserInfo } from '@/models/UserInfo'
import { ICvSelectItem, hasDefinition } from '@/models/CvSelectItem'

import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'

import { createDeviceUrn } from '@/modelUtils/urnBuilders'

import Validator from '@/utils/validator'

type StatusSelectValue = Status | string | undefined

@Component({
  components: {
    PermissionGroupSelect,
    VisibilitySwitch
  }
})
export default class DeviceBasicDataForm extends mixins(Rules) {
  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private deviceTypes: DeviceType[] = []
  private permissionGroups: PermissionGroup[] = []
  private userInfo: DetailedUserInfo | null = null
  private entityName: string = 'device'

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

  get pageRules (): {[index: string]: (a: any) => (boolean | string)} {
    return {
      validateVisibility: Validator.validateVisibility(this.value.permissionGroups, this.entityName),
      validatePermissionGroups: Validator.validatePermissionGroups(this.value.isPrivate, this.entityName)
    }
  }

  mounted () {
    this.$api.states.findAllPaginated().then((foundStates) => {
      this.states = foundStates
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of states failed')
    })
    this.$api.manufacturer.findAllPaginated().then((foundManufacturers) => {
      this.manufacturers = foundManufacturers
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of manufactures failed')
    })
    this.$api.deviceTypes.findAllPaginated().then((foundDeviceTypes) => {
      this.deviceTypes = foundDeviceTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of device types failed')
    })
  }

  update (key: string, value: string|PermissionGroup[]) {
    const newObj = Device.createFromObject(this.value)

    switch (key) {
      case 'persistentIdentifier':
        newObj.persistentIdentifier = value as string
        break
      case 'shortName':
        newObj.shortName = value as string
        break
      case 'longName':
        newObj.longName = value as string
        break
      case 'deviceTypeName':
        newObj.deviceTypeName = value as string
        {
          const deviceTypeIndex = this.deviceTypes.findIndex(t => t.name === value)
          if (deviceTypeIndex > -1) {
            newObj.deviceTypeUri = this.deviceTypes[deviceTypeIndex].uri
          } else {
            newObj.deviceTypeUri = ''
          }
        }
        break
      case 'manufacturerName':
        newObj.manufacturerName = value as string
        {
          const manufacturerIndex = this.manufacturers.findIndex(m => m.name === value)
          if (manufacturerIndex > -1) {
            newObj.manufacturerUri = this.manufacturers[manufacturerIndex].uri
          } else {
            newObj.manufacturerUri = ''
          }
        }
        break
      case 'model':
        newObj.model = value as string
        break
      case 'description':
        newObj.description = value as string
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
      case 'dualUse':
        // Boolean(true) => true
        // Boolean(false) => false
        // but Boolean('false') => true
        // due to the change handler, this is already a boolean
        // only typescript doesn't know about this
        // so we can be sure to go with it here
        newObj.dualUse = Boolean(value)
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
        const state = this.states.find(s => s.name === value)
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
    return this.states.map(s => s.name)
  }

  get deviceTypeNames (): string[] {
    return this.deviceTypes.map(t => t.name)
  }

  get deviceManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get deviceStatusName () {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.value.statusName
  }

  get deviceTypeName () {
    const deviceTypeIndex = this.deviceTypes.findIndex(t => t.uri === this.value.deviceTypeUri)
    if (deviceTypeIndex > -1) {
      return this.deviceTypes[deviceTypeIndex].name
    }
    return this.value.deviceTypeName
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
    const status = this.states.find(c => c.uri === this.value.statusUri)
    if (status) {
      return status
    }
    return {
      name: this.value.statusName,
      uri: this.value.statusUri,
      definition: ''
    }
  }

  get deviceURN () {
    return createDeviceUrn(this.value, this.manufacturers)
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
}
</script>
