<template>
  <div>
    <template v-for="(item,index) in listItems">
      <slot name="list-item" :item="item" :index="index" />
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class BaseList extends Vue {
  @Prop({
    required: true
  })
  private listItems!: []
}
</script>

<style scoped>

</style>
