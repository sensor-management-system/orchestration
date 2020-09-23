<template>
  <div />
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LogoutCallback',
  fetch ({ store }) {
    store.commit('increment')
  },
  created () {
    this.handleSignoutPopupCallback().catch((err) => {
      // eslint-disable-next-line
      console.error(err) // Handle errors any way you want
    })
  },
  methods: {
    ...mapActions('auth', ['handleSignoutPopupCallback'])
  }
}
</script>
