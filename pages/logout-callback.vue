<template>
    <div></div>
</template>

<script>
    import {mapActions} from 'vuex'

    export default {
        name: "logout-callback",
        fetch ({ store }) {
            store.commit('increment')
        },
        methods: {
            ...mapActions( 'auth',[
                'handleSignoutPopupCallback'
            ])
        },
        created() {
            this.handleSignoutPopupCallback()
                .catch((err) => {
                    console.error(err) // Handle errors any way you want
                })
        }
    }
</script>

<style scoped>

</style>
