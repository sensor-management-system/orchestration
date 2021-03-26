<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
  <div>
    <CustomFieldCard
      v-model="value"
    >
      <template #actions>
        <v-btn
          v-if="isLoggedIn"
          color="primary"
          text
          small
          nuxt
          :to="'/devices/' + deviceId + '/customfields/' + value.id + '/edit'"
        >
          Edit
        </v-btn>
        <v-menu
          v-if="isLoggedIn"
          close-on-click
          close-on-content-click
          offset-x
          left
          z-index="999"
        >
          <template v-slot:activator="{ on }">
            <v-btn
              data-role="property-menu"
              icon
              small
              v-on="on"
            >
              <v-icon
                dense
                small
              >
                mdi-dots-vertical
              </v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              dense
              @click="openDeleteDialog"
            >
              <v-list-item-content>
                <v-list-item-title
                  class="red--text"
                >
                  <v-icon
                    left
                    small
                    color="red"
                  >
                    mdi-delete
                  </v-icon>
                  Delete
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </CustomFieldCard>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { CustomTextField } from '@/models/CustomTextField'
import CustomFieldCard from '@/components/CustomFieldCard.vue'

@Component({
  components: {
    CustomFieldCard
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  get field (): CustomTextField {
    return this.value
  }

  set field (value: CustomTextField) {
    this.$emit('input', value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  openDeleteDialog (): void {
    this.$emit('openDeleteDialog', this.value.id)
  }
}
</script>
