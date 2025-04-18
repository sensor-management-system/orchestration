<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      v-if="value"
      ref="mountForm"
      @submit.prevent
    >
      <v-container>
        <mount-action-date-form
          v-if="withDates"
          ref="dateForm"
          v-model="mountActionDateDTO"
          :begin-date-rules="beginDateRules"
          :end-date-rules="endDateRules"
          :end-required="unmountRequired"
          @input="update"
        />
        <v-row class="pb-0">
          <v-col>
            <v-text-field
              v-model="mountActionInformationDTO.label"
              label="Mount label"
              :disabled="readonly"
              @input="debouncedUpdate"
            />
          </v-col>
        </v-row>
        <v-row class="pb-0">
          <v-col cols="12">
            <span>
              <v-tooltip
                bottom
              >
                <template #activator="{ on, attrs }">
                  Relative offsets:
                  <v-icon
                    size="20"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle
                  </v-icon>
                </template>
                Offsets are relative to parent node.
              </v-tooltip></span>
          </v-col>
          <v-col
            md="12"
            lg="4"
            xl="3"
            dense
          >
            <v-text-field
              :value="mountActionInformationDTO.offsetX"
              data-role="textfield-offset-x"
              label="Relative offset (x)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNonNull($event, 'offsetX')"
            />
          </v-col>
          <v-col
            md="12"
            lg="4"
            xl="3"
            dense
          >
            <v-text-field
              :value="mountActionInformationDTO.offsetY"
              data-role="textfield-offset-y"
              label="Relative offset (y)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNonNull($event, 'offsetY')"
            />
          </v-col>
          <v-col
            md="12"
            lg="4"
            xl="3"
            dense
          >
            <v-text-field
              :value="mountActionInformationDTO.offsetZ"
              data-role="textfield-offset-z"
              label="Relative offset (z)"
              type="number"
              step="any"
              :disabled="readonly"
              required
              :rules="[rules.numeric, rules.required]"
              class="required m-annotated"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNonNull($event, 'offsetZ')"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <span>
              <v-tooltip
                bottom
              >
                <template #activator="{ on, attrs }">
                  Absolute offsets:
                  <v-icon
                    size="20"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle
                  </v-icon>
                </template>
                Relative offsets of the node are included.
              </v-tooltip></span>
          </v-col>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (x):
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetX | round(6) }} m
              </v-col>
            </v-row>
          </v-col>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (y):
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetY | round(6) }} m
              </v-col>
            </v-row>
          </v-col>
          <v-col md="12" lg="4" xl="3">
            <v-row
              no-gutters
            >
              <v-col
                cols="12"
                md="6"
                lg="12"
                class="text-caption text--secondary"
              >
                Absolute offset (z):
              </v-col>
              <v-col
                cols="12"
                md="6"
                lg="12"
              >
                {{ absoluteOffsets.offsetZ | round(6) }} m
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-row class="pb-0">
          <v-col cols="12" md="4">
            <v-text-field
              :value="mountActionInformationDTO.x"
              label="Longitude (x)"
              step="any"
              clearable
              :rules="[rules.numericOrEmpty]"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNullable($event, 'x')"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              :value="mountActionInformationDTO.y"
              label="Latitude (y)"
              step="any"
              clearable
              :rules="[rules.numericOrEmpty]"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNullable($event, 'y')"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="mountActionInformationDTO.epsgCode"
              :item-value="(x) => x.code"
              :item-text="(x) => x.text"
              :items="epsgCodes"
              label="EPSG Code"
              clearable
              @input="update"
            />
          </v-col>
        </v-row>
        <v-row class="pb-0">
          <v-col cols="12" md="4" offset-md="4">
            <v-text-field
              :value="mountActionInformationDTO.z"
              label="Height (z)"
              step="any"
              clearable
              :rules="[rules.numericOrEmpty]"
              hide-spin-buttons
              @wheel.prevent
              @input="debouncedUpdateNumericFieldNullable($event, 'z')"
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="elevationDatum"
              :item-value="(x) => x.name"
              :item-text="(x) => x.name"
              :items="elevationData"
              label="Elevation Datum"
              clearable
              @input="update"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <span>
              <v-autocomplete
                v-model="mountActionInformationDTO.beginContact"
                data-role="select-begin-contact"
                :items="contacts"
                label="Mount contact"
                :disabled="readonly"
                :item-text="(x) => x.toString()"
                :item-value="(x) => x"
                required
                :rules="[rules.required]"
                class="required"
                @input="update"
              />
            </span>
          </v-col>
          <v-col v-if="withUnmount">
            <span>
              <v-autocomplete
                v-model="mountActionInformationDTO.endContact"
                data-role="select-end-contact"
                :items="contacts"
                label="Unmount contact"
                :disabled="readonly"
                :item-text="(x) => x.toString()"
                :item-value="(x) => x"
                :required="unmountRequired"
                :clearable="!unmountRequired"
                :rules="getEndContactRules()"
                :class="unmountRequired ? 'required' : ''"
                @input="update"
              />
            </span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea
              v-model="mountActionInformationDTO.beginDescription"
              data-role="textarea-begin-description"
              label="Mount description"
              rows="3"
              :disabled="readonly"
              @input="debouncedUpdate"
            />
          </v-col>
          <v-col v-if="withUnmount">
            <v-textarea
              v-model="mountActionInformationDTO.endDescription"
              data-role="textarea-end-description"
              label="Unmount description"
              rows="3"
              :disabled="readonly"
              @input="debouncedUpdate"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>
<script lang="ts">

import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DateTime } from 'luxon'

import { Rules } from '@/mixins/Rules'
import { VocabularyState, LoadEpsgCodesAction, LoadElevationDataAction } from '@/store/vocabulary'

import { Contact } from '@/models/Contact'

import MountActionDateForm from '@/components/configurations/MountActionDateForm.vue'
import { MountActionDateDTO, MountActionInformationDTO, IOffsets } from '@/utils/configurationInterfaces'
import { parseFloatOrDefault, parseFloatOrNull } from '@/utils/numericsHelper'

@Component({
  components: {
    MountActionDateForm
  },
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadEpsgCodes', 'loadElevationData'])
  }
})
export default class MountActionDetailsForm extends mixins(Rules) {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: MountActionInformationDTO

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: () => true,
    type: Boolean
  })
  readonly withUnmount!: boolean

  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly unmountRequired!: boolean

  @Prop({
    default: () => true,
    type: Boolean
  })
  readonly withDates!: boolean

  @Prop({
    default: () => [],
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly beginDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly endDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: (): IOffsets => ({ offsetX: 0, offsetY: 0, offsetZ: 0 }),
    required: false,
    type: Object
  })
  readonly parentOffsets!: IOffsets

  debounceTimer: ReturnType<typeof setTimeout> | null = null

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  loadElevationData!: LoadElevationDataAction
  loadEpsgCodes!: LoadEpsgCodesAction

  fetch () {
    Promise.all([this.loadElevationData(), this.loadEpsgCodes()])
  }

  get mountActionDateDTO (): MountActionDateDTO {
    return {
      beginDate: this.mountActionInformationDTO.beginDate,
      endDate: this.mountActionInformationDTO.endDate
    }
  }

  set mountActionDateDTO (value: MountActionDateDTO) {
    this.mountActionInformationDTO.beginDate = value.beginDate
    this.mountActionInformationDTO.endDate = value.endDate
  }

  get mountActionInformationDTO (): MountActionInformationDTO {
    return this.value
  }

  validateForm (): boolean {
    let isValid: boolean = false
    if (this.$refs.mountForm) {
      isValid = (this.$refs.mountForm as Vue & { validate: () => boolean }).validate()
    }
    if (isValid && this.$refs.dateForm) {
      isValid = (this.$refs.dateForm as MountActionDateForm).validateForm()
    }
    return isValid
  }

  resetValidation (): void {
    if (this.$refs.mountForm) {
      (this.$refs.mountForm as Vue & { resetValidation: () => void }).resetValidation()
    }
    if (this.$refs.dateForm) {
      (this.$refs.dateForm as MountActionDateForm).resetValidation()
    }
  }

  getEndContactRules (): ((value: any) => boolean | string)[] {
    if (this.unmountRequired) {
      // @ts-ignore
      return [this.rules.required]
    }
    return []
  }

  updateNumericFieldNonNull (value: any, field: 'offsetX' | 'offsetY' | 'offsetZ') {
    this.mountActionInformationDTO[field] = parseFloatOrDefault(value, 0.0)
    this.update()
  }

  debouncedUpdateNumericFieldNonNull (value: any, field: 'offsetX' | 'offsetY' | 'offsetZ') {
    if (this.debounceTimer !== null) {
      clearTimeout(this.debounceTimer)
    }

    this.debounceTimer = setTimeout(() => {
      this.updateNumericFieldNonNull(value, field)
    }, 250)
  }

  updateNumericFieldNullable (value: any, field: 'x' | 'y' | 'z') {
    this.mountActionInformationDTO[field] = parseFloatOrNull(value)
    this.update()
  }

  debouncedUpdateNumericFieldNullable (value: any, field: 'x' | 'y' | 'z') {
    if (this.debounceTimer !== null) {
      clearTimeout(this.debounceTimer)
    }

    this.debounceTimer = setTimeout(() => {
      this.updateNumericFieldNullable(value, field)
    }, 250)
  }

  update () {
    this.$emit('input', this.mountActionInformationDTO)
  }

  debouncedUpdate () {
    if (this.debounceTimer !== null) {
      clearTimeout(this.debounceTimer)
    }

    this.debounceTimer = setTimeout(() => {
      this.update()
    }, 250)
  }

  get absoluteOffsets (): IOffsets {
    return {
      offsetX: this.parentOffsets.offsetX + this.value.offsetX,
      offsetY: this.parentOffsets.offsetY + this.value.offsetY,
      offsetZ: this.parentOffsets.offsetZ + this.value.offsetZ
    }
  }

  get elevationDatum (): string | null {
    if (!this.mountActionInformationDTO.elevationDatumName) {
      return null
    }
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.mountActionInformationDTO.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.mountActionInformationDTO.elevationDatumName
  }

  set elevationDatum (newElevationDatumName: string | null) {
    this.mountActionInformationDTO.elevationDatumUri = ''
    if (!newElevationDatumName) {
      this.mountActionInformationDTO.elevationDatumName = ''
    } else {
      this.mountActionInformationDTO.elevationDatumName = newElevationDatumName
      const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.mountActionInformationDTO.elevationDatumUri)
      if (elevationDatumIndex > -1) {
        this.mountActionInformationDTO.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
      }
    }
  }
}
</script>

<style scoped>
/* @import "@/assets/styles/_forms.scss"; */

/* the m-annotated class is to add the unit (meters) to the fields */
.m-annotated::after {
  content: " m";
  white-space: pre;
}
</style>
