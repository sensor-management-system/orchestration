<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-row
      dense
    >
      <v-col cols="12" md="5">
        <v-text-field
          v-model="searchText"
          label="Search term"
          placeholder="Search contacts"
          hint="Please enter at least 3 characters"
          @keydown.enter="basicSearch"
        />
      </v-col>
      <v-col
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

    <div
      v-if="contacts.length > 0"
    >
      <v-row
        no-gutters
        class="mt-10"
      >
        <v-col
          cols="12"
          md="3"
        >
          <v-subheader>
            <FoundEntries v-model="totalCount" entity-name="contact" />
            <v-spacer />
          </v-subheader>
        </v-col>
        <v-col
          cols="12"
          md="6"
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
          cols="12"
          md="3"
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
              v-if="$auth.loggedIn && canDeleteContact(item)"
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
    <DeleteDialog
      v-if="contactToDelete"
      v-model="showDeleteDialog"
      title="Delete Contact"
      :disabled="loading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the contact <em>{{ contactToDelete.fullName }}</em>?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState, mapGetters } from 'vuex'

import { SetTitleAction, SetTabsAction } from '@/store/appbar'
import {
  ContactsState,
  PageSizesGetter,
  SearchContactsPaginatedAction,
  SetPageNumberAction,
  SetPageSizeAction,
  DeleteContactAction
} from '@/store/contacts'

import { Contact } from '@/models/Contact'

import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import PageSizeSelect from '@/components/shared/PageSizeSelect.vue'
import BaseList from '@/components/shared/BaseList.vue'
import ContactsListItem from '@/components/contacts/ContactsListItem.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { QueryParams } from '@/modelUtils/QueryParams'
import { CanDeleteContactGetter } from '@/store/permissions'
import FoundEntries from '@/components/shared/FoundEntries.vue'

@Component({
  components: {
    FoundEntries,
    ContactsListItem,
    BaseList,
    DeleteDialog,
    DotMenuActionDelete,
    PageSizeSelect,
    ProgressIndicator
  },
  computed: {
    ...mapState('contacts', ['pageNumber', 'pageSize', 'totalPages', 'totalCount', 'contacts']),
    ...mapGetters('contacts', ['pageSizes']),
    ...mapGetters('permissions', ['canDeleteContact'])
  },
  methods: {
    ...mapActions('contacts', ['searchContactsPaginated', 'setPageNumber', 'setPageSize', 'deleteContact']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])
  }
})
export default class SearchContactsPage extends Vue {
  private loading: boolean = false
  private searchText: string = ''

  private showDeleteDialog: boolean = false
  private contactToDelete: Contact | null = null

  // vuex definition for typescript check
  pageNumber!: ContactsState['pageNumber']
  setPageNumber!: SetPageNumberAction
  pageSize!: ContactsState['pageSize']
  setPageSize!: SetPageSizeAction
  pageSizes!: PageSizesGetter
  totalCount!: ContactsState['totalCount']
  searchContactsPaginated!: SearchContactsPaginatedAction
  deleteContact!: DeleteContactAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  canDeleteContact!: CanDeleteContactGetter

  async created () {
    if (!this.$auth.loggedIn) {
      this.$router.replace('/', () => {
        this.$store.commit('snackbar/setError', 'Login is required to see this page.')
      })
      return
    }

    try {
      this.loading = true
      this.initializeAppBar()
      this.initSearchQueryParams()
      await this.runInitialSearch()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of contacts failed')
    } finally {
      this.loading = false
    }
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
    const sizeChanged: boolean = this.size !== newVal

    this.setPageSize(newVal)
    this.setSizeInUrl(false)

    if (sizeChanged) {
      this.runSearch()
    }
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
      this.setPageAndSizeInUrl()
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

  initializeAppBar () {
    this.setTitle('Contacts')
    this.setTabs([])
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

  setPageAndSizeInUrl (preserveHash: boolean = true): void {
    // In general it should be possible to just call
    // setPageInUrl()
    // and
    // setSizeInUrl()
    // However, it seems that setSizeInUrl removes the page parameter then.
    // So we do both in one run.
    let query: QueryParams = {
      ...this.$route.query
    }
    if (this.size) {
      // add size to the current url params
      query = {
        ...query,
        size: String(this.size)
      }
    }
    if (this.page) {
      // add query to the current url params
      query = {
        ...query,
        page: String(this.page)
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
