<template>
    <div class="user-profile">
        <div class="profile-card">
            <h1 class="profile-card__title">{{userName}}</h1>
            <h2>Claims</h2>
            <p v-for="(value,claim) of claims" class="profile-card__subtitle" :key="claim">
                {{claim}}: {{value}}
            </p>
            <p>
                exp: {{claims.exp | timeStampToDate}}
            </p>
        </div>
    </div>
</template>

<script>

    export default {
        name: "Profile",
        data: () => ({
            //
        }),
        computed: {
            userName() {
                return this.$store.getters['auth/username'];
            },
            claims() {
                return this.$store.getters['auth/allUserClaims'];
            }
        },
        filters: {
            timeStampToDate(value) {
                if (!value) return '';
                let date = new Date(value * 1000);
                let day = "0" + date.getDate();
                let month = "0" + (date.getMonth() + 1);
                let year = date.getFullYear();
                let hours = date.getHours();
                let minutes = "0" + date.getMinutes();
                let seconds = "0" + date.getSeconds();

                return day.substr(-2) + '.' +
                    month.substr(-2) + '.' +
                    year + ' ' +
                    hours + ':' +
                    minutes.substr(-2) + ':' +
                    seconds.substr(-2);
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