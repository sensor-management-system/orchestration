<template>
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-card-text
        @click.stop.prevent="show = !show"
      >
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{ contact.toString() }}
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
            <v-btn
              icon
              @click.stop.prevent="show = !show"
            >
              <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-expand-transition>
        <v-card
          v-show="show"
          flat
          tile
          color="grey lighten-5"
        >
          <v-card-text>
            <v-row
              dense
            >
              <v-col
                cols="12"
                md="3"
              >
                <label>Given name:</label>
                {{ contact.givenName }}
              </v-col>
              <v-col
                cols="12"
                md="3"
              >
                <label>Family name:</label>
                {{ contact.familyName }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col
                cols="12"
                md="3"
              >
                <label>E-Mail:</label>
                {{ contact.email | orDefault }}
                <a v-if="contact.email.length > 0" :href="'mailto:' + contact.email">
                  <v-icon
                    small
                  >
                    mdi-email
                  </v-icon>
                </a>
              </v-col>
              <v-col
                cols="12"
                md="6"
              >
                <label>Website:</label>
                {{ contact.website | orDefault }}
                <a v-if="contact.website.length > 0" :href="contact.website" target="_blank">
                  <v-icon
                    small
                  >
                    mdi-open-in-new
                  </v-icon>
                </a>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import { Contact } from '@/models/Contact'
import DotMenu from '@/components/DotMenu.vue'
@Component({
  components: { DotMenu }
})
export default class BaseEntityContactListItem extends Vue {
  @Prop({
    required:true,
    type: Object
  })
  private contact!:Contact;

  private show = false;
}
</script>

<style scoped>

</style>
