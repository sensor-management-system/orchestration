<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row align="center">
      <v-col>
        <v-row>
          <v-col>
            <label>Visibility / Permissions</label>
            <VisibilityChip
              v-model="value.visibility"
            />
            <PermissionGroupChips
              v-model="value.permissionGroups"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" :md="siteImagesShouldBeRendered ? 12 : 6">
            <label>Persistent identifier (PID)</label>
            <pid-tooltip
              :value="value.persistentIdentifier"
              show-button
            />
          </v-col>
          <v-col cols="12" :md="siteImagesShouldBeRendered ? 12 : 6">
            <label>Label</label>
            {{ value.label }}
          </v-col>
          <v-col cols="12" :md="siteImagesShouldBeRendered ? 12 : 6">
            <label>Part of</label>
            <span v-if="value.outerSiteId && site">
              <nuxt-link :to="'/sites/' + value.outerSiteId" target="_blank">{{ site.label }}</nuxt-link>
              <v-icon small>mdi-open-in-new</v-icon>
            </span>
            <span v-else>
              {{ null | orDefault }}
            </span>
          </v-col>
        </v-row>
        <v-divider class="my-4" />
        <v-row>
          <v-col cols="12" :md="siteImagesShouldBeRendered ? 12 : 6">
            <label>Usage</label>
            {{ value.siteUsageName | orDefault }}
            <a v-if="value.siteUsageUri" target="_blank" :href="value.siteUsageUri">
              <v-icon small>
                mdi-open-in-new
              </v-icon>
            </a>
          </v-col>
          <v-col cols="12" :md="siteImagesShouldBeRendered ? 12 : 6">
            <label>Type</label>
            {{ value.siteTypeName | orDefault }}
            <a v-if="value.siteTypeUri" target="_blank" :href="value.siteTypeUri">
              <v-icon small>
                mdi-open-in-new
              </v-icon>
            </a>
          </v-col>
        </v-row>
        <v-divider class="my-4" />
      </v-col>
      <v-col v-if="siteImagesShouldBeRendered" cols="12" md="6">
        <AttachmentImagesCarousel
          :value="value.images"
          :download-attachment="downloadAttachment"
          :proxy-url="proxyUrl"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Description</label>
        {{ value.description | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Website</label>
        {{ value.website | orDefault }}
        <a v-if="value.website.length > 0" :href="value.website" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-divider class="my-4" />
    <v-row v-if="value.geometry.length != 0">
      <v-col cols="12">
        <SiteMap :value="value.geometry" :readonly="true" />
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        <label>This site / lab does not have location data.</label>
        <v-subheader>
          Edit the site / lab to add coordinates.
        </v-subheader>
        <v-divider class="my-4" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Street</label>
        {{ [value.address.street, value.address.streetNumber] | sparseJoin(' ') | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>City</label>
        {{ [value.address.zipCode, value.address.city] | sparseJoin(' ') | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Country</label>
        {{ value.address.country | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Building - Room</label>
        {{ [value.address.building, value.address.room] | sparseJoin(' - ') | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="value.keywords">
      <v-col>
        <label>Keywords</label>
        <v-chip-group v-if="value.keywords.length">
          <v-chip v-for="keyword, idx in value.keywords" :key="idx" small>
            {{ keyword }}
          </v-chip>
        </v-chip-group>
        <span v-else>
          {{ '' | orDefault }}
        </span>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Site } from '@/models/Site'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import SiteMap from '@/components/sites/SiteMap.vue'

import VisibilityChip from '@/components/VisibilityChip.vue'
import AttachmentImagesCarousel from '@/components/shared/AttachmentImagesCarousel.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'

import { DownloadAttachmentAction, SearchSitesAction, SitesState } from '@/store/sites'
import { ProxyUrlAction } from '@/store/proxy'

@Component({
  components: {
    VisibilityChip,
    PermissionGroupChips,
    SiteMap,
    AttachmentImagesCarousel,
    PidTooltip
  },
  computed: {
    ...mapState('sites', ['sites'])
  },
  methods: {
    ...mapActions('sites', ['searchSites', 'downloadAttachment']),
    ...mapActions('proxy', ['proxyUrl'])
  }
})
export default class SiteBasicData extends Vue {
  @Prop({
    default: () => new Site(),
    required: true,
    type: Site
  })
  readonly value!: Site

  // vuex definition for typescript check
  sites!: SitesState['sites']
  searchSites!: SearchSitesAction
  downloadAttachment!: DownloadAttachmentAction
  proxyUrl!: ProxyUrlAction

  async mounted () {
    try {
      await this.searchSites()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to load sites')
    }
  }

  get site (): Site | null {
    if (!this.value.outerSiteId || !this.sites) {
      return null
    }
    const idx = this.sites.findIndex(s => s.id === this.value.outerSiteId)
    if (idx > -1) {
      return this.sites[idx]
    }
    return null
  }

  get siteImagesShouldBeRendered () {
    return this.value.images.length > 0
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";

.clickable {
    cursor: pointer;
}
</style>
