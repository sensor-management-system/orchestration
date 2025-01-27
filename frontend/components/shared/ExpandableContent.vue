<!--
SPDX-FileCopyrightText: 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div class="d-inline">
    <div
      style="cursor: pointer"
      :title="opened ? 'show less' : 'show more'"
      @click.stop.prevent="opened = !opened"
    >
      <v-icon class="arrowIcon" :color="iconColor" :class="{ 'rotate': opened }">
        {{ closedIcon }}
      </v-icon>
      <slot name="header" :opened="opened" />
    </div>
    <div>
      <v-expand-transition>
        <div v-if="opened" :class="{ 'indent': indent }">
          <slot name="default" />
        </div>
      </v-expand-transition>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

@Component
export default class ExpandableContent extends Vue {
  @Prop({
    default: 'mdi-menu-right',
    required: false,
    type: String
  })
  private closedIcon!: string

  @Prop({
    required: false,
    type: String
  })
  private iconColor!: string

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private indent!: boolean

  private opened: boolean = false
}
</script>

<style scoped>
.arrowIcon {
    transition: transform .15s ease-out !important;
}

.arrowIcon.rotate {
    transform: rotate(90deg);
}

.indent {
  position: relative;
  left: 2em;
}
</style>
