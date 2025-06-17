<!--
SPDX-FileCopyrightText: 2025
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-card v-if="isLoading || parsedReleaseNotes" style="width: 100%">
    <v-row no-gutters class="flex-no-wrap justify-space-between">
      <v-col cols="12">
        <div class="primary white--text rounded rounded-b-0">
          <v-card-title
            class="text-h5 font-weight-bold"
          >
            Release Notes
            <v-spacer />
            <v-btn v-if="linkToReleaseNotes" :href="linkToReleaseNotes" target="_blank" icon>
              <v-icon class="white--text">
                mdi-open-in-new
              </v-icon>
            </v-btn>
          </v-card-title>
        </div>
        <v-divider />

        <v-card-text class="primary_text--text">
          <v-list v-if="isLoading">
            <span>Latest release</span>
            <v-divider />
            <v-skeleton-loader type="list-item-two-line" />
            <span>Older releases</span>
            <v-divider />
            <div v-if="isLoading">
              <v-skeleton-loader type="list-item-two-line" />
              <v-divider class="my-1 mx-4" />
              <v-skeleton-loader type="list-item-two-line" />
              <v-divider class="my-1 mx-4" />
              <v-skeleton-loader type="list-item-two-line" />
              <v-divider class="my-1 mx-4" />
            </div>
          </v-list>

          <v-list v-else-if="parsedReleaseNotes.length != 0">
            <span>Latest release</span>
            <v-divider />
            <ReleaseNotesEntry :release-notes="latestRelease" initially-opened />
            <span>Older releases</span>
            <v-divider />

            <div v-for="release in oldReleasesToShow" :key="release.version">
              <ReleaseNotesEntry :release-notes="release" />
              <v-divider class="my-1 mx-4" />
            </div>

            <v-list-item
              v-if="amountOfOldReleasesToShow < oldReleases.length"
              class="justify-center"
              @click="amountOfOldReleasesToShow += 3"
            >
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-chevron-down
                  </v-icon>
                </template>
                <span>Load more</span>
              </v-tooltip>
            </v-list-item>
          </v-list>

          <span v-else>
            No release notes available.
          </span>
        </v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ReleaseNotesEntry from '@/components/ReleaseNotesEntry.vue'
import { Release } from '@/models/ReleaseNotes'

@Component({
  components: { ReleaseNotesEntry, BaseExpandableListItem }
})
export default class ReleaseNotes extends Vue {
  private isLoading: boolean = true
  private parsedReleaseNotes: Release[] = []

  @Prop({
    type: Number,
    default: 3
  })
  private readonly initialAmountOfOlderReleases!: number

  @Prop({
    type: String,
    required: false
  })
  private readonly linkToReleaseNotes!: string|null

  private amountOfOldReleasesToShow = this.initialAmountOfOlderReleases

  async created () {
    try {
      this.isLoading = true
      this.parsedReleaseNotes = await this.$api.releaseNotes.findAllReleases()
      if (!this.parsedReleaseNotes || this.parsedReleaseNotes.length === 0) {
        this.$emit('close')
      }
    } catch (_) {
      this.$emit('close')
      this.$store.commit('snackbar/setWarning', 'Failed to load release notes')
    } finally {
      this.isLoading = false
    }
  }

  get latestRelease (): Release | null {
    if (!this.parsedReleaseNotes) {
      return null
    }
    return this.parsedReleaseNotes[0]
  }

  get oldReleases (): Release[] {
    return this.parsedReleaseNotes.slice(1)
  }

  get oldReleasesToShow (): Release[] {
    return this.oldReleases.slice(0, Math.min(this.amountOfOldReleasesToShow, this.oldReleases.length))
  }
}
</script>
