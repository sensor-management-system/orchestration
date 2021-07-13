<template>
  <v-menu
    close-on-click
    close-on-content-click
    offset-x
    left
    z-index="999"
  >
    <template #activator="{ on }">
      <v-btn
        data-role="property-menu"
        icon
        small
        v-on="on"
      >
        <v-icon dense small>
          mdi-dots-vertical
        </v-icon>
      </v-btn>
    </template>

    <v-list>
      <v-list-item
        dense
        @click="showDeleteDialog"
      >
        <v-list-item-content>
          <v-list-item-title class="red--text">
            <v-icon
              left
              small
              color="red"
            >
              mdi-delete
            </v-icon>
            Delete
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'

@Component()
export default class PlatformActionDeleteMenu extends Vue {
  @Prop({ type: Object, required: true }) action!:IActionCommonDetails;

  showDeleteDialog () {
    this.$store.commit('smsActions/setActionIdToDelete', this.action.id)
  }
}
</script>

<style scoped>

</style>
