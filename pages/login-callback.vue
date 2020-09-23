<template>
  <div />
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LoginCallback',
  fetch ({ store }) {
    store.commit('increment')
  },
  created () {
    this.handleSigninPopupCallback().catch((err) => {
      console.error(err) // Handle errors any way you want
    })
  },
  methods: {
    ...mapActions('auth', ['handleSigninPopupCallback'])
  }
}
</script>
