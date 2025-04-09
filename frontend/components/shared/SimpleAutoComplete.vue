<!--
 SPDX-FileCopyrightText: 2020 - 2025

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-menu
    v-model="menuVisible"
    :close-on-content-click="false"
    bottom
    offset-y
    nudge-top="20"
  >
    <template #activator="{ on }">
      <div v-if="localSelectedItems.length === 0">
        <v-text-field
          v-model="search"
          :label="label"
          :hint="hint"
          :append-icon="menuVisible ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          class="autocomplete-input"
          v-on="on"
        />
      </div>
      <div v-else>
        <div class="selected-items">
          <v-chip
            v-for="(item, index) in localSelectedItems"
            :key="index"
            close
            @click:close="removeItem(item)"
          >
            {{ itemText(item) }}
          </v-chip>
        </div>
        <v-text-field
          v-model="search"
          :label="label"
          :hint="hint"
          :append-icon="menuVisible ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          class="autocomplete-input"
          v-on="on"
        />
      </div>
    </template>
    <v-list>
      <v-list-item
        v-for="(item, index) in filteredItems"
        :key="index"
        :class="{ 'primary--text v-list-item--active': isSelected(item) }"
        @click="toggleItem(item)"
      >
        <slot name="item" :item="item">
          {{ itemText(item) }}
        </slot>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

@Component
export default class SimpleAutoComplete extends Vue {
  @Prop({ type: Array, default: [] }) items!: any[]
  @Prop({ type: String, default: '' }) label!: string
  @Prop({ type: String, default: '' }) hint!: string
  @Prop({ type: Function, default: (item: any) => item.toString() }) itemText!: (item: any) => string

  @Prop({ type: Array, default: [] }) value!: any[]

  search = ''
  menuVisible = false
  filteredItems = this.items
  localSelectedItems: any[] = []

  removeItem (item: any) {
    const index = this.localSelectedItems.indexOf(item)
    if (index !== -1) {
      this.localSelectedItems.splice(index, 1)
      this.$emit('input', this.localSelectedItems)
    }
  }

  toggleItem (item: any) {
    const index = this.localSelectedItems.indexOf(item)
    if (index === -1) {
      this.localSelectedItems = [...this.localSelectedItems, item]
    } else {
      this.localSelectedItems = this.localSelectedItems.filter(i => i !== item)
    }
    this.$emit('input', this.localSelectedItems)
  }

  isSelected (item: any) {
    return this.localSelectedItems.includes(item)
  }

  @Watch('value', { immediate: true })
  onValueChanged (newValue: any[]) {
    this.localSelectedItems = [...newValue]
  }

  @Watch('search')
  searchItems () {
    if (this.search === '') {
      this.filteredItems = this.items
    } else {
      this.filteredItems = this.items.filter((item) => {
        return this.itemText(item).toLowerCase().includes(this.search.toLowerCase())
      })
    }
  }

  @Watch('menuVisible')
  onMenuVisibleChanged (newValue: boolean) {
    if (newValue) {
      this.searchItems()
    }
  }
}
</script>

<style scoped>
.autocomplete-input {
  flex-grow: 1;
}

.selected-items {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
