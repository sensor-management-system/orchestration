<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="configurationContacts.length === 0">
      There are no contacts for this configuration.
    </hint-card>
    <BaseList
      :list-items="configurationContacts"
    >
      <template #list-item="{item}">
        <BaseEntityContactListItem
          :contact="item"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="removeContact(item.id)"
            />
          </template>
        </BaseEntityContactListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="configurationContacts.length>3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import BaseList from '@/components/shared/BaseList.vue'
import BaseEntityContactListItem from '@/components/shared/BaseEntityContactListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import HintCard from '@/components/HintCard.vue'

@Component({
  components: { HintCard, ProgressIndicator, DotMenuActionDelete, BaseEntityContactListItem, BaseList },
  computed: mapState('configurations', ['configurationContacts']),
  methods: mapActions('configurations', ['loadConfigurationContacts', 'removeConfigurationContact'])
})
export default class ConfigurationShowContactPage extends Vue {
  private isSaving = false

  // vuex definition for typescript check
  loadConfigurationContacts!: (id: string) => void
  removeConfigurationContact!: ({
    configurationId,
    contactId
  }: { configurationId: string, contactId: string }) => void

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async removeContact (contactId: string) {
    try {
      this.isSaving = true
      await this.removeConfigurationContact({
        configurationId: this.configurationId,
        contactId
      })
      this.loadConfigurationContacts(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
