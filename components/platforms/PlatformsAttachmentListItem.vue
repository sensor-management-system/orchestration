<template>
  <v-card  :key="attachment.id" class="mb-2">
    <v-list-item>
      <v-list-item-avatar>
        <v-icon large>
          {{ filetypeIcon(attachment) }}
        </v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-subtitle>
          {{ filename(attachment) }}
        </v-list-item-subtitle>
        <v-list-item-title v-if="attachment.label">
          <a :href="attachment.url" target="_blank">{{ attachment.label }}</a>
        </v-list-item-title>
        <v-list-item-title v-else>
          <a :href="attachment.url" target="_blank">
            <v-icon color="primary">mdi-open-in-new</v-icon>
          </a>
        </v-list-item-title>
        <v-list-item-action-text>
          <v-row>
            <v-col align-self="end" class="text-right">
              <v-btn
                v-if="$auth.loggedIn"
                color="primary"
                text
                small
                nuxt
                :to="'/platforms/' + platformId + '/attachments/' + attachment.id + '/edit'"
              >
                Edit
              </v-btn>
              <DotMenu
                v-if="$auth.loggedIn"
              >
                <template #actions>
                  <slot name="dot-menu-items">
                  </slot>
                </template>
              </DotMenu>
            </v-col>
          </v-row>
        </v-list-item-action-text>
      </v-list-item-content>
    </v-list-item>

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mixins, Prop } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'
import DotMenu from '@/components/DotMenu.vue'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
@Component({
  components: { DotMenu }
})
export default class PlatformsAttachmentListItem extends mixins(AttachmentsMixin) {
  @Prop({
    required:true,
    type: Object
  })
  private attachment!:Attachment;

  @Prop({
    required:true
  })
  private platformId!:string;

}
</script>

<style scoped>

</style>
