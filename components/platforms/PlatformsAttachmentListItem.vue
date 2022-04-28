<template>
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-container>
        <v-row no-gutters>
          <v-avatar class="mt-0 align-self-center">
            <v-icon large>
              {{ filetypeIcon(attachment) }}
            </v-icon>
          </v-avatar>
          <v-col>
            <v-row
              no-gutters
            >
              <v-col>
                <v-card-subtitle>
                  {{ filename(attachment) }}
                </v-card-subtitle>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
                <DotMenu>
                  <template #actions>
                    <slot name="dot-menu-items">
                    </slot>
                  </template>
                </DotMenu>
              </v-col>
            </v-row>
            <v-row
              no-gutters
            >
              <v-col class="text-subtitle-1">
                <a :href="attachment.url" target="_blank" v-if="attachment.label">
                  <v-icon color="primary">mdi-open-in-new</v-icon>
                  {{ attachment.label }}
                </a>
                <a :href="attachment.url" target="_blank" v-else>
                  <v-icon color="primary">mdi-open-in-new</v-icon>
                </a>
              </v-col>
              <v-col
                align-self="end"
                class="text-right"
              >
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
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mixins, Prop } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'
import DotMenu from '@/components/DotMenu.vue'
import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
@Component({
  components: { DotMenuActionDelete, DotMenu }
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
