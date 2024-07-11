<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
          <v-list-item-title>
            {{ item.shortName }}
          </v-list-item-title>
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
