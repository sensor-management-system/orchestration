<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />

    <platform-new-action-button />

    <template v-if="isAddActionPage">
      <NuxtChild
        @input="$fetch"
        @showsave="showsave"
      />
    </template>

    <template v-else-if="isEditActionPage">
      <NuxtChild
        @input="$fetch"
        @showload="showload"
        @showsave="showsave"
      />
    </template>

    <template v-else>
      <platform-action-timeline :actions="actions" />
      <platform-action-delete-dialog />
    </template>
  </div>
</template>

<script>
import PlatformActionTimeline from "@/components/platform/actions/PlatformActionTimeline";
import PlatformNewActionButton from "@/components/platform/actions/PlatformNewActionButton";
import ProgressIndicator from "@/components/ProgressIndicator";
import PlatformActionDeleteDialog from "@/components/platform/actions/PlatformActionDeleteDialog";

export default {
  name: "action",
  components: {PlatformActionDeleteDialog, PlatformNewActionButton, PlatformActionTimeline, ProgressIndicator}
}
</script>

<style scoped>

</style>
