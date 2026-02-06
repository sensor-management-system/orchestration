<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <span class="text-caption text--secondary">from:</span> {{ from | toUtcDateTimeStringHHMM }}
    <span class="text-caption text--secondary">to:</span> {{ to | toUtcDateTimeStringHHMM('open end') }}
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

@Component({})
export default class TsmLinkingDates extends Vue {
  @Prop({
    required: false
  })
  private from!: DateTime | null

  @Prop({
    required: false
  })
  private to!: DateTime | null
}
</script>
