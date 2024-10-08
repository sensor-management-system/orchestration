<!--
SPDX-FileCopyrightText: 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <save-and-cancel-buttons
        v-if="canHandleExportControl"
        save-btn-text="Update"
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
        @save="save"
      />
    </v-card-actions>
    <v-card flat>
      <v-card-text
        class="py-2 px-3"
      >
        <div class="d-flex align-center">
          <span class="text-caption">
            {{ filename(valueCopy) }}<span v-if="valueCopy.createdAt && valueCopy.isUpload">,
              uploaded at {{ valueCopy.createdAt | toUtcDateTimeString }}
            </span>
          </span>
        </div>
        <v-row
          no-gutters
        >
          <v-col cols="8" class="text-subtitle-1">
            <v-icon>
              {{ filetypeIcon(valueCopy) }}
            </v-icon>
            <v-form ref="attachmentsEditForm" class="pb-2" @submit.prevent>
              <v-text-field
                v-model="valueCopy.url"
                :label="valueCopy.isUpload ? 'File': 'URL'"
                required
                class="required"
                type="url"
                placeholder="https://"
                :rules="valueCopy.isUpload ? [] : [rules.required, rules.validUrl]"
                :disabled="valueCopy.isUpload"
              />
              <v-text-field
                v-model="valueCopy.label"
                label="Label"
                required
                class="required"
                :rules="[rules.required]"
              />
              <v-radio-group
                v-model="valueCopy.isExportControlOnly"
                label="Visibility"
                row
              >
                <v-radio label="Internal" :value="true" />
                <v-radio label="Public" :value="false" />
              </v-radio-group>
              <v-textarea
                v-model="valueCopy.description"
                label="Description"
                rows="3"
              />
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          v-if="canHandleExportControl"
          save-btn-text="Update"
          :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { Rules } from '@/mixins/Rules'
import { UploadRules } from '@/mixins/UploadRules'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { ExportControlAttachment } from '@/models/ExportControlAttachment'
import { CanHandleExportControlGetter } from '@/store/permissions'
import { SetLoadingAction } from '@/store/progressindicator'
import { UpdateExportControlAttachmentAction, LoadExportControlAttachmentAction, ManufacturermodelsState } from '@/store/manufacturermodels'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

@Component({
  computed: {
    ...mapGetters('permissions', ['canHandleExportControl']),
    ...mapState('manufacturermodels', ['exportControlAttachment'])
  },
  components: {
    SaveAndCancelButtons
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('manufacturermodels', ['updateExportControlAttachment', 'loadExportControlAttachment']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ExportControlAttachmentEditPage extends mixins(Rules, AttachmentsMixin, UploadRules) {
  private valueCopy: ExportControlAttachment = new ExportControlAttachment()

  canHandleExportControl!: CanHandleExportControlGetter
  exportControlAttachment!: ManufacturermodelsState['exportControlAttachment']
  setLoading!: SetLoadingAction
  updateExportControlAttachment!: UpdateExportControlAttachmentAction
  loadExportControlAttachment!: LoadExportControlAttachmentAction

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadExportControlAttachment(this.attachmentId)
      if (this.exportControlAttachment) {
        this.valueCopy = ExportControlAttachment.createFromObject(this.exportControlAttachment)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.setLoading(false)
    }
  }

  get manufacturerModelId (): string {
    return this.$route.params.manufacturerModelId
  }

  get attachmentId (): string {
    return this.$route.params.attachmentId
  }

  async save () {
    if (!(this.$refs.attachmentsEditForm as Vue & { validate: () => boolean }).validate()) {
      return
    }

    (this.$refs.attachmentsEditForm as Vue & { resetValidation: () => boolean }).resetValidation()
    try {
      this.setLoading(true)

      await this.updateExportControlAttachment({
        manufacturerModelId: this.manufacturerModelId,
        attachment: this.valueCopy
      })
      this.$store.commit('snackbar/setSuccess', 'Aattachment updated')
      this.$router.push('/manufacturer-models/' + this.manufacturerModelId + '/export-control')
    } catch (error: any) {
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
