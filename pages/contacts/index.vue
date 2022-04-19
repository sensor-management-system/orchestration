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
          @keydown.enter="search"
        />
      </v-col>
      <v-col
        cols="12"
        md="7"
        align-self="center"
      >
        <v-btn
          color="primary"
          small
          @click="search"
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

      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="search"
      />
      <BaseList
        :list-items="contacts"
      >
        <template v-slot:list-item="{item}">
          <ContactsListItem
            :key="item.id"
            :contact="item"
          >
            <template #dot-menu-items>
                  <DotMenuActionDelete
                    :readonly="!$auth.loggedIn"
                    @click="initDeleteDialog(item)"
                  />
            </template>
          </ContactsListItem>
        </template>
      </BaseList>
      <v-pagination
        v-model="page"
        :disabled="loading"
        :length="totalPages"
        :total-visible="7"
        @input="search"
      />
    </div>
    <ContacsDeleteDialog
      v-model="showDeleteDialog"
      :contact-to-delete="contactToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
    <v-btn
      v-if="$auth.loggedIn"
      bottom
      color="primary"
      dark
      elevation="10"
      fab
      fixed
      right
      to="/contacts/new"
    >
      <v-icon>
        mdi-plus
      </v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import {mapState,mapActions} from 'vuex';

import { Contact } from '@/models/Contact'

import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'

import BaseList from '@/components/shared/BaseList.vue'
import ContactsListItem from '@/components/contacts/ContactsListItem.vue'

@Component({
  components: {
    ContactsListItem,
    BaseList,
    ContacsDeleteDialog,
    DotMenuActionDelete
  },
  computed:mapState('contacts',['pageNumber','pageSize','totalPages','contacts']),
  methods:{
    ...mapActions('contacts',['searchContactsPaginated','setPageNumber','deleteContact']),
    ...mapActions('appbar',['init','setDefaults'])
  }
})
export default class SearchContactsPage extends Vue {

  private loading: boolean = false
  private searchText: string = ''

  private showDeleteDialog: boolean = false
  private contactToDelete: Contact | null = null

  get page(){
    return this.pageNumber;
  }

  set page(newVal){
    this.setPageNumber(newVal);
    this.setPageInUrl(false);
  }

  async created () {
    await this.init({
      tabs: [],
      title: 'Contacts',
      saveBtnHiden: true,
      cancelBtnHidden: true
    });
    this.setPageFromUrl();
    this.search();
  }

  beforeDestroy () {
    this.setDefaults();
  }

  async search(){
    try{
      this.loading=true;
      await this.searchContactsPaginated(this.searchText);
    }catch (e){
      this.$store.commit('snackbar/setError', 'Loading of contacts failed')
    }finally {
      this.loading=false;
    }
  }
  clearSearch () {
    this.searchText = ''
  }
  setPageFromUrl():void{
    const urlPage = this.getPageFromUrl();
    this.setPageNumber(urlPage);
  }
  getPageFromUrl (): number | undefined {
    if ('page' in this.$route.query && typeof this.$route.query.page === 'string') {
      return parseInt(this.$route.query.page) || 1
    }
    return 1;
  }
  setPageInUrl (preserveHash: boolean = true): void {
    let query: QueryParams = {}
    if (this.page) {
      // add page to the current url params
      query = {
        ...this.$route.query,
        page: String(this.page)
      }
    } else {
      // remove page from the current url params
      const {
        // eslint-disable-next-line
        page,
        ...params
      } = this.$route.query
      query = params
    }
    this.$router.push({
      query,
      hash: preserveHash ? this.$route.hash : ''
    })
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

    this.loading = true
    try {
      await this.deleteContact(this.contactToDelete.id)
      this.search();//to update the list
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    } finally {
      this.loading = false
      this.closeDialog()
    }
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
