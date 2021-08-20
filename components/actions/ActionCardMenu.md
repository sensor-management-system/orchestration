A menu with action related menu items.

## Usage

### Standard Usage

```vue
<template>
  <v-card
    v-if="showCard"
  >
    <v-card-subtitle>
      <v-row no-gutters>
        <v-col>
          A simple card with a menu
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <ActionCardMenu
            :value="action"
            @delete-menu-item-click="hideCard"
          />
        </v-col>
      </v-row>
    </v-card-subtitle>
  </v-card>
</template>

<script>
  import { ActionCommonDetails } from '@/models/ActionCommonDetails'

  export default {
    data () {
      return {
        action: new ActionCommonDetails(),
        showCard: true
      }
    },
    methods: {
      hideCard: function () {
        this.showCard = false
        setTimeout(() => this.showCard = true, 2000)
      }
    }
  }
</script>
```
