<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-container v-if="!(actions.length === 0 && !isFilterUsed)">
        <ConfigurationActionsFilter
          v-model="filter"
        />
      </v-container>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
    <v-card
      flat
    >
      <hint-card v-if="actions.length === 0 && !isFilterUsed">
        There are no actions for this configuration.
      </hint-card>
      <hint-card v-if="actions.length === 0 && isFilterUsed">
        There are no actions that match the filter criteria.
      </hint-card>
      <v-card-text
        v-if="actions.length > 0"
      >
        <v-timeline dense>
          <v-timeline-item
            v-for="action in actions"
            :key="action.key"
            :color="action.color"
            :icon="action.icon"
            class="mb-4"
          >
            <ConfigurationsTimelineActionCard
              :action="action"
              :is-public="isPublic"
              @open-attachment="openAttachment"
            />
          </v-timeline-item>
        </v-timeline>
        <v-card-actions
          v-if="actions.length > 3"
        >
          <v-spacer />
          <v-btn
            v-if="editable"
            color="primary"
            small
            :to="'/configurations/' + configurationId + '/actions/new'"
          >
            Add Action
          </v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
    <download-dialog
      v-model="showDownloadDialog"
      :filename="selectedAttachmentFilename"
      :url="selectedAttachmentUrl"
      @cancel="closeDownloadDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapGetters, mapActions, mapState } from 'vuex'

import {
  ConfigurationsState,
  DownloadAttachmentAction,
  ConfigurationFilter, FilteredActionsGetter
} from '@/store/configurations'

import HintCard from '@/components/HintCard.vue'
import ConfigurationsTimelineActionCard from '@/components/configurations/ConfigurationsTimelineActionCard.vue'
import DownloadDialog from '@/components/shared/DownloadDialog.vue'

import { Attachment } from '@/models/Attachment'
import { Visibility } from '@/models/Visibility'

import { getLastPathElement } from '@/utils/urlHelpers'
import ConfigurationActionsFilter from '@/components/configurations/ConfigurationActionsFilter.vue'
import { LoadConfigurationGenericActionTypesAction } from '@/store/vocabulary'

@Component({
  components: {
    ConfigurationActionsFilter,
    ConfigurationsTimelineActionCard,
    HintCard,
    DownloadDialog
  },
  computed: {
    ...mapGetters('configurations', ['filteredActions']),
    ...mapState('configurations', ['configuration'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadConfigurationGenericActionTypes']),
    ...mapActions('configurations', ['downloadAttachment'])
  }
})
export default class ConfigurationShowActionPage extends Vue {
  private filter: ConfigurationFilter = {
    selectedActionTypes: [],
    selectedYears: [],
    selectedContacts: []
  }

  @InjectReactive()
  private editable!: boolean

  filteredActions!: FilteredActionsGetter
  loadConfigurationGenericActionTypes!: LoadConfigurationGenericActionTypesAction
  private readonly configuration!: ConfigurationsState['configuration']
  private downloadAttachment!: DownloadAttachmentAction

  private showDownloadDialog: boolean = false
  private attachmentToDownload: Attachment | null = null

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get actions () {
    return this.filteredActions(this.filter)
  }

  get isFilterUsed () {
    return this.filter.selectedActionTypes.length > 0 || this.filter.selectedYears.length > 0 || this.filter.selectedContacts.length > 0
  }

  async created () {
    await this.loadConfigurationGenericActionTypes()
  }

  initDowloadDialog (attachment: Attachment) {
    this.attachmentToDownload = attachment
    this.showDownloadDialog = true
  }

  closeDownloadDialog () {
    this.showDownloadDialog = false
    this.attachmentToDownload = null
  }

  openAttachment (attachment: Attachment) {
    this.initDowloadDialog(attachment)
  }

  get selectedAttachmentFilename (): string {
    if (this.attachmentToDownload) {
      return getLastPathElement(this.attachmentToDownload.url)
    }
    return 'attachment'
  }

  async selectedAttachmentUrl (): Promise<string | null> {
    if (!this.attachmentToDownload) {
      return null
    }
    try {
      const blob = await this.downloadAttachment(this.attachmentToDownload.url)
      const url = window.URL.createObjectURL(blob)
      return url
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Attachment could not be loaded')
    }
    return null
  }

  get isPublic (): boolean {
    return (this.configuration?.visibility === Visibility.Public) || false
  }
}
</script>

<style scoped>

</style>
