<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/configurations/' + configurationId + '/attachments'"
        @save="save"
      />
    </v-card-actions>
    <v-card>
      <v-card-text
        class="py-2 px-3"
      >
        <div class="d-flex align-center">
          <span class="text-caption">
            {{ filename(valueCopy) }}
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
                v-model="valueCopy.label"
                label="Label"
                required
                class="required"
                :rules="[rules.required]"
              />
            </v-form>
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              :href="valueCopy.url"
              target="_blank"
              text
              small
              nuxt
            >
              <v-icon
                small
              >
                mdi-open-in-new
              </v-icon>
              Open in new tab
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, mixins, InjectReactive, Watch } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import {
  ConfigurationsState,
  LoadConfigurationAttachmentsAction,
  LoadConfigurationAttachmentAction,
  UpdateConfigurationAttachmentAction
} from '@/store/configurations'

import { Attachment } from '@/models/Attachment'

import { Rules } from '@/mixins/Rules'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component({
  components: {
    SaveAndCancelButtons,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('configurations', ['configurationAttachment']),
  methods: mapActions('configurations', ['loadConfigurationAttachment', 'loadConfigurationAttachments', 'updateConfigurationAttachment'])
})
// @ts-ignore
export default class AttachmentEditPage extends mixins(Rules, AttachmentsMixin) {
  @InjectReactive()
    editable!: boolean

  private isSaving = false
  private isLoading = false
  private valueCopy: Attachment = new Attachment()

  // vuex definition for typescript check
  configurationAttachment!: ConfigurationsState['configurationAttachment']
  loadConfigurationAttachment!: LoadConfigurationAttachmentAction
  loadConfigurationAttachments!: LoadConfigurationAttachmentsAction
  updateConfigurationAttachment!: UpdateConfigurationAttachmentAction

  created () {
    if (!this.editable) {
      this.$router.replace('/configurations/' + this.configurationId + '/attachments', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await this.loadConfigurationAttachment(this.attachmentId)
      if (this.configurationAttachment) {
        this.valueCopy = Attachment.createFromObject(this.configurationAttachment)
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load attachment')
    } finally {
      this.isLoading = false
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get attachmentId (): string {
    return this.$route.params.attachmentId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  async save () {
    if (!(this.$refs.attachmentsEditForm as Vue & { validate: () => boolean }).validate()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.isSaving = true
      await this.updateConfigurationAttachment({
        configurationId: this.configurationId,
        attachment: this.valueCopy
      })
      this.loadConfigurationAttachments(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Attachment updated')
      this.$router.push('/configurations/' + this.configurationId + '/attachments')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save attachments')
    } finally {
      this.isSaving = false
    }
  }

  @Watch('editable', {
    immediate: true
  })
  onEditableChanged (value: boolean, oldValue: boolean | undefined) {
    if (!value && typeof oldValue !== 'undefined') {
      this.$router.replace('/configurations/' + this.configurationId + '/attachments', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
    }
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
