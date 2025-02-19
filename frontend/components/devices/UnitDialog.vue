<!--
SPDX-FileCopyrightText: 2022 - 2024
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
        <v-card-title>Suggest new unit</v-card-title>
        <v-card-text>
          <p>
            You can suggest a new unit for the controlled vocabulary. This is submitted as a proposal.
          </p>
          <p>
            A curator reviews your contribution before accepting it and including it in the full controlled vocabulary.
          </p>
          <p>
            In order to give the curator the opportunity to contact you, we will send your e-mail address with this request.
          </p>
          <v-form ref="unitForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.name"
                  label="Term"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingNames]"
                />
                <SimilarTermsList :terms="units" :search="unit.name" :n-gram-length="2" />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="unit.definition"
                  label="Definition"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.provenance"
                  label="Provenance"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="unit.provenanceUri"
                  label="Provenance URI"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.provenanceTerm"
                  label="Provenance term"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="unit.ucumCaseSensitiveSymbol"
                  label="UCUM c/s"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <provenance-hint>
                  To fill out the provenance please note the origin of the term.
                  Perhaps there is a relevant vocabulary
                  (<a href="http://vocab.nerc.ac.uk/" target="_blank">NERC</a>,
                  <a href="http://vocabulary.odm2.org/" target="_blank">ODM2</a>,
                  <a href="https://en.wikipedia.org/" target="_blank">Wiki</a>, etc.) that contains the term.
                  If it's a term used in your scientific discipline, you can note that as well.
                  In the field <em>Provenance URI</em> you can enter the link to the origin of the term.

                  For the units <a href="https://ucum.org/ucum" target="_blank">UCUM</a> is a good source for terms.
                  It helps for the curation process to include the case sensitive symbol (c/s).
                </provenance-hint>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.category"
                  label="Category"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-textarea
                  v-model="unit.note"
                  label="Note for the curator"
                  rows="2"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="unit.globalProvenanceId"
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
import { Unit } from '@/models/Unit'
import { AddUnitAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'
import SimilarTermsList from '@/components/shared/SimilarTermsList.vue'

@Component({
  computed: {
    ...mapState('vocabulary', ['units', 'globalProvenances'])
  },
  methods: {
    ...mapActions('vocabulary', ['addUnit', 'loadGlobalProvenances']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    SimilarTermsList,
    ProvenanceHint
  }
})
export default class UnitDialog extends mixins(Rules) {
  private unit = new Unit()
  private addUnit!: AddUnitAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private units!: VocabularyState['units']
  private globalProvenances!: VocabularyState['globalProvenances']

  // vuex definition for typescript check
  setLoading!: SetLoadingAction

  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

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
    this.unit = new Unit()
  }

  notInExistingNames (term: string| null): boolean | string {
    if (!term) {
      return true
    }
    if (this.units.find(x => x.name === term)) {
      return 'Term is already part of the controlled vocabulary'
    }
    return true
  }

  validateForm (): boolean {
    return (this.$refs.unitForm as Vue & { validate: () => boolean}).validate()
  }

  async submit () {
    if (!this.validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors before submitting')
      return
    }
    this.setLoading(true)
    const unit = Unit.createFromObject(this.unit)
    this.showDialog = false
    try {
      const result = await this.addUnit({ unit })
      this.$emit('aftersubmit', result)
      this.$store.commit('snackbar/setSuccess', 'Your proposal has been successfully submitted. Your changes will be reviewed soon.')
    } catch (err) {
      this.$store.commit('snackbar/setError', 'Error on submitting the unit')
    } finally {
      this.setLoading(false)
      this.resetInputs()
    }
  }

  @Watch('value')
  async onOpenCloseToggle (newValue: boolean) {
    if (newValue) {
      // We open the dialog
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
