<template>
  <v-timeline dense>
    <v-timeline-item
      v-for="(action, index) in actions"
      :key="getActionTypeIterationKey(action)"
      :color="action.getColor()"
      class="mb-4"
      small
    >
      <GenericActionCard
        v-if="action.isGenericAction"
        v-model="actions[index]"
      >
        <template v-if="isLoggedIn" #menu>
          <platform-action-delete-menu />
        </template>
        <template #actions>
          <v-btn
            v-if="isLoggedIn"
            :to="'/devices/' + deviceId + '/actions/generic-device-actions/' + action.id + '/edit'"
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

<script>
import GenericActionCard from '@/components/GenericActionCard.vue'
import PlatformActionDeleteMenu from "@/components/platform/actions/PlatformActionDeleteMenu";

export default {
  name: "PlatformActionTimeline",
  props: ["actions"],
  components: {PlatformActionDeleteMenu, GenericActionCard}
}
</script>

<style scoped>

</style>
