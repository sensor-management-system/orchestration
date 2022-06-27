<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
    <v-row>
      <v-col cols="12" md="5">
        <v-text-field
          v-model="searchText"
          label="Name"
          placeholder="Name of contact"
          hint="Please enter at least 3 characters"
          @keydown.enter="basicSearch"
        />
      </v-col>
      <v-col
        cols="5"
        align-self="center"
      >
        <v-btn
          color="primary"
          small
          @click="basicSearch"
        >
          Search
        </v-btn>
        <v-btn
          text
          small
          @click="clearSearch"
        >
          Clear
        </v-btn>
      </v-col>
      <v-col
        align-self="center"
        class="text-right"
      >
        <v-btn
          v-if="$auth.loggedIn"
          color="accent"
          small
          nuxt
          to="/contacts/new"
        >
          New Contact
        </v-btn>
      </v-col>
    </v-row>

    <v-progress-circular
      v-if="loading"
      class="progress-spinner"
      color="primary"
      indeterminate
    />
    <div v-if="contacts.length<=0 && !loading">
      <p class="text-center">
        There are no contacts that match your search criteria.
      </p>
    </div>

    <div v-if="contacts.length>0">
      <v-subheader>
        <template v-if="contacts.length == 1">
          1 contact found
        </template>
        <template v-else>
          {{ contacts.length }} contacts found
        </template>
        <!-- No export to pdf due to data privacy reasons -->
      </v-subheader>

      <v-row
        no-gutters
      >
        <v-spacer />
        <v-col
          cols="4"
        >
          <v-pagination
            v-model="page"
            :disabled="loading"
            :length="totalPages"
            :total-visible="7"
            @input="runSearch"
          />
        </v-col>
        <v-col
          cols="4"
          class="flex-grow-1 flex-shrink-0"
        >
          <v-subheader>
            <page-size-select
              v-model="size"
              :items="pageSizeItems"
              label="Items per page"
            />
          </v-subheader>
        </v-col>
      </v-row>
      <BaseList
        :list-items="contacts"
      >
        <template #list-item="{item}">
          <ContactsListItem
            :key="item.id"
            :contact="item"
          >
            <template
              v-if="$auth.loggedIn"
              #dot-menu-items
            >
              <DotMenuActionDelete
                @click="initDeleteDialog(item)"
              />
            </template>
            <template #actions>
              <v-btn
                :to="'/contacts/' + item.id"
                color="primary"
                text
                small
                @click.stop.prevent
              >
                View
              </v-btn>
            </template>
          </ContactsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="runSearch"
      />
    </div>
    <ContacsDeleteDialog
      v-model="showDeleteDialog"
      :contact-to-delete="contactToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState, mapGetters } from 'vuex'

import { Contact } from '@/models/Contact'

import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'

import BaseList from '@/components/shared/BaseList.vue'
import ContactsListItem from '@/components/contacts/ContactsListItem.vue'
import { QueryParams } from '@/modelUtils/QueryParams'

@Component({
  components: {
    ContactsListItem,
    BaseList,
    ContacsDeleteDialog,
    DotMenuActionDelete,
    PageSizeSelect
  },
  computed: {
    ...mapState('contacts', ['pageNumber', 'pageSize', 'totalPages', 'contacts']),
    ...mapGetters('contacts', ['pageSizes'])
  },
  methods: {
    ...mapActions('contacts', ['searchContactsPaginated', 'setPageNumber', 'setPageSize', 'deleteContact']),
    ...mapActions('appbar', ['initContactsIndexAppBar', 'setDefaults'])
  }
})
export default class SearchContactsPage extends Vue {
  private loading: boolean = false
  private searchText: string = ''

  private showDeleteDialog: boolean = false
  private contactToDelete: Contact | null = null

  // vuex definition for typescript check
  initContactsIndexAppBar!: () => void
  setDefaults!: () => void
  pageNumber!: number
  setPageNumber!: (newPageNumber: number) => void
  pageSize!: number
  setPageSize!: (newPageSize: number) => void
  pageSizes!: number[]
  searchContactsPaginated!: (searchtext: string) => void
  deleteContact!: (id: string) => void

  async created () {
    try {
      this.loading = true
      await this.initContactsIndexAppBar()
      this.initSearchQueryParams()
      this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of contacts failed')
    } finally {
      this.loading = false
    }
  }

  beforeDestroy () {
    this.setDefaults()
  }

  get page () {
    return this.pageNumber
  }

  set page (newVal) {
    this.setPageNumber(newVal)
    this.setPageInUrl(false)
  }

  get size (): number {
    return this.pageSize
  }

  set size (newVal: number) {
    this.setPageSize(newVal)
    this.setSizeInUrl(false)
    this.runSearch()
  }

  get pageSizeItems (): number[] {
    const resultSet = new Set([
      ...this.pageSizes,
      this.getSizeFromUrl()
    ])
    return Array.from(resultSet).sort((a, b) => a - b)
  }

  async runInitialSearch (): Promise<void> {
    this.page = this.getPageFromUrl()
    this.size = this.getSizeFromUrl()

    await this.runSearch()
  }

  basicSearch () {
    // Important to set page to one otherwise it's possible that you don't anything
    this.page = 1
    this.runSearch()
  }

  clearSearch () {
    this.searchText = ''
    this.initUrlQueryParams()
  }

  async runSearch () {
    try {
      this.loading = true
      this.initUrlQueryParams()
      await this.searchContactsPaginated(this.searchText)
      this.setPageInUrl()
      this.setSizeInUrl()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of contacts failed')
    } finally {
      this.loading = false
    }
  }

  initDeleteDialog (contact: Contact) {
    this.showDeleteDialog = true
    this.contactToDelete = contact
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.contactToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.contactToDelete === null || this.contactToDelete.id === null) {
      return
    }

    try {
      this.loading = true
      await this.deleteContact(this.contactToDelete.id)
      this.runSearch()// to update the list
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
  }

  getPageFromUrl (): number {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 1
    }
    return 1
  }

  setPageInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(this.page)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }

  initSearchQueryParams (): void {
    if (this.$route.query.searchText) {
      this.searchText = this.$route.query.searchText as string
    }
  }

  initUrlQueryParams (): void {
    const params: {[key: string]: string} = {}

    if (this.searchText) {
      params.searchText = this.searchText
    }
    this.$router.push({
      query: params,
      hash: this.$route.hash
    })
  }

  getSizeFromUrl (): number {
    if ('size' in this.$route.query && typeof this.$route.query.size === 'string') {
      return parseInt(this.$route.query.size) ?? this.size
    }
    return this.size
  }

  setSizeInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.size) {
      // add size to the current url params
      query = {
        ...this.$route.query,
        size: String(this.size)
      }
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_search.scss";
.progress-spinner {
  position: absolute;
  top: 40vh;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 32px;
  z-index: 99;
}
</style>
