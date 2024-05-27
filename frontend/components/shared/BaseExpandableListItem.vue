<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-hover
      v-slot="{ hover }"
    >
      <v-card
        :elevation="hover ? 6 : 2"
        class="ma-2"
        :color="backgroundColor"
      >
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
            <DotMenu
              v-if="$slots['dot-menu-items']"
            >
              <template #actions>
                <slot name="dot-menu-items" />
              </template>
            </DotMenu>
          </div>
          <v-row
            no-gutters
          >
            <v-col cols="10" class="text-subtitle-1">
              <slot :show="show" />
            </v-col>
            <v-col
              align-self="center"
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
        <v-expand-transition
          v-if="$slots['expandable']"
        >
          <v-card
            v-show="show"
            flat
            tile
            :color="expandableColor"
          >
            <v-card-text
              class="py-2 px-3"
            >
              <slot name="expandable" />
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </v-card>
    </v-hover>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DotMenu from '@/components/DotMenu.vue'

@Component({
  components: {
    DotMenu
  }
})
export default class BaseExpandableListItem extends Vue {
  @Prop({
    default: 'white',
    required: false,
    type: String
  })
  private expandableColor!: string

  @Prop({
    default: 'white',
    required: false,
    type: String
  })
  private backgroundColor!: string

  private show: boolean = false
}
</script>
