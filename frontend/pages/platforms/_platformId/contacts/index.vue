<!--
SPDX-FileCopyrightText: 2020 - 2023
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
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
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="contactsWithRoles.length === 0">
      There are no contacts for this platform.
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
      v-if="contactsWithRoles.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { RemovePlatformContactRoleAction, LoadPlatformContactRolesAction } from '@/store/platforms'

import HintCard from '@/components/HintCard.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import BaseList from '@/components/shared/BaseList.vue'
import ContactWithRolesListItem from '@/components/contacts/ContactWithRolesListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import { RoleNameMixin } from '@/mixins/RoleNameMixin'

@Component({
  components: {
    DotMenuActionDelete,
    ContactWithRolesListItem,
    BaseList,
    HintCard
  },
  computed: {
    ...mapState('platforms', ['platformContactRoles']),
    ...mapGetters('platforms', ['contactsWithRoles']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('platforms', ['removePlatformContactRole', 'loadPlatformContactRoles']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformShowContactPage extends mixins(RoleNameMixin) {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  removePlatformContactRole!: RemovePlatformContactRoleAction
  loadPlatformContactRoles!: LoadPlatformContactRolesAction
  setLoading!: SetLoadingAction

  get platformId (): string {
    return this.$route.params.platformId
  }

  async removeContactRole (contactRoleId: string) {
    try {
      this.setLoading(true)
      await this.removePlatformContactRole({
        platformContactRoleId: contactRoleId
      })
      this.$store.commit('snackbar/setSuccess', 'Role removed')
      this.loadPlatformContactRoles(this.platformId)
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
