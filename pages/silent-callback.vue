<template>
    <div></div>
</template>

<script>
    import {mapActions} from 'vuex'
    export default {
        name: "SilentRenewCallback",
        methods: {
            ...mapActions( 'auth',[
                'handleSilentRenewCallback'
            ])
        },
        created() {
            this.handleSilentRenewCallback()
                .catch((err) => {
                    console.error(err) // Handle errors any way you want
                })
        }
    }
</script>

<style scoped>

</style>