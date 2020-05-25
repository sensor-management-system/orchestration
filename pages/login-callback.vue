<template>
    <div></div>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        name: "login-callback",
        fetch ({ store }) {
            store.commit('increment')
        },
        methods: {
            ...mapActions( 'auth',[
                'handleSigninPopupCallback'
            ])
        },
        created() {
            this.handleSigninPopupCallback()
                .catch((err) => {
                    console.error(err) // Handle errors any way you want
                })
        }
    }
</script>

<style scoped>

</style>
