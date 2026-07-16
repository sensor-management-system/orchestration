<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form ref="basicForm" @submit.prevent>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            :value="value.name"
            label="Name"
            required
            class="required"
            :rules="[rules.required]"
            @input="update('name', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            :value="value.ror"
            label="ROR"
            @input="update('ror', $event)"
          />
          <template #append>
            <a v-if="value.ror.length > 0" :href="value.ror" target="_blank">
              <v-icon
                small
              >
                mdi-open-in-new
              </v-icon>
            </a>
          </template>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            :value="value.abbreviation"
            label="Abbreviation"
            :rules="[additionalRules.max8Chars]"
            @input="update('abbreviation', $event)"
          />
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { ExternalUrlLinkMixin } from '@/mixins/ExternalUrlLinkMixin'

import { Rules } from '@/mixins/Rules'
import { Organization } from '@/models/Organization'

@Component({
})
export default class OrganizationBasicDataForm extends mixins(Rules, ExternalUrlLinkMixin) {
  @Prop({
    required: true,
    type: Organization
  })
  readonly value!: Organization

  private additionalRules = {
    max8Chars: (x: string | null) => {
      if (!x) {
        return true
      }
      if (x.length > 8) {
        return 'Maximum length is 8 characters'
      }
      return true
    }
  }

  update (key: string, value: string) {
    const newObj = Organization.createFromObject(this.value)
    switch (key) {
      case 'name':
        newObj.name = value
        break
      case 'ror':
        newObj.ror = value
        break
      case 'abbreviation':
        newObj.abbreviation = value
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
