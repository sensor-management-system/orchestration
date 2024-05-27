<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
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
              :value="value.permissionGroup ? [value.permissionGroup] : []"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 12 : 6">
            <label>Persistent identifier (PID)</label>
            <pid-tooltip
              :value="value.persistentIdentifier"
              show-button
            />
          </v-col>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 6 : 3">
            <label>Label</label>
            {{ value.label }}
          </v-col>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 6 : 3">
            <label>Status</label>
            {{ value.status | orDefault }}
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <label>Start date</label>
            <span v-if="value.startDate">
              {{ value.startDate | toUtcDateTimeStringHHMM | orDefault }}
              <span class="text-caption text--secondary">(UTC)</span>
            </span>
            <span v-else>
              {{ null | orDefault }}
            </span>
          </v-col>
          <v-col cols="12" md="6">
            <label>End date</label>
            <span v-if="value.endDate">
              {{ value.endDate | toUtcDateTimeStringHHMM | orDefault }}
              <span class="text-caption text--secondary">(UTC)</span>
            </span>
            <span v-else>
              {{ null | orDefault }}
            </span>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 6 : 3">
            <label>Project</label>
            {{ value.project | orDefault }}
          </v-col>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 6 : 3">
            <label>Campaign</label>
            {{ value.campaign | orDefault }}
          </v-col>
          <v-col cols="12" :md="configurationImagesShouldBeRendered ? 6 : 3">
            <label>Site / Lab</label>
            <span v-if="value.siteId && site">
              <nuxt-link :to="'/sites/' + value.siteId" target="_blank">{{ site.label }}</nuxt-link><v-icon small>mdi-open-in-new</v-icon>
            </span>
            <span v-else>
              {{ null | orDefault }}
            </span>
          </v-col>
        </v-row>
      </v-col>
      <v-col v-if="configurationImagesShouldBeRendered" cols="12" md="6">
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
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { Configuration } from '@/models/Configuration'
import { Site } from '@/models/Site'

import { SearchSitesAction, SitesState } from '@/store/sites'
import { DownloadAttachmentAction } from '@/store/configurations'
import { ProxyUrlAction } from '@/store/proxy'

import DateTimePicker from '@/components/DateTimePicker.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'
import PidTooltip from '@/components/shared/PidTooltip.vue'
import AttachmentImagesCarousel from '@/components/shared/AttachmentImagesCarousel.vue'
import QrCodeDialog from '@/components/QrCodeDialog.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'

@Component({
  components: {
    DateTimePicker,
    PermissionGroupChips,
    PidTooltip,
    QrCodeDialog,
    VisibilityChip,
    AttachmentImagesCarousel
  },
  computed: mapState('sites', ['sites']),
  methods: {
    ...mapActions('sites', ['searchSites']),
    ...mapActions('configurations', ['downloadAttachment']),
    ...mapActions('proxy', ['proxyUrl'])
  }
})
export default class ConfigurationsBasicDataForm extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

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

  // @ts-ignore
  update (key: string, value: any) {
    // @ts-ignore
    if (typeof this.value[key] !== 'undefined') {
      const newObj = Configuration.createFromObject(this.value)
      // @ts-ignore
      newObj[key] = value
      this.$emit('input', newObj)
    }
  }

  get site (): Site | null {
    if (!this.value.siteId || !this.sites) {
      return null
    }
    const idx = this.sites.findIndex(s => s.id === this.value.siteId)
    if (idx > -1) {
      return this.sites[idx]
    }
    return null
  }

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }

  get configurationImagesShouldBeRendered () {
    return this.value.images.length > 0
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
