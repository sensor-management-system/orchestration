<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
          :rules="[rules.required, additionalRules.isValidEmailAddress]"
          @input="update('email', $event)"
        >
          <template slot="append">
            <a v-if="value.email.length > 0" :href="'mailto:' + value.email">
              <v-icon
                small
              >
                mdi-email
              </v-icon>
            </a>
          </template>
        </v-text-field>
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
              <v-icon
                small
              >
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
    <v-row>
      <v-col cols="12" md="9">
        <v-text-field
          v-if="readonly"
          :value="value.orcid"
          label="ORCID"
          placeholder="0000-1111-2222-3333"
          readonly
          disabled
        >
          <template #append>
            <a v-if="value.orcid.length > 0" :href="'https://orcid.org/' + value.orcid" target="_blank">
              <v-icon
                small
              >
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
        </v-text-field>
        <v-text-field
          v-else
          :value="value.orcid"
          label="ORCID"
          placeholder="0000-1111-2222-3333"
          :rules="[additionalRules.isValidOrcid]"
          @input="update('orcid', $event)"
        >
          <template #append>
            <a v-if="value.orcid.length > 0" :href="'https://orcid.org/' + value.orcid" target="_blank">
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
    <v-row>
      <v-col cols="12" md="9">
        <autocomplete-text-input
          :value="value.organization"
          label="Organization"
          endpoint="contact-organizations"
          @input="update('organization', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'

import Validator from '@/utils/validator'
import { isValidOrcid } from '@/utils/orcidHelpers'

import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'

@Component({
  components: {
    AutocompleteTextInput
  }
})
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

  private additionalRules = {
    isValidEmailAddress: Validator.isValidEmailAddress,
    isValidOrcid: (x: string | null) => {
      if (!x) {
        // The field is empty. It can be that there is no orcid, so we are fine.
        return true
      }
      // Now we can check all the nesty details of an orcid.
      // We use the function from the orcidHelpers file (which came from the Li2 development).
      if (!isValidOrcid(x)) {
        return 'The ORCID is not valid'
      }
      return true
    }
  }

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
      case 'organization':
        newObj.organization = value
        break
      case 'orcid':
        newObj.orcid = value
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
