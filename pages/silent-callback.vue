<template>
  <div />
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'SilentRenewCallback',
  created () {
    this.handleSilentRenewCallback().catch((err) => {
      console.error(err) // Handle errors any way you want
    })
  },
  methods: {
    ...mapActions('auth', ['handleSilentRenewCallback'])
  }
}
</script>
