/* SPDX-FileCopyrightText: 2020 - 2024
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Vue, Component } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import {
  ConfigurationsState,
  SetSelectedLocationDateAction,
  SetSelectedTimepointItemAction
} from '@/store/configurations'

@Component({
  computed: {
    ...mapState('configurations', ['selectedTimepointItem', 'configurationLocationActionTimepoints'])
  },
  methods: {
    ...mapActions('configurations', ['setSelectedTimepointItem', 'setSelectedLocationDate'])
  }
})
export class LocationSelectList extends Vue {
  // vuex definition for typescript check
  selectedTimepointItem!: ConfigurationsState['selectedTimepointItem']
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  setSelectedTimepointItem!: SetSelectedTimepointItemAction
  setSelectedLocationDate!: SetSelectedLocationDateAction

  setSelectListItemIfMissingAndUpdateSelectedDate (id: string, type: string) {
    if (this.selectedTimepointItem === null || (this.selectedTimepointItem.type !== type || this.selectedTimepointItem.id !== id)) {
      this.findSelectListItemAndSetTimepointAndDate(id, type)
    }
  }

  findSelectListItemAndSetTimepointAndDate (id: string, type: string) {
    const found = this.configurationLocationActionTimepoints.find((item: ILocationTimepoint) => {
      return item.type === type && item.id === id
    }) as ILocationTimepoint | undefined
    if (found) {
      this.setSelectedTimepointItem(found)
      this.setSelectedLocationDate(found.timepoint)
    }
  }
}
