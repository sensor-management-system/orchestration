<template>
  <div>
    <template v-for="item in listItems" >
      <slot name="list-item" :item="item">

      </slot>
    </template>

  </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component
export default class BaseList extends Vue {
  @Prop({
    required:true
  })
  private listItems!:[];
}
</script>

<style scoped>

</style>
