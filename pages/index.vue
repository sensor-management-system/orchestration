<template>

  <v-container>
    <v-row>
                <v-col class="text-center">
                    <v-btn
                            color="primary"
                            v-if="isLoggedIn"
                            @click="silentRenew"
                    >
                        Silent Renew
                    </v-btn>
                </v-col>
            </v-row>
      <v-row v-if="!isLoggedIn">
          <v-col>
              <h1 class="display-1 text-center">You're not logged in</h1>
          </v-col>
      </v-row>
      <v-row v-if="isLoggedIn"
             class="text-center"
      >
          <v-col>
              <h1><kbd>{{username}}</kbd> you're now logged in.</h1>
            <h2>Go check you Profile</h2>
                <v-btn to="/profile">Show Profile</v-btn>
          </v-col>
      </v-row>
    <v-row justify="center">
      <v-col cols="12">
        <h1>Welcome to the Sensor Management System</h1>
        <p>The purpose of this application is to help scientists and technicans to...</p>
        <p>
          If you don't have an account, you can browse and view all datasets.<br>
          If you're already registered, you can login below
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="2">
        <v-text-field
          label="username"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-text-field
          label="password"
          type="password"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary">
          Login
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>

    export default {
        name: 'Home',
        data: () => ({
        }),
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
                return this.$store.getters['auth/isAuthenticated'];
            },
            username(){
                return this.$store.getters['auth/username'];
            }

        }

    }
</script>
