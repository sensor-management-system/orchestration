<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list nav>
        <!-- Home -->
        <v-list-item to="/" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-apps</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Devices -->
        <v-list-item to="/devices" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-network</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Devices</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Projects -->
        <v-list-item to="/projects" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-nature-people</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Projects</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Users -->
        <v-list-item to="/users" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Users</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <!-- Help -->
        <v-list-item to="/help" nuxt exact>
          <v-list-item-action>
            <v-icon>mdi-help-circle-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Help</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn
          color="primary"
          v-if="!isLoggedIn"
          @click="loginPopup"
      >
        OIDC_login
      </v-btn>
      <v-btn
          color="primary"
          v-if="isLoggedIn"
          light
          @click="logoutPopup"
      >
          Logout
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer
      :fixed="fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      miniVariant: false,
      title: 'Sensor System Management'
    }
  },
    mounted() {
      this.$store.dispatch('auth/loadStoredUser');
    },
    methods: {
      loginPopup() {
        this.$store.dispatch('auth/loginPopup');
      },
      logoutPopup() {
        let routing = {
          router: this.$router,
          currentRoute: this.$route.path
        };
        this.$store.dispatch('auth/logoutPopup', routing);
      },
      silentRenew(){
        this.$store.dispatch('auth/silentRenew');
      }
    },
    computed: {
      isLoggedIn() {
        return this.$store.getters["auth/isAuthenticated"]
      }
    }
}
</script>
