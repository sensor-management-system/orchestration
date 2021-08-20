A dialog to confirm the deletion of an action.

## Usage

### Standard Usage

```vue
<template>
  <section>
    <v-btn @click="showDialog = true">Show Dialog</v-btn>
    <ActionDeleteDialog
      v-model="showDialog"
      @delete-dialog-button-click="showDialog = false"
    />
  </section>
</template>

<script>
  export default {
    data () {
      return {
        showDialog: false
      }
    }
  }
</script>
```
