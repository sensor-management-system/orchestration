<template>
  <div class="user-profile">
    <div class="profile-card">
      <h1 class="profile-card__title">
        {{ userName }}
      </h1>
      <h2>Claims</h2>
      <p v-for="(value,claim) of claims" :key="claim" class="profile-card__subtitle">
        {{ claim }}: {{ value }}
      </p>
      <p>
        exp: {{ claims.exp | timeStampToDate }}
      </p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Profile',
  filters: {
    timeStampToDate (value) {
      if (!value) {
        return ''
      }
      const date = new Date(value * 1000)
      const day = '0' + date.getDate()
      const month = '0' + (date.getMonth() + 1)
      const year = date.getFullYear()
      const hours = date.getHours()
      const minutes = '0' + date.getMinutes()
      const seconds = '0' + date.getSeconds()

      return day.substr(-2) + '.' +
        month.substr(-2) + '.' +
        year + ' ' +
        hours + ':' +
        minutes.substr(-2) + ':' +
        seconds.substr(-2)
    }
  },
  data: () => ({
    //
  }),
  computed: {
    userName () {
      return this.$store.getters['auth/username']
    },
    claims () {
      return this.$store.getters['auth/allUserClaims']
    }
  }
}
</script>

<style scoped>
.profile-card {
  background-color: #fff;
  color: #000;
  padding: 15vmin 20vmin;
  text-align: center;
}

.profile-card__title {
  margin: 0;
  font-size: 36px;
}

.profile-card__subtitle {
  margin: 0;
  color: #c0c0c0;
  font-size: 18px;
  margin-bottom: 5px;
}
</style>
