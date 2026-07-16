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
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/organizations/' + organizationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <dot-menu v-if="deletable">
          <template #actions>
            <dot-menu-action-delete @click="initDeleteDialog" />
          </template>
        </dot-menu>
      </v-card-actions>
      <organization-basic-data v-if="organization" v-model="organization" />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/organizations/' + organizationId + '/basic/edit'"
        >
          Edit
        </v-btn>
        <dot-menu v-if="deletable">
          <template #actions>
            <dot-menu-action-delete @click="initDeleteDialog" />
          </template>
        </dot-menu>
      </v-card-actions>
      <delete-dialog
        v-model="showDeleteDialog"
        title="Delete Organization"
        :disabled="isLoading"
        @cancel="closeDeleteDialog"
        @delete="deleteAndCloseDialog"
      >
        Do you really want to delete the organization <em>{{ organization.name }}</em>?
      </delete-dialog>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DeleteOrganizationAction, OrganizationsState } from '@/store/organizations'
import OrganizationBasicData from '@/components/organizations/OrganizationBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import { ErrorMessageDispatcher, sourceLowerCaseIncludes } from '@/utils/errorHelpers'

@Component({
  components: {
    OrganizationBasicData,
    DotMenu,
    DotMenuActionDelete,
    DeleteDialog
  },
  computed: {
    ...mapState('organizations', ['organization']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('organizations', ['deleteOrganization'])
  }
})
export default class OrganizationShowBasicPage extends Vue {
  @InjectReactive()
    editable!: boolean

  @InjectReactive()
    deletable!: boolean

  private showDeleteDialog: boolean = false

  organization!: OrganizationsState['organization']
  setLoading!: SetLoadingAction
  deleteOrganization!: DeleteOrganizationAction

  get organizationId () {
    return this.$route.params.organizationId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDeleteDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    if (this.organization === null || this.organization.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteOrganization(this.organization)
      this.$router.push('/organizations')
      this.$store.commit('snackbar/setSuccess', 'Organization deleted')
    } catch (e) {
      const msg = new ErrorMessageDispatcher()
        .forCase({
          // 409 is a conflict
          status: 409,
          predicate: sourceLowerCaseIncludes('associated contacts'),
          text: 'There are still contacts associated with the organization'
        })
        .defaultText('Organization could not be deleted')
        .dispatch(e)

      this.$store.commit('snackbar/setError', msg)
    } finally {
      this.setLoading(false)
      this.closeDeleteDialog()
    }
  }
}
</script>
