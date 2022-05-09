<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
      <v-col>
        <v-autocomplete
          label="Permission groups"
          :items="userGroups"
          ></v-autocomplete>
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
          :value="platformStatusName"
          :items="statusNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Status"
          @input="update('statusName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="platformTypeName"
          :items="platformTypeNames"
          :readonly="readonly"
          :disabled="readonly"
          label="Platform type"
          @input="update('platformTypeName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          :value="platformManufacturerName"
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
    <v-divider />
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
    <v-divider />
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
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import { Manufacturer } from '@/models/Manufacturer'

import { createPlatformUrn } from '@/modelUtils/urnBuilders'
import { mapGetters, mapState } from 'vuex'

@Component({
  computed:mapGetters('permissions',['userGroups'])
})
export default class PlatformBasicDataForm extends mixins(Rules) {
  private states: Status[] = []
  private manufacturers: Manufacturer[] = []
  private platformTypes: PlatformType[] = []

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
    this.$api.platformTypes.findAllPaginated().then((foundPlatformTypes) => {
      this.platformTypes = foundPlatformTypes
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Loading of platform types failed')
    })
  }

  update (key: string, value: string) {
    const newObj = Platform.createFromObject(this.value)

    switch (key) {
      case 'persistentIdentifier':
        newObj.persistentIdentifier = value
        break
      case 'shortName':
        newObj.shortName = value
        break
      case 'longName':
        newObj.longName = value
        break
      case 'statusName':
        newObj.statusName = value
        {
          const statusIndex = this.states.findIndex(s => s.name === value)
          if (statusIndex > -1) {
            newObj.statusUri = this.states[statusIndex].uri
          } else {
            newObj.statusUri = ''
          }
        }
        break
      case 'platformTypeName':
        newObj.platformTypeName = value
        {
          const platformTypeIndex = this.platformTypes.findIndex(t => t.name === value)
          if (platformTypeIndex > -1) {
            newObj.platformTypeUri = this.platformTypes[platformTypeIndex].uri
          } else {
            newObj.platformTypeUri = ''
          }
        }
        break
      case 'manufacturerName':
        newObj.manufacturerName = value
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
        newObj.model = value
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
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    this.$emit('input', newObj)
  }

  get manufacturerNames (): string[] {
    return this.manufacturers.map(m => m.name)
  }

  get statusNames (): string[] {
    return this.states.map(s => s.name)
  }

  get platformTypeNames (): string[] {
    return this.platformTypes.map(t => t.name)
  }

  get platformManufacturerName (): string {
    const manufacturerIndex = this.manufacturers.findIndex(m => m.uri === this.value.manufacturerUri)
    if (manufacturerIndex > -1) {
      return this.manufacturers[manufacturerIndex].name
    }
    return this.value.manufacturerName
  }

  get platformStatusName () {
    const statusIndex = this.states.findIndex(s => s.uri === this.value.statusUri)
    if (statusIndex > -1) {
      return this.states[statusIndex].name
    }
    return this.value.statusName
  }

  get platformTypeName () {
    const platformTypeIndex = this.platformTypes.findIndex(t => t.uri === this.value.platformTypeUri)
    if (platformTypeIndex > -1) {
      return this.platformTypes[platformTypeIndex].name
    }
    return this.value.platformTypeName
  }

  get platformURN () {
    return createPlatformUrn(this.value, this.platformTypes)
  }

  public validateForm (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>
