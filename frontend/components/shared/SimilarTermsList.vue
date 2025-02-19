<!--
SPDX-FileCopyrightText: 2022 - 2024
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row no-gutters class="mt-2">
      <v-col v-if="similarFilteredTerms.length > 0" dense class="v-text-field__details">
        <v-alert text icon="mdi-alert">
          <div class="v-messages">
            There exist similar terms:
            <ul>
              <li v-for="(similarProperty, idx) in similarFilteredTerms" :key="idx">
                <b>{{ similarProperty.name }}</b>
                <v-btn
                  x-small
                  :href="similarProperty.uri"
                  target="_blank"
                  icon
                >
                  <v-icon>mdi-open-in-new</v-icon>
                </v-btn>
                <span v-if="filteredPropertyKey">
                  with {{ filteredPropertyName }} <b>{{ getRelatedFilteredProperty(similarProperty).name }}</b>
                  <v-btn
                    x-small
                    :href="getRelatedFilteredProperty(similarProperty).uri"
                    target="_blank"
                    icon
                  >
                    <v-icon small>mdi-open-in-new</v-icon>
                  </v-btn>
                </span>
              </li>
            </ul>
            Please check if you can use one of them.
            If so, you can close this dialog and use the term directly in the select list.
          </div>
        </v-alert>
      </v-col>
    </v-row>
    <v-row no-gutters class="mt-2">
      <v-col v-if="similarExcludedFromFilteredTerms.length > 0">
        <v-alert text type="info">
          <div class="v-messages">
            There exist similar terms for different {{ filteredPropertyNamePlural }}:
            <ul>
              <li v-for="(similarProperty, idx) in similarExcludedFromFilteredTerms" :key="idx">
                <span>
                  <b>{{ similarProperty.name }}</b>
                  <v-btn
                    color="info"
                    x-small
                    :href="similarProperty.uri"
                    target="_blank"
                    icon
                  ><v-icon small>mdi-open-in-new</v-icon>
                  </v-btn>
                  with {{ filteredPropertyName }} <b>{{ getRelatedFilteredProperty(similarProperty).name }}</b>
                  <v-btn
                    color="info"
                    x-small
                    :href="getRelatedFilteredProperty(similarProperty).uri"
                    target="_blank"
                    icon
                  ><v-icon small>mdi-open-in-new</v-icon>
                  </v-btn>
                  <v-tooltip right>
                    <template #activator="{ on, attrs }">
                      <v-btn
                        x-small
                        outlined
                        color="info"
                        v-bind="attrs"
                        v-on="on"
                        @click="reuseEntry(similarProperty)"
                      >
                        Reuse
                      </v-btn>
                    </template>
                    <span>Reuse properties from this entry into the current form</span>
                  </v-tooltip>
                </span>
              </li>
            </ul>
            If you want to enable one of those terms for another {{ filteredPropertyName }}, you can reuse them.
          </div>
        </v-alert>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from 'nuxt-property-decorator'

interface CvEntry {
  id: string
  name: string
}

@Component
export default class SimilarTermsList extends Vue {
  /**
   * The term checked for similarity with existing terms.
   */
  @Prop({
    required: false,
    default: () => '',
    type: String
  })
  readonly search!: string

  /**
   * The length of n-Grams (e.g. 3 is trigrams)
   * @default 3
   */
  @Prop({
    required: false,
    default: 3,
    type: Number
  })
  readonly nGramLength!: number

  /**
   * The similarity threshold.
   * @default 0.12
   */
  @Prop({
    required: false,
    default: 0.12,
    type: Number
  })
  readonly threshold!: number

  /**
   * All existing terms checked for similarity of the suggested term.
   */
  @Prop({
    required: true,
    type: Array
  })
  readonly terms!: CvEntry[]

  /**
   * @optional Only used if existing terms are filtered by a specific property.
   * A list of all available selections for the property filtered by.
   */
  @Prop({
    required: false,
    type: Array
  })
  readonly propertiesFilteredBy!: CvEntry[]

  /**
   * @optional Only used if existing terms are filtered by a specific property.
   * The value of the property filtered by.
   */
  @Prop({
    required: false,
    type: String
  })
  readonly filteredPropertyValue!: any

  /**
   * @optional Only used if existing terms are filtered by a specific property.
   * The key of the property filtered by.
   */
  @Prop({
    required: false,
    type: String
  })
  readonly filteredPropertyKey!: keyof CvEntry

  /**
   * @optional Only used if existing terms are filtered by a specific property.
   * The display name of the property filtered by.
   */
  @Prop({
    required: false,
    type: String
  })
  readonly filteredPropertyName!: string

  /**
   * @optional Only used if existing terms are filtered by a specific property.
   * The plural display name of the property filtered by.
   */
  @Prop({
    required: false,
    type: String
  })
  readonly filteredPropertyNamePlural!: string

  generateNGrams (text: string): string[] {
    const nGrams = []
    for (let i = 0; i < text.length - this.nGramLength + 1; i++) {
      nGrams.push(text.substring(i, i + this.nGramLength))
    }
    return nGrams
  }

  nGramSimilarity (text1: string, text2: string): number {
    const nGrams1 = new Set(this.generateNGrams(text1))
    const nGrams2 = new Set(this.generateNGrams(text2))

    const intersection = new Set([...nGrams1].filter(nGram => nGrams2.has(nGram)))
    const union = new Set([...nGrams1, ...nGrams2])

    return intersection.size / union.size
  }

  get similarTerms (): CvEntry[] {
    if (!this.search || this.search.length < this.nGramLength) {
      return []
    }
    const result = []

    const terms = this.terms

    for (const prop of terms) {
      const similarityValue = this.nGramSimilarity(prop.name.toLowerCase(), this.search.toLowerCase())
      if (similarityValue < this.threshold) {
        continue
      }
      result.push({
        prop,
        similarity: similarityValue
      })
    }

    result.sort((a, b) => b.similarity - a.similarity)
    return result.slice(0, this.nGramLength).map(x => x.prop)
  }

  /**
   * @returns {CvEntry[]} all terms matching the filtered property.
   */
  get filteredTerms () {
    if (!this.filteredPropertyValue) {
      return this.terms
    }
    return this.terms.filter(t => t[this.filteredPropertyKey] === this.filteredPropertyValue)
  }

  /**
   * @returns {CvEntry[]} all terms not matching the filtered property.
   */
  get excludedFromFilteredTerms () {
    if (!this.filteredPropertyValue) {
      return []
    }
    return this.terms.filter(t => t[this.filteredPropertyKey] !== this.filteredPropertyValue)
  }

  /**
   * @returns {CvEntry[]} all similar terms matching the filtered property if given.
   */
  get similarFilteredTerms () {
    return this.similarTerms.filter(t => this.filteredTerms.includes(t))
  }

  /**
   * @returns {CvEntry[]} all similar terms not matching the filtered property.
   */
  get similarExcludedFromFilteredTerms () {
    return this.similarTerms.filter(t => this.excludedFromFilteredTerms.includes(t))
  }

  getRelatedFilteredProperty (similarProperty: CvEntry) {
    return this.propertiesFilteredBy.find(p => p.id === similarProperty[this.filteredPropertyKey])
  }

  @Emit('reuse')
  reuseEntry (property: CvEntry) {
    this.$store.commit('snackbar/setInfo', `Reused ${property.name}. Please check auto-filled details and adjust them accordingly before submitting!`)
    return property
  }
}
</script>
