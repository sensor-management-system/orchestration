<template>
  <div>
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/platforms/' + platformId + '/attachments/new'"
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <hint-card v-if="platformAttachments.length === 0">
      There are no attachments for this platform.
    </hint-card>

    <BaseList
      :list-items="platformAttachments"
    >
      <template v-slot:list-item="{item}">
        <PlatformsAttachmentListItem
          :attachment="item"
          :platform-id="platformId"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialog(item)"
            />
          </template>
        </PlatformsAttachmentListItem>
      </template>

    </BaseList>
    <v-card-actions
      v-if="platformAttachments.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
      >
        Add Attachment
      </v-btn>
    </v-card-actions>
    <PlatformsAttachmentDeleteDialog
      v-model="showDeleteDialog"
      :attachment-to-delete="attachmentToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import HintCard from '@/components/HintCard.vue'
import { mapActions, mapState } from 'vuex'
import BaseList from '@/components/shared/BaseList.vue'
import PlatformsAttachmentListItem from '@/components/platforms/PlatformsAttachmentListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import PlatformsAttachmentDeleteDialog from '@/components/platforms/PlatformsAttachmentDeleteDialog.vue'
import { Attachment } from '@/models/Attachment'
import { Platform } from '@/models/Platform'
@Component({
  components: { PlatformsAttachmentDeleteDialog, DotMenuActionDelete, PlatformsAttachmentListItem, BaseList, HintCard, ProgressIndicator },
  computed: mapState('platforms',['platformAttachments']),
  methods:mapActions('platforms',['loadPlatformAttachments','deletePlatformAttachment'])
})
export default class PlatformAttachmentShowPage extends Vue{
  private showDeleteDialog=false;
  private attachmentToDelete:Attachment|null=null;

  get platformId (): string {
    return this.$route.params.platformId
  }

  initDeleteDialog (attachment: Attachment) {
    this.showDeleteDialog = true
    this.attachmentToDelete = attachment
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.attachmentToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.attachmentToDelete === null || this.attachmentToDelete.id === null) {
      return
    }
    try {
      await this.deletePlatformAttachment(this.attachmentToDelete.id) // TODO returns a 500 error, but deletion is fine; probably backend problem
      this.$store.commit('snackbar/setSuccess', 'Attachment deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete attachment')
    } finally {
      this.closeDialog()
    }
    try{
      this.loadPlatformAttachments(this.platformId)
    }catch (_error) {
     console.log('error',_error);
    }
  }
}
</script>

<style scoped>

</style>
