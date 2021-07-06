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
        :disabled="!isLoggedIn"
        dense
        @click="showDeleteDialog(action)"
      >
        <v-list-item-content>
          <v-list-item-title :class="isLoggedIn ? 'red--text' : 'grey--text'">
            <v-icon
              left
              small
              :color="isLoggedIn ? 'red' : 'grey'"
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

<script>
export default {
  name: "PlatformActionDeleteMenu"
}
</script>

<style scoped>

</style>
