<!--
SPDX-FileCopyrightText: 2025
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <BaseExpandableListItem v-if="releaseNotes" ref="listItem" no-elevation>
    <template #header>
      {{ releaseNotes.date }}
    </template>
    <template #default>
      <span class="text-h6 mr-2">{{ releaseNotes.tag }}</span><span v-if="isCurrentVersion(releaseNotes.tag)">(Current version)</span>
    </template>
    <template #expandable>
      <div v-for="(entry, i) in changeLogEntryItems" :key="i">
        <span
          v-if="releaseNotes.notes[entry.key]?.length != 0"
          class="font-weight-bold d-flex align-content-center"
        >
          <v-icon
            small
            class="mr-1"
          >
            {{ entry.icon }}
          </v-icon>
          {{ entry.text }}
        </span>
        <ul class="mb-2">
          <li v-for="(note, j) in releaseNotes.notes[entry.key]" :key="j">
            {{ note.text }}
            <v-btn
              v-if="note.linkToWiki"
              x-small
              icon
              :href="note.linkToWiki"
              target="_blank"
              title="View in Wiki"
            >
              <v-icon x-small>
                >
                message-question-outline
              </v-icon>
            </v-btn>
            <v-btn
              v-if="note.linkToMergeRequest"
              x-small
              icon
              :href="note.linkToMergeRequest"
              target="_blank"
              title="View Merge Request"
            >
              <v-icon x-small>
                mdi-gitlab
              </v-icon>
            </v-btn>
          </li>
        </ul>
      </div>
    </template>
  </BaseExpandableListItem>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import { Release } from '@/models/ReleaseNotes'

@Component({
  components: { BaseExpandableListItem }
})
export default class ReleaseNotesEntry extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private releaseNotes!: Release

  @Prop({
    required: false,
    type: Boolean,
    default: false
  })
  private initiallyOpened!: boolean

  mounted () {
    if (this.initiallyOpened) {
      (this.$refs.listItem as BaseExpandableListItem).open()
    }
  }

  private changeLogEntryItems = [
    { key: 'added', icon: 'mdi-tag-plus', text: 'Added' },
    { key: 'changed', icon: 'mdi-tag-edit', text: 'Changed' },
    { key: 'fixed', icon: 'mdi-tag-check', text: 'Fixed' }
  ]

  isCurrentVersion (tag: string): boolean {
    return process.env.version === tag
  }
}
</script>
