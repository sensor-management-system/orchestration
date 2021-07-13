<template>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="isLoggedIn && !(isAddActionPage || isEditActionPage)"
      color="primary"
      small
      :to="'/platforms/' + platformId + '/actions/new'"
    >
      Add Action
    </v-btn>
  </v-card-actions>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

@Component
export default class PlatformNewActionButton extends Vue {
  @Prop({ type: String, required: true }) platformId!:string;

  get isLoggedIn ():boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isEditActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/platforms\/' + this.platformId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  get isAddActionPage ():boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/platforms\/' + this.platformId + '\/actions\/new$'
    return !!this.$route.path.match(addUrl)
  }
}
</script>

<style scoped>

</style>
