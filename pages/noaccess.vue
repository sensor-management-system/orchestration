<template>
  <v-container fill-height fluid>
    <v-row
      align="center"
      justify="center"
    >
      <v-col>
        <v-card>
          <v-alert type="error" class="text-center" :icon="false">
            <h1 class="display-4">
              Access not allowed!
            </h1>
            <h2 class="display-2">
              Log in!
            </h2>
          </v-alert>
        </v-card>
        <div class="text-center">
          <h4>Redirect Uri</h4>
          {{ $route.query.redirect }}
        </div>
        <div>
          <h4>IsLoggedIn</h4>
          {{ isLoggedIn }}
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AccessDenied',
  computed: {
    isLoggedIn () {
      return this.$store.getters['auth/isAuthenticated']
    }
  },
  watch: {
    isLoggedIn () {
      this.redirectUserIfLoggedIn()
    }
  },
  mounted () {
    this.redirectUserIfLoggedIn()
  },
  methods: {
    redirectUserIfLoggedIn () {
      if (this.isLoggedIn) {
        let redirectRoute = '/'
        if (this.$route.query.redirect !== undefined) {
          redirectRoute = this.$route.query.redirect
        }
        this.$router.push(redirectRoute)
      }
    }
  }
}
</script>
