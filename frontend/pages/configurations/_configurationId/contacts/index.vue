<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
