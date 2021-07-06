<template>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="isLoggedIn && !(isAddActionPage || isEditActionPage)"
      color="primary"
      small
      :to="'/platform/' + platformId + '/actions/new'"
    >
      Add Action
    </v-btn>
  </v-card-actions>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class PlatformNewActionButton extends Vue {
  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn ():boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/devices\/' + this.deviceId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isAddActionPage ():boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/devices\/' + this.deviceId + '\/actions\/new$'
    return !!this.$route.path.match(addUrl)
  }
}
</script>

<style scoped>

</style>
