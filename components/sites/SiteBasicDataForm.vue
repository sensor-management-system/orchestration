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
          :disabled-options="[visibilityPrivateValue]"
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
          :value="value.label"
          :readonly="readonly"
          :disabled="readonly"
          label="Label"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('label', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
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
        <v-select
          :value="value.epsgCode"
          class="required"
          :item-value="(x) => x.code"
          :item-text="(x) => x.text"
          :items="epsgCodes()"
          label="EPSG Code"
          :rules="[rules.required]"
          @change="update('epsgCode', $event)"
        />
      </v-col>
    </v-row>
    <v-divider
      class="my-4"
    />
    <v-row>
      <v-col cols="12" class="mb-4">
        <h4>Draw the site geometry</h4>
        <SiteMap :value="value.geometry" @updateCoords="update('geometry', $event)" />
      </v-col>
    </v-row>
    <h4>Address information</h4>
    <v-row>
      <v-col cols="8">
        <v-text-field
          :value="value.address.street"
          :readonly="readonly"
          :disabled="readonly"
          label="Street"
          placeholder="Street name"
          @input="update('address.street', $event)"
        />
      </v-col>
      <v-col cols="4">
        <v-text-field
          :value="value.address.streetNumber"
          :readonly="readonly"
          :disabled="readonly"
          label="Street number"
          placeholder="Street number"
          @input="update('address.streetNumber', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          :value="value.address.city"
          :readonly="readonly"
          :disabled="readonly"
          label="City"
          placeholder="City"
          @input="update('address.city', $event)"
        />
      </v-col>
      <v-col cols="2">
        <v-text-field
          :value="value.address.zipCode"
          :readonly="readonly"
          :disabled="readonly"
          label="Zip code"
          placeholder="Zip code"
          @input="update('address.zipCode', $event)"
        />
      </v-col>
      <v-col cols="4">
        <v-text-field
          :value="value.address.country"
          :readonly="readonly"
          :disabled="readonly"
          label="Country"
          placeholder="Country"
          @input="update('address.country', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          :value="value.address.building"
          :readonly="readonly"
          :disabled="readonly"
          label="Building"
          placeholder="Building"
          @input="update('address.building', $event)"
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          :value="value.address.room"
          :readonly="readonly"
          :disabled="readonly"
          label="Room"
          placeholder="Room"
          @input="update('address.room', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import { Rules } from '@/mixins/Rules'

import { ILatLng, Site } from '@/models/Site'
import { Status } from '@/models/Status'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { DetailedUserInfo } from '@/models/UserInfo'

import PermissionGroupSelect from '@/components/PermissionGroupSelect.vue'
import VisibilitySwitch from '@/components/VisibilitySwitch.vue'

import Validator from '@/utils/validator'
import SiteMap from '@/components/sites/SiteMap.vue'
import { VocabularyState } from '@/store/vocabulary'

@Component({
  components: {
    PermissionGroupSelect,
    VisibilitySwitch,
    SiteMap
  },
  methods: {
    ...mapState('vocabulary', ['epsgCodes'])

  }
})
export default class SiteBasicDataForm extends mixins(Rules) {
  private states: Status[] = []
  private userInfo: DetailedUserInfo | null = null
  private entityName: string = 'site'

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']

  @Prop({
    required: true,
    type: Site
  })
  readonly value!: Site

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  get pageRules (): {[index: string]: (a: any) => (boolean | string)} {
    return {
      validatePermissionGroups: Validator.validatePermissionGroups(false, this.entityName)
    }
  }

  get privateRules () {
    return [
      Validator.validateVisibility(this.value.visibility, [], this.entityName)
    ]
  }

  mounted () {
  }

  update (key: string, value: string|PermissionGroup[]) {
    const newObj = Site.createFromObject(this.value)

    switch (key) {
      case 'label':
        newObj.label = value as string
        break

      case 'description':
        newObj.description = value as string
        break

      case 'epsgCode':
        newObj.epsgCode = value as string
        break

      case 'geometry':
        newObj.geometry = value as unknown as ILatLng[]
        break

      case 'address.street':
        newObj.address.street = value as string
        break

      case 'address.streetNumber':
        newObj.address.streetNumber = value as string
        break

      case 'address.city':
        newObj.address.city = value as string
        break

      case 'address.zipCode':
        newObj.address.zipCode = value as string
        break

      case 'address.country':
        newObj.address.country = value as string
        break

      case 'address.building':
        newObj.address.building = value as string
        break

      case 'address.room':
        newObj.address.room = value as string
        break

      case 'visibility':
        switch (value) {
          case Visibility.Internal:
            newObj.visibility = Visibility.Internal
            break
          case Visibility.Public:
            newObj.visibility = Visibility.Public
            break
        }
        break
      case 'permissionGroups':
        newObj.permissionGroups = value as PermissionGroup[]
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }
    this.$emit('input', newObj)
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

  get visibilityPrivateValue (): Visibility {
    return Visibility.Private
  }
}
</script>
