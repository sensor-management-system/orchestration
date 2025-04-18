<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-dialog
      v-model="showDialog"
      max-width="600"
      persistent
      scrollable
    >
      <v-card v-if="showDialog">
        <v-card-title>Suggest new sampling medium</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new sampling medium for the controlled vocabulary. This is submitted as a proposal.
          </p>
          <p>
            A curator reviews your contribution before accepting it and including it in the full controlled vocabulary.
          </p>
          <p>
            In order to give the curator the opportunity to contact you, we will send your e-mail address with this request.
          </p>
          <v-form ref="suggestionForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="suggestion.compartmentId"
                  :items="compartments"
                  label="Compartment"
                  item-value="id"
                  clearable
                  required
                  class="required"
                  :rules="[rules.required]"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.name"
                  label="Term"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingNames]"
                />
                <SimilarTermsList :search="suggestion.name" :terms="samplingMedia" />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="suggestion.definition"
                  label="Definition"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.provenance"
                  label="Provenance"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="suggestion.provenanceUri"
                  label="Provenance URI"
                />
              </v-col>
            </v-row>
            <v-row class="mt-0">
              <v-col class="pt-0 pb-0">
                <provenance-hint />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="suggestion.category"
                  label="Category"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="suggestion.note"
                  label="Note for the curator"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="suggestion.globalProvenanceId"
                  :items="globalProvenances"
                  label="Global provenance"
                  item-value="id"
                  clearable
                />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            @click="showDialog = false"
          >
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            @click="submit"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { SetLoadingAction } from '@/store/progressindicator'
import ProvenanceHint from '@/components/shared/ProvenanceHint.vue'
import { Rules } from '@/mixins/Rules'
import { SamplingMedia } from '@/models/SamplingMedia'
import { AddSamplingMediaAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'
import SimilarTermsList from '@/components/shared/SimilarTermsList.vue'

@Component({
  computed: {
    ...mapState('vocabulary', ['compartments', 'globalProvenances', 'samplingMedia'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadGlobalProvenances', 'addSamplingMedia']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    SimilarTermsList,
    ProvenanceHint
  }
})
export default class SamplingMediaDialog extends mixins(Rules) {
  private suggestion = new SamplingMedia()
  private addSamplingMedia!: AddSamplingMediaAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private compartments!: VocabularyState['compartments']
  private samplingMedia!: VocabularyState['samplingMedia']
  private globalProvenances!: VocabularyState['globalProvenances']

  // vuex definition for typescript check
  setLoading!: SetLoadingAction

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    required: false,
    type: String,
    default: ''
  })
  readonly initialTerm!: string

  @Prop({
    required: false,
    type: String,
    default: null
  })
  readonly initialCompartmentId!: string | null

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  async fetchRelated () {
    try {
      await this.loadGlobalProvenances()
    } catch {
      this.$store.commit('snackbar/setError', 'Loading of global provenances failed')
    }
  }

  resetInputs () {
    this.suggestion = new SamplingMedia()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.samplingMedia.find(x => x.name === term)) {
      return 'Term is already part of the controlled vocabulary'
    }
    return true
  }

  validateForm (): boolean {
    return (this.$refs.suggestionForm as Vue & { validate: () => boolean }).validate()
  }

  async submit () {
    if (!this.validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors before submitting')
      return
    }
    this.setLoading(true)
    const samplingMedium = SamplingMedia.createFromObject(this.suggestion)
    this.showDialog = false
    try {
      const result = await this.addSamplingMedia({ samplingMedium })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the sampling medium')
    } finally {
      this.setLoading(false)
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      this.suggestion.name = this.initialTerm
      this.suggestion.compartmentId = this.initialCompartmentId
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
