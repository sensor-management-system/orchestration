<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          :to="'/organizations'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <organization-basic-data-form ref="basicForm" v-model="organization" />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          :to="'/organizations'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions } from 'vuex'

import { Organization } from '@/models/Organization'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import OrganizationBasicDataForm from '@/components/organizations/OrganizationBasicDataForm.vue'
import { SaveOrganizationAction } from '@/store/organizations'
import { SetShowBackButtonAction, SetTitleAction } from '@/store/appbar'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  components: {
    SaveAndCancelButtons,
    OrganizationBasicDataForm
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('organizations', ['saveOrganization']),
    ...mapActions('appbar', ['setTitle', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }

})
export default class OrganizationNewPage extends Vue {
  private organization = new Organization()
  saveOrganization!: SaveOrganizationAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  created () {
    this.initializeAppBar()
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTitle('New Organization')
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      const savedOrganization = await this.saveOrganization(this.organization)
      const organizationId = savedOrganization.id
      this.$store.commit('snackbar/setSuccess', 'Organization created')
      this.$router.push(`/organizations/${organizationId}`)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Organization could not be created')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
