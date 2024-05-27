<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-text-field
    :value="valueAsDateTimeString"
    :label="label"
    :rules="textInputRules"
    :hint="hint"
    persistent-hint
    :class="{ 'required': required }"
    :clearable="!required"
    v-bind="$attrs"
    @input="updateByTextfield"
  >
    <template #append>
      <span class="text-caption text--secondary">(UTC)</span>
    </template>
    <template #append-outer>
      <v-btn
        v-if="!readonly"
        icon
        @click.stop="initPicker"
      >
        <v-icon>mdi-calendar-range</v-icon>
      </v-btn>
      <v-dialog
        v-model="dialog"
        :width="dialogWidth"
        @click:outside="closePicker"
      >
        <v-card>
          <v-card-text class="text-center">
            <v-tabs v-model="activeTab" fixed-tabs>
              <v-tab v-if="isDateUsed" key="calendar">
                <slot name="dateIcon">
                  <v-icon>mdi-calendar-outline</v-icon>
                </slot>
              </v-tab>
              <v-tab v-if="isTimeUsed" key="time">
                <slot name="timeIcon">
                  <v-icon>mdi-clock-outline</v-icon>
                </slot>
              </v-tab>
              <v-tab-item v-if="isDateUsed" key="calendar">
                <v-date-picker
                  :value="datePickerValue"
                  class="height-adjustment"
                  :min="minDate"
                  :max="maxDate"
                  @input="setDatePickerValue"
                />
              </v-tab-item>
              <v-tab-item v-if="isTimeUsed" key="time">
                <v-time-picker
                  :value="timePickerValue"
                  format="24hr"
                  class="height-adjustment"
                  @input="setTimePickerValue"
                />
                <p class="text-caption">
                  The referenced time zone is UTC.
                </p>
              </v-tab-item>
            </v-tabs>
          </v-card-text>
          <v-card-actions>
            <v-btn
              small
              text
              @click="resetPicker"
            >
              Cancel
            </v-btn>
            <v-spacer />
            <v-btn
              color="accent"
              small
              @click="applyPickerValue"
            >
              Apply
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </v-text-field>
</template>

<script lang="ts">

import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

const DEFAULT_DIALOG_WIDTH = 340
const DEFAULT_DATETIME_FORMAT = 'yyyy-MM-dd HH:mm'
const DEFAULT_DATE_FORMAT = 'yyyy-MM-dd'
const DEFAULT_TIME_FORMAT = 'HH:mm'
@Component
// @ts-ignore
export default class DateTimePicker extends Vue {
  @Prop({ type: Object, default: null }) value!: DateTime | null
  @Prop({ type: String, required: true }) label!: string
  @Prop({ type: String, required: false }) hint!: string

  @Prop({ type: Number, default: DEFAULT_DIALOG_WIDTH }) dialogWidth?: number

  @Prop({ type: Boolean, default: false }) useDate!: boolean
  @Prop({ type: Boolean, default: false }) useTime!: boolean

  @Prop({ default: () => [], type: Array }) readonly rules!: []

  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({ default: false, type: Boolean }) readonly required!: boolean

  @Prop({ type: String, required: false }) minDate!: string
  @Prop({ type: String, required: false }) maxDate!: string

  private isDatetimeUsed: boolean = true
  private usesDate: boolean = false
  private usesTime: boolean = false

  private dialog: boolean = false
  private activeTab: number = 0

  private optsZone = { zone: 'UTC' }

  private textInput: string = ''

  private currentFormat: string = DEFAULT_DATETIME_FORMAT

  private datePickerValue: string = ''
  private timePickerValue: string = ''

  private textListRules = []

  created () {
    this.usesDate = this.useDate
    this.usesTime = this.useTime

    if (this.usesDate || this.usesTime) {
      this.isDatetimeUsed = false
    }

    if (this.usesDate && this.usesTime) {
      this.isDatetimeUsed = true
      this.usesDate = false
      this.usesTime = false
    }

    if (this.usesDate) {
      this.currentFormat = DEFAULT_DATE_FORMAT
    }
    if (this.usesTime) {
      this.currentFormat = DEFAULT_TIME_FORMAT
    }
  }

  get isTimeUsed () {
    return this.isDatetimeUsed || this.usesTime
  }

  get isDateUsed () {
    return this.isDatetimeUsed || this.usesDate
  }

  get valueAsDateTimeString (): string {
    if (this.value) {
      this.setTextInputByValue(this.value)
    } else if (this.isValueValidByCurrentFormat(this.textInput)) {
      this.emitDateTimeObject()
    }
    return this.textInput
  }

  get datePart (): string {
    if (this.isValueValidByCurrentFormat(this.textInput)) {
      return this.parseToCurrentFormat().toFormat(DEFAULT_DATE_FORMAT)
    }
    return DateTime.now().setZone('UTC').toFormat(DEFAULT_DATE_FORMAT)
  }

  get timePart (): string {
    if (this.isValueValidByCurrentFormat(this.textInput)) {
      return this.parseToCurrentFormat().toFormat(DEFAULT_TIME_FORMAT)
    }
    return DateTime.utc().set({
      hour: 12, minute: 0, second: 0, millisecond: 0
    }).toFormat(DEFAULT_TIME_FORMAT)
  }

  setTextInputByValue (datetimeValue: DateTime | null) {
    if (datetimeValue) {
      this.textInput = datetimeValue.toUTC().toFormat(this.currentFormat)
    } else {
      this.textInput = ''
    }
  }

  setDatePickerValue (value: string) {
    this.datePickerValue = value
  }

  setTimePickerValue (value: string) {
    this.timePickerValue = value
  }

  resetPickerValues () {
    this.setTimePickerValue('')
    this.setDatePickerValue('')
  }

  initPicker () {
    this.dialog = true
    this.initDateAndTimePickerValues()
  }

  initDateAndTimePickerValues () {
    this.datePickerValue = this.datePart
    this.timePickerValue = this.timePart
  }

  resetPicker () {
    this.resetPickerValues()
    this.closePicker()
  }

  closePicker () {
    this.dialog = false
    this.activeTab = 0
  }

  getPickerValue (): string {
    if (this.isDatetimeUsed) {
      return this.datePickerValue + ' ' + this.timePickerValue
    }
    if (this.usesDate) {
      return this.datePickerValue
    }
    if (this.usesTime) {
      return this.timePickerValue
    }
    return ''
  }

  applyPickerValue () {
    const value = this.getPickerValue()
    this.updateByTextfield(value)
    this.closePicker()
    this.resetPickerValues()
  }

  parseToCurrentFormat () {
    const currentFormatTime = DateTime.fromFormat(this.textInput, this.currentFormat, this.optsZone)
    return currentFormatTime
  }

  updateByTextfield (newTextValue: string | null) {
    this.textInput = newTextValue || ''
    if (this.isValueValidByCurrentFormat(this.textInput)) {
      this.emitDateTimeObject()
    } else {
      this.emitValue(null)
    }
  }

  emitDateTimeObject () {
    const newValue = this.parseToCurrentFormat()
    this.emitValue(newValue)
  }

  emitValue (newValue: DateTime | null) {
    this.$emit('input', newValue)
  }

  isValueValidByCurrentFormat (value: string): boolean {
    return DateTime.fromFormat(value, this.currentFormat).isValid
  }

  get textInputRules () {
    let rulesList: ((value: string) => string | boolean)[] = []

    const textInputRule = (v: string) => {
      return !v || this.isValueValidByCurrentFormat(v) || `Please use the format: ${this.currentFormat}`
    }
    rulesList.push(textInputRule)

    if (this.rules.length > 0) {
      rulesList = rulesList.concat(this.rules)
    }
    return rulesList
  }

  public resetTextInput (): void {
    this.textInput = ''
  }
}
</script>

<style lang="scss">
@import '@/assets/styles/_forms.scss';
.height-adjustment {
  min-height: 392px;
}
</style>
