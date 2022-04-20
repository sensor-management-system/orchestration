<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
 <NuxtChild/>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'

import { AttachmentsMixin } from '@/mixins/AttachmentsMixin'

import AttachmentListItem from '@/components/AttachmentListItem.vue'
import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { mapActions } from 'vuex'

@Component({
  components: {
    AttachmentListItem,
    HintCard,
    ProgressIndicator
  },
  methods:mapActions('platforms',['loadPlatformAttachments'])
})
export default class PlatformAttachmentsPage extends mixins(AttachmentsMixin) {

  private isLoading = false
  async created(){
    try {
      this.isLoading = true;
      this.loadPlatformAttachments(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'failed to fetch attachments')
    } finally {
      this.isLoading = false
    }
  }

  // async fetch () {
  //   this.isLoading = true
  //   try {
  //     this.attachments = await this.$api.platforms.findRelatedPlatformAttachments(this.platformId)
  //     this.isLoading = false
  //   } catch (e) {
  //     this.$store.commit('snackbar/setError', 'failed to fetch attachments')
  //     this.isLoading = false
  //   }
  // }

  head () {
    return {
      titleTemplate: 'Attachments - %s'
    }
  }
  //
  // get isInProgress (): boolean {
  //   return this.isLoading || this.isSaving
  // }

  get platformId (): string {
    return this.$route.params.platformId
  }

  // get isEditAttachmentPage (): boolean {
  //   // eslint-disable-next-line no-useless-escape
  //   const editUrl = '^\/platforms\/' + this.platformId + '\/attachments\/([0-9]+)\/edit$'
  //   return !!this.$route.path.match(editUrl)
  // }
  //
  // get isAddAttachmentPage (): boolean {
  //   // eslint-disable-next-line no-useless-escape
  //   const addUrl = '^\/platforms\/' + this.platformId + '\/attachments\/new$'
  //   return !!this.$route.path.match(addUrl)
  // }
  //
  // showsave (shouldShowSave: boolean) {
  //   this.isSaving = shouldShowSave
  // }

  // addAttachmentToList (newAttachment: Attachment) {
  //   this.attachments.push(newAttachment)
  // }

  // deleteAndCloseDialog (id: string) {
  //   if (id) {
  //     this.isSaving = true
  //     this.showDeleteDialog = {}
  //
  //     this.$api.platformAttachments.deleteById(id).then(() => {
  //       const searchIndex = this.attachments.findIndex(a => a.id === id)
  //       if (searchIndex > -1) {
  //         this.attachments.splice(searchIndex, 1)
  //       }
  //       this.isSaving = false
  //     }).catch((_error) => {
  //       this.isSaving = false
  //       this.$store.commit('snackbar/setError', 'Failed to delete attachment')
  //     })
  //   }
  // }

  // showDeleteDialogFor (id: string) {
  //   Vue.set(this.showDeleteDialog, id, true)
  // }
  //
  // hideDeleteDialogFor (id: string) {
  //   Vue.set(this.showDeleteDialog, id, false)
  // }
  //
  // isEditModeForAttachment (attachment: Attachment): boolean {
  //   return this.$route.path === '/platforms/' + this.platformId + '/attachments/' + attachment.id + '/edit'
  // }
}
</script>
