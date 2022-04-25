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
        :to="'/devices/' + deviceId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceContacts.length === 0">
      There are no contacts for this device.
    </hint-card>
    <BaseList
      :list-items="deviceContacts"
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
      v-if="deviceContacts.length>3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import BaseList from '@/components/shared/BaseList.vue'
import BaseEntityContactListItem from '@/components/shared/BaseEntityContactListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'

@Component({
  components: { DotMenuActionDelete, BaseEntityContactListItem, BaseList, ProgressIndicator, HintCard },
  computed:mapState('devices',['deviceContacts']),
  methods:mapActions('devices',['loadDeviceContacts','removeDeviceContact'])
})
export default class DeviceShowContactPage extends Vue {

  private isSaving = false

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async removeContact(contactId:string):void{

    try {
      this.isSaving = true
      await this.removeDeviceContact({
        deviceId: this.deviceId,
        contactId: contactId
      })
      this.loadDeviceContacts(this.deviceId)
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
