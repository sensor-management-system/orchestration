<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="contactsWithRoles.length === 0">
      There are no contacts for this configuration.
    </hint-card>
    <BaseList
      :list-items="contactsWithRoles"
    >
      <template #list-item="{item}">
        <contact-with-roles-list-item
          :key="item.contact.id"
          :value="item"
          :cv-contact-roles="cvContactRoles"
        >
          <template v-if="editable" #dot-menu-items>
            <DotMenuActionDelete
              v-for="role in item.roles"
              :key="role.id"
              :text="`Remove '${roleName(role, cvContactRoles)}' role`"
              @click="removeContactRole(role.id)"
            />
          </template>
        </contact-with-roles-list-item>
      </template>
    </BaseList>
    <v-card-actions
      v-if="contactsWithRoles.length>3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadConfigurationContactRolesAction, RemoveConfigurationContactRoleAction } from '@/store/configurations'

import BaseList from '@/components/shared/BaseList.vue'
import ContactWithRolesListItem from '@/components/contacts/ContactWithRolesListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import HintCard from '@/components/HintCard.vue'
import { RoleNameMixin } from '@/mixins/RoleNameMixin'

@Component({
  components: {
    HintCard,
    DotMenuActionDelete,
    ContactWithRolesListItem,
    BaseList
  },
  computed: {
    ...mapState('configurations', ['configurationContactRoles']),
    ...mapGetters('configurations', ['contactsWithRoles']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfigurationContactRoles', 'removeConfigurationContactRole']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationShowContactPage extends mixins(RoleNameMixin) {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  loadConfigurationContactRoles!: LoadConfigurationContactRolesAction
  removeConfigurationContactRole!: RemoveConfigurationContactRoleAction
  setLoading!: SetLoadingAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async removeContactRole (contactRoleId: string) {
    try {
      this.setLoading(true)
      await this.removeConfigurationContactRole({
        configurationContactRoleId: contactRoleId
      })
      this.$store.commit('snackbar/setSuccess', 'Role removed')
      this.loadConfigurationContactRoles(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Removing role failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
