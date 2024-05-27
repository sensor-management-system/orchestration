<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

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
      <v-card>
        <v-card-title>Suggest new site / lab type</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new site / lab type for the controlled vocabulary. This is submitted as a proposal.
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
                  v-model="suggestion.siteUsageId"
                  :items="siteUsages"
                  label="Site / Lab Usage"
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
import { SiteType } from '@/models/SiteType'
import { AddSiteTypeAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'

@Component({
  computed: {
    ...mapState('vocabulary', ['siteTypes', 'siteUsages', 'globalProvenances'])
  },
  methods: {
    ...mapActions('vocabulary', ['addSiteType', 'loadGlobalProvenances']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    ProvenanceHint
  }
})
export default class SiteTypeDialog extends mixins(Rules) {
  private suggestion = new SiteType()
  private addSiteType!: AddSiteTypeAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private siteUsages!: VocabularyState['siteUsages']
  private siteTypes!: VocabularyState['siteTypes']
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
  readonly initialSiteUsageId!: string | null

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
    this.suggestion = new SiteType()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.siteTypes.find(x => x.name === term)) {
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
    // Copy before closing the dialog
    const siteType = SiteType.createFromObject(this.suggestion)
    this.showDialog = false
    try {
      const result = await this.addSiteType({ siteType })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the site / lab type')
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
      this.suggestion.siteUsageId = this.initialSiteUsageId
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
