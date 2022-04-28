<template>
<div>
  <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="$auth.loggedIn"
        >
          <template #actions>
            <DotMenuActionDelete
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
      <ContactBasicData
        v-if="contact"
        v-model="contact"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          color="primary"
          small
          nuxt
          :to="'/contacts/' + contactId + '/edit'"
        >
          Edit
        </v-btn>
        <DotMenu
          v-if="$auth.loggedIn"
        >
          <template #actions>
            <DotMenuActionDelete
              @click="initDeleteDialog"
            />
          </template>
        </DotMenu>
      </v-card-actions>
    <ContacsDeleteDialog
      v-model="showDeleteDialog"
      :contact-to-delete="contact"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </v-card>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { mapActions, mapState } from 'vuex'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ContactBasicData from '@/components/ContactBasicData.vue'
import ContacsDeleteDialog from '@/components/contacts/ContacsDeleteDialog.vue'

@Component({
  components: { ContacsDeleteDialog, ContactBasicData, DotMenuActionDelete, DotMenu },
  computed:mapState('contacts',['contact']),
  methods: {
    ...mapActions('contacts', ['deleteContact']),
    ...mapActions('appbar', ['initContactsContactIdIndexAppBar'])
  }
})
export default class ContactIndexPage extends Vue {
  showDeleteDialog=false;

  created(){
    this.initContactsContactIdIndexAppBar(this.contact)
  }

  get contactId () {
    return this.$route.params.contactId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {

    this.closeDialog()

    if (this.contact === null) {
      return
    }
    try{
      await this.deleteContact(this.contact.id)
      this.$router.push('/contacts')
      this.$store.commit('snackbar/setSuccess', 'Contact deleted')
    }catch (_error){
      this.$store.commit('snackbar/setError', 'Contact could not be deleted')
    }
  }
}
</script>

<style scoped>

</style>
