<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-list-item

        :key="index"
      >
        <v-list-item-content>
          <v-list-item-title v-text="item.shortName" />
        </v-list-item-content>
      </v-list-item>
      <v-card-text
        class="py-2 px-3"
        @click.stop.prevent="show = !show"
      >
        <div
          v-if="$slots['header']"
          class="d-flex align-center"
        >
          <slot name="header" />
          <v-spacer />
        </div>
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            <slot />
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <slot name="actions" />
            <DotMenu
              v-if="!$slots['header'] && $slots['dot-menu-items']"
            >
              <template #actions>
                <slot name="dot-menu-items" />
              </template>
            </DotMenu>
            <v-btn
              v-if="$slots['expandable']"
              icon
              small
              @click.stop.prevent="show = !show"
            >
              <v-icon
                small
              >
                {{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DotMenu from '@/components/DotMenu.vue'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'

@Component({
  components: {
    DotMenu
  }
})
export default class BaseMountListItem extends Vue {
  @Prop({
    default: 'white',
    required: false,
    type: String
  })
  private expandableColor!: string

  @Prop({
    required: true,
    type: Object
  })
  private item!: Platform | Device

  @Prop({
    required: true,
    type: Number
  })
  private index!: number

  private show: boolean = false
}
</script>
