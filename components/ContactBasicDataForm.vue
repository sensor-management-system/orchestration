<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.givenName"
          label="Given name"
          :readonly="readonly"
          :disabled="readonly"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('givenName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="value.familyName"
          label="Family name"
          :readonly="readonly"
          :disabled="readonly"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('familyName', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-text-field
          :value="value.email"
          label="E-mail"
          type="email"
          :readonly="readonly"
          :disabled="readonly"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('email', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-text-field
          v-if="readonly"
          :value="value.website"
          label="Website"
          placeholder="https://"
          type="url"
          :readonly="true"
          :disabled="true"
        >
          <template slot="append">
            <a v-if="value.website.length > 0" :href="value.website" target="_blank">
              <v-icon>
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
        </v-text-field>
        <v-text-field
          v-else
          :value="value.website"
          label="Website"
          placeholder="https://"
          type="url"
          @input="update('website', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

@Component
export default class ContactBasicDataForm extends mixins(Rules) {
  @Prop({
    required: true,
    type: Contact
  })
  readonly value!: Contact

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  update (key: string, value: string) {
    const newObj = Contact.createFromObject(this.value)
    switch (key) {
      case 'givenName':
        newObj.givenName = value
        break
      case 'familyName':
        newObj.familyName = value
        break
      case 'email':
        newObj.email = value
        break
      case 'website':
        newObj.website = value
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    this.$emit('input', newObj)
  }

  public validateForm (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }
}

</script>
