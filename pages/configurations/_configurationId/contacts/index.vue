<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      :dark="isSaving"
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
      <template v-slot:list-item="{item}">
        <BaseEntityContactListItem
          :contact="item"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="removeContact(item.id)"
            ></DotMenuActionDelete>
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
import BaseList from '@/components/shared/BaseList.vue'
import BaseEntityContactListItem from '@/components/shared/BaseEntityContactListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import HintCard from '@/components/HintCard.vue'
import { mapActions,mapState } from 'vuex'

@Component({
  components: { HintCard, ProgressIndicator, DotMenuActionDelete, BaseEntityContactListItem, BaseList },
  computed:mapState('configurations',['configurationContacts']),
  methods:mapActions('configurations',['loadConfigurationContacts','removeConfigurationContact'])
})
export default class ConfigurationShowContactPage extends Vue {

  private isSaving = false

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async removeContact(contactId:string):void{

    try {
      this.isSaving = true
      await this.removeConfigurationContact({
        configurationId: this.configurationId,
        contactId: contactId
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
