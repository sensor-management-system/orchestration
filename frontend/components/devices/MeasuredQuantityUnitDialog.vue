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
          <!-- First we have a form to select if we want to add an existing
               unit or not.
          -->
          <v-form ref="unitSelectionTypeForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="useExistingUnit"
                  :items="existingOrNewUnit"
                  :item-text="(x) => x.text"
                  :item-value="(x) => x.value"
                />
              </v-col>
            </v-row>
          </v-form>
          <!-- If the user wants to use an existing unit, then she/he
               should select it.
          -->
          <v-form v-if="useExistingUnit" ref="unitSelectionForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-select
                  v-model="measuredQuantityUnit.unitId"
                  :items="units"
                  label="Unit"
                  item-value="id"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingMeasuredQuantityBindings]"
                />
              </v-col>
            </v-row>
          </v-form>
          <!-- Else we show the input fields to add a new unit overall.
          -->
          <v-form v-else ref="unitForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="unit.name"
                  label="Term"
                  required
                  class="required"
                  :rules="[rules.required, notInExistingNames]"
                />
                <SimilarTermsList
                  :search="unit.name"
                  :terms="units"
                  :n-gram-length="2"
                />
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
            <v-row class="mt-0">
              <v-col class="pt-0 pb-0">
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
          <!-- And last we show the default form for default limits.
          -->
          <v-form ref="measuredQuantityUnitForm" @submit.prevent>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="measuredQuantityUnit.defaultLimitMin"
                  label="Default limit min"
                  type="number"
                  step="any"
                  @wheel.prevent
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-model="measuredQuantityUnit.defaultLimitMax"
                  label="Default limit max"
                  type="number"
                  step="any"
                  @wheel.prevent
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
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { Unit } from '@/models/Unit'
import { AddUnitAction, AddMeasuredQuantityUnitAction, LoadGlobalProvenancesAction, VocabularyState } from '@/store/vocabulary'
import SimilarTermsList from '@/components/shared/SimilarTermsList.vue'

@Component({
  computed: {
    ...mapState('vocabulary', ['units', 'globalProvenances', 'measuredQuantityUnits'])
  },
  methods: {
    ...mapActions('vocabulary', ['addUnit', 'addMeasuredQuantityUnit', 'loadGlobalProvenances']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    SimilarTermsList,
    ProvenanceHint
  }
})
export default class MeasuredQuantityUnitDialog extends mixins(Rules) {
  private unit = new Unit()
  private measuredQuantityUnit = new MeasuredQuantityUnit()
  private addUnit!: AddUnitAction
  private addMeasuredQuantityUnit!: AddMeasuredQuantityUnitAction
  private loadGlobalProvenances!: LoadGlobalProvenancesAction
  private units!: VocabularyState['units']
  private globalProvenances!: VocabularyState['globalProvenances']
  private measuredQuantityUnits !: VocabularyState['measuredQuantityUnits']
  private useExistingUnit: boolean = true
  private existingOrNewUnit = [
    { text: 'Existing unit', value: true },
    { text: 'New unit', value: false }
  ]

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
    default: null
  })
  readonly initialMeasuredQuantityId!: string | null

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
    this.measuredQuantityUnit = new MeasuredQuantityUnit()
    this.useExistingUnit = true
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

  notInExistingMeasuredQuantityBindings (unitId: string | null): boolean | string {
    if (!unitId) {
      return true
    }
    const existing = this.measuredQuantityUnits.find(x => x.unitId === unitId && x.measuredQuantityId === this.measuredQuantityUnit.measuredQuantityId)
    if (existing) {
      return 'Unit selection already possible for the measured quantity'
    }
    return true
  }

  validateForms (): boolean {
    const formsToValidate = ['unitSelectionTypeForm']

    if (this.useExistingUnit) {
      formsToValidate.push('unitSelectionForm')
    } else {
      formsToValidate.push('unitForm')
    }
    formsToValidate.push('measuredQuantityUnitForm')

    let result = true
    for (const form of formsToValidate) {
      result = result && (this.$refs[form] as Vue & { validate: () => boolean}).validate()
    }
    return result
  }

  async submit () {
    if (!this.validateForms()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors before submitting')
      return
    }
    this.setLoading(true)
    const unit = Unit.createFromObject(this.unit)
    const measuredQuantityUnit = MeasuredQuantityUnit.createFromObject(this.measuredQuantityUnit)
    this.showDialog = false
    try {
      let selectedUnit: Unit | null = null
      if (!this.useExistingUnit) {
        selectedUnit = await this.addUnit({ unit })
      } else {
        selectedUnit = this.units.find(x => x.id === measuredQuantityUnit.unitId) || null
      }
      if (selectedUnit) {
        measuredQuantityUnit.unitId = selectedUnit.id
        measuredQuantityUnit.name = selectedUnit.name
        measuredQuantityUnit.definition = selectedUnit.definition
      }
      const result = await this.addMeasuredQuantityUnit({
        measuredQuantityUnit
      })
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
      if (this.initialMeasuredQuantityId) {
        this.measuredQuantityUnit.measuredQuantityId = this.initialMeasuredQuantityId
      }
      await this.fetchRelated()
    } else {
      this.resetInputs()
    }
  }
}
</script>
