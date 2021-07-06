<template>
  <v-timeline dense>
    <v-timeline-item
      v-for="(action, index) in actions"
      :key="index"
      :color="action.getColor()"
      class="mb-4"
      small
    >
      <GenericActionCard
        v-if="action.isGenericAction"
        v-model="actions[index]"
      >
        <template v-if="isLoggedIn" #menu>
          <platform-action-delete-menu
            :action="actions[index]"
          />
        </template>
        <template #actions>
          <v-btn
            v-if="isLoggedIn"
            :to="'/platforms/' + platformId + '/actions/generic-platform-actions/' + action.id + '/edit'"
            color="primary"
            text
            @click.stop.prevent
          >
            Edit
          </v-btn>
        </template>
      </GenericActionCard>
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import GenericActionCard from '@/components/GenericActionCard.vue'
import PlatformActionDeleteMenu from '@/components/platform/actions/PlatformActionDeleteMenu'

@Component({
  components: {
    PlatformActionDeleteMenu,
    GenericActionCard
  }
})
export default class PlatformActionTimeline extends Vue {
  @Prop({ default: () => [], type: Array }) actions!:[];

  @Prop({ type: String, required: true }) platformId!:string;

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>

<style scoped>

</style>
