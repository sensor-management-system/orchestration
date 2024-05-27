<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions class="pl-0">
      <label v-if="lastUpdateInformation">
        Last update of export control information by  {{ lastUpdateInformation.contact }} at {{ lastUpdateInformation.date | toUtcDateTimeString }}
      </label>
      <v-spacer />
      <v-btn
        v-if="manufacturerModelId && canHandleExportControl"
        color="primary"
        small
        nuxt
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
      >
        Inspect
      </v-btn>
    </v-card-actions>
    <export-control-basic-data
      v-if="exportControl"
      v-model="exportControl"
      :show-internal-note="false"
    />

    <v-card v-if="publicExportControlAttachments.length > 0" flat class="pt-6">
      <label>Attachments</label>
      <base-list :list-items="publicExportControlAttachments">
        <template #list-item="{ item }">
          <attachment-list-item
            :attachment="item"
            :is-public="true"
          />
        </template>
      </base-list>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import { DateTime } from 'luxon'

import { PlatformsState, LoadExportControlAction, LoadManufacturerModelIdAction } from '@/store/platforms'
import { CanHandleExportControlGetter } from '@/store/permissions'
import { LoadExportControlAttachmentsAction, LoadExportControlCreatedAndUpdatedByContactsAction, ManufacturermodelsState, PublicExportControlAttachmentsGetter, SetExportControlAttachmentsMutation } from '@/store/manufacturermodels'
import { SetLoadingAction } from '@/store/progressindicator'

import AttachmentListItem from '@/components/shared/AttachmentListItem.vue'
import BaseList from '@/components/shared/BaseList.vue'
import ExportControlBasicData from '@/components/manufacturerModels/ExportControlBasicData.vue'
import { Contact } from '@/models/Contact'

interface ILastUpdateInformation {
  date: DateTime
  contact: Contact
}

@Component({
  computed: {
    ...mapState('platforms', ['exportControl', 'manufacturerModelId']),
    ...mapGetters('permissions', ['canHandleExportControl']),
    ...mapState('manufacturermodels', ['exportControlCreatedByContact', 'exportControlUpdatedByContact']),
    ...mapGetters('manufacturermodels', ['publicExportControlAttachments'])
  },
  methods: {
    ...mapActions('platforms', ['loadExportControl', 'loadManufacturerModelId']),
    ...mapActions('manufacturermodels', ['loadExportControlAttachments', 'loadExportControlCreatedAndUpdatedByContacts']),
    ...mapActions('progressindicator', ['setLoading']),
    ...mapMutations('manufacturermodels', ['setExportControlAttachments'])
  },
  components: {
    AttachmentListItem,
    BaseList,
    ExportControlBasicData
  }
})
export default class PlatformExportControlPage extends Vue {
  exportControl!: PlatformsState['exportControl']
  manufacturerModelId!: PlatformsState['manufacturerModelId']
  exportControlCreatedByContact!: ManufacturermodelsState['exportControlCreatedByContact']
  exportControlUpdatedByContact!: ManufacturermodelsState['exportControlUpdatedByContact']
  publicExportControlAttachments!: PublicExportControlAttachmentsGetter
  loadExportControl!: LoadExportControlAction
  loadManufacturerModelId!: LoadManufacturerModelIdAction
  loadExportControlAttachments!: LoadExportControlAttachmentsAction
  setLoading!: SetLoadingAction
  setExportControlAttachments!: SetExportControlAttachmentsMutation
  loadExportControlCreatedAndUpdatedByContacts!: LoadExportControlCreatedAndUpdatedByContactsAction
  canHandleExportControl!: CanHandleExportControlGetter

  head () {
    return {
      titleTemplate: 'Export Control - %s'
    }
  }

  async fetch () {
    try {
      await Promise.all([
        this.loadExportControl({ platformId: this.platformId }),
        this.loadManufacturerModelId({ platformId: this.platformId })
      ])
      if (this.manufacturerModelId) {
        this.loadExportControlAttachments(this.manufacturerModelId)
      } else {
        this.setExportControlAttachments([])
      }
      this.loadExportControlCreatedAndUpdatedByContacts(this.exportControl)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of export control information failed')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId () {
    return this.$route.params.platformId
  }

  get lastUpdateInformation (): ILastUpdateInformation | null {
    let result = null
    if (this.exportControlCreatedByContact && this.exportControl?.createdAt) {
      result = {
        contact: this.exportControlCreatedByContact,
        date: this.exportControl.createdAt
      }
    }
    if (this.exportControlUpdatedByContact && this.exportControl?.updatedAt) {
      result = {
        contact: this.exportControlUpdatedByContact,
        date: this.exportControl.updatedAt
      }
    }
    return result
  }
}
</script>
