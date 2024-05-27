<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
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
        :to="'/devices/' + deviceId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="contactsWithRoles.length === 0">
      There are no contacts for this device.
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
        :to="'/devices/' + deviceId + '/contacts/new'"
      >
        Assign contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadDeviceContactRolesAction, RemoveDeviceContactRoleAction } from '@/store/devices'

import { RoleNameMixin } from '@/mixins/RoleNameMixin'

import HintCard from '@/components/HintCard.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import BaseList from '@/components/shared/BaseList.vue'
import ContactWithRolesListItem from '@/components/contacts/ContactWithRolesListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

@Component({
  components: {
    DotMenuActionDelete,
    ContactWithRolesListItem,
    BaseList,
    HintCard
  },
  computed: {
    ...mapState('devices', ['deviceContactRoles']),
    ...mapGetters('devices', ['contactsWithRoles']),
    ...mapState('vocabulary', ['cvContactRoles'])
  },
  methods: {
    ...mapActions('devices', ['loadDeviceContactRoles', 'removeDeviceContactRole']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DeviceShowContactPage extends mixins(RoleNameMixin) {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  removeDeviceContactRole!: RemoveDeviceContactRoleAction
  loadDeviceContactRoles!: LoadDeviceContactRolesAction
  setLoading!: SetLoadingAction

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async removeContactRole (contactRoleId: string) {
    try {
      this.setLoading(true)
      await this.removeDeviceContactRole({
        deviceContactRoleId: contactRoleId
      })
      this.$store.commit('snackbar/setSuccess', 'Role removed')
      this.loadDeviceContactRoles(this.deviceId)
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
