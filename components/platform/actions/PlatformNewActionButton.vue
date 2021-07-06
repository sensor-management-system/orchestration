<template>
  <v-card-actions>
    <v-spacer/>
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

<script>
export default {
  name: "PlatformNewActionButton",
  computed: {
    platformId (){
      return this.$route.params.platformId
    },
    isLoggedIn(){
      return this.$store.getters['oidc/isAuthenticated']
    },
    isEditActionPage(){
      // eslint-disable-next-line no-useless-escape
      const editUrl = '^\/devices\/' + this.deviceId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
      return !!this.$route.path.match(editUrl)
    },
    isAddActionPage(){
      // eslint-disable-next-line no-useless-escape
      const addUrl = '^\/devices\/' + this.deviceId + '\/actions\/new$'
      return !!this.$route.path.match(addUrl)
    }
  }
}
</script>

<style scoped>

</style>
