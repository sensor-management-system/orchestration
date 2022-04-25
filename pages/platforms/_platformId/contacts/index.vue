<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer/>
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="platformContacts.length === 0">
      There are no contacts for this platform.
    </hint-card>
    <BaseList
      :list-items="platformContacts"
    >
      <template v-slot:list-item="{item}">
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
      v-if="platformContacts.length > 3"
    >
      <v-spacer/>
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PlatformAddContactPage from '@/pages/platforms/_platformId/contacts/new.vue'
import { mapActions, mapState } from 'vuex'
import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import BaseList from '@/components/shared/BaseList.vue'
import BaseEntityContactListItem from '@/components/shared/BaseEntityContactListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

@Component({
  components: { DotMenuActionDelete, BaseEntityContactListItem, BaseList, ProgressIndicator, HintCard },
  computed: mapState('platforms', ['platformContacts']),
  methods:mapActions('platforms',['removePlatformContact','loadPlatformContacts'])
})
export default class PlatformShowContactPage extends Vue {

  private isSaving = false

  get platformId (): string {
    return this.$route.params.platformId
  }
  async removeContact (contactId: string): void {
    try {
      this.isSaving = true
      this.removePlatformContact({
        platformId: this.platformId,
        contactId: contactId
      })
      this.loadPlatformContacts(this.platformId);
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
