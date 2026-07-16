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
          v-if="editable"
          save-btn-text="apply"
          :to="'/organizations/' + organizationId + '/basic'"
          @save="save"
        />
      </v-card-actions>
      <organization-basic-data-form
        v-if="organizationCopy"
        ref="basicForm"
        v-model="organizationCopy"
      />
      <v-card-actions>
        <v-spacer />
        <save-and-cancel-buttons
          v-if="editable"
          save-btn-text="apply"
          :to="'/organizations/' + organizationId + '/basic'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, mixins, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'
import { Organization } from '@/models/Organization'
import { LoadOrganizationAction, OrganizationsState, SaveOrganizationAction } from '@/store/organizations'
import { SetTitleAction } from '@/store/appbar'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import OrganizationBasicDataForm from '@/components/organizations/OrganizationBasicDataForm.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    OrganizationBasicDataForm
  },
  computed: {
    ...mapState('organizations', ['organization'])
  },
  middleware: ['auth'],
  methods: {
    ...mapActions('appbar', ['setTitle']),
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('organizations', ['loadOrganization', 'saveOrganization'])
  }
})
export default class OrganizationEditPage extends mixins(CheckEditAccess) {
  private organizationCopy: Organization = new Organization()

  organization!: OrganizationsState['organization']
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  loadOrganization!: LoadOrganizationAction
  saveOrganization!: SaveOrganizationAction

  getRedirectUrl (): string {
    return '/organizations/' + this.organizationId
  }

  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this organization.'
  }

  created () {
    if (this.organization) {
      this.organizationCopy = Organization.createFromObject(this.organization)
    }
  }

  get organizationId (): string {
    return this.$route.params.organizationId
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    try {
      this.setLoading(true)
      await this.saveOrganization(this.organizationCopy)
      this.loadOrganization({ organizationId: this.organizationId })
      this.$router.push('/organizations/' + this.organizationId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Saving of organization failed')
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('organization', { immediate: true, deep: true })
  onOrganizationChanged (value: OrganizationsState['organization']) {
    if (value) {
      this.organizationCopy = Organization.createFromObject(value)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
