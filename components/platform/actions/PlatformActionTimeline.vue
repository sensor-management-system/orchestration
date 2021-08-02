<template>
  <v-timeline dense>
    <v-timeline-item
      v-for="(action, index) in actions"
      :key="getActionTypeIterationKey(action)"
      :color="getColor(action)"
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
      <PlatformMountActionCard
        v-if="action.isPlatformMountAction"
        v-model="action.inner"
      />
      <PlatformUnmountActionCard
        v-if="action.isPlatformUnmountAction"
        v-model="action.inner"
      />
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import GenericActionCard from '@/components/GenericActionCard.vue'
import PlatformActionDeleteMenu from '@/components/platform/actions/PlatformActionDeleteMenu.vue'

import PlatformMountActionCard from '@/components/PlatformMountActionCard.vue'
import PlatformUnmountActionCard from '@/components/PlatformUnmountActionCard.vue'

import { GenericAction } from '@/models/GenericAction'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'

@Component({
  components: {
    PlatformActionDeleteMenu,
    GenericActionCard,
    PlatformMountActionCard,
    PlatformUnmountActionCard
  }
})
export default class PlatformActionTimeline extends Vue {
  @Prop({ default: () => [], type: Array }) actions!:[];

  @Prop({ type: String, required: true }) platformId!:string;

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  getColor (action: IActionCommonDetails): string {
    if ('isPlatformMountAction' in action) {
      return 'green'
    } else if ('isPlatformUnmountAction' in action) {
      return 'red'
    } else if ('isGenericAction' in action) {
      switch ((action as GenericAction).actionTypeName) {
        case 'Platform Application': return 'yellow'
        case 'Platform Maintenance': return 'blue'
        case 'Platform Observation': return 'orange'
        case 'Platform Visit': return 'brown'
      }
    }
    return 'gray'
  }

  getActionTypeIterationKey (action: IActionCommonDetails): string {
    return this.getActionType(action) + '-' + action.id
  }

  getActionType (action: IActionCommonDetails): string {
    switch (true) {
      case 'isGenericAction' in action:
        return 'generic-action'
      case 'isPlatformMountAction' in action:
        return 'platform-mount-action'
      case 'isPlatformUnmountAction' in action:
        return 'platform-unmount-action'
      default:
        return 'unknown-action'
    }
  }
}
</script>

<style scoped>

</style>
