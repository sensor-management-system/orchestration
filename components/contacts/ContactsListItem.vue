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
          no.gutters
        >
          <v-col>
            <div class="'text-caption text-disabled">
              {{ contact.email }}
            </div>
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <DotMenu>
              <template #actions>
                <slot name="dot-menu-items" />
              </template>
            </DotMenu>
          </v-col>
        </v-row>
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{ contact.fullName }}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              :to="'/contacts/' + contact.id"
              color="primary"
              text
              @click.stop.prevent
            >
              View
            </v-btn>
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
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Given name:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ contact.givenName }}
              </v-col>
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Family name:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ contact.familyName }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Website:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ contact.website }}
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
export default class ContactsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private contact!: Contact

  private show = false
}
</script>

<style scoped>

</style>
