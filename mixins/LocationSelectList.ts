// Web client of the Sensor Management System software developed within the
// Helmholtz DataHub Initiative by GFZ and UFZ.
//
// Copyright (C) 2020, 2021
// - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
// - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
// - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
// - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
// - Helmholtz Centre Potsdam - GFZ German Research Centre for
//   Geosciences (GFZ, https://www.gfz-potsdam.de)
// - Helmholtz Centre for Environmental Research GmbH - UFZ
// (UFZ, https://www.ufz.de)
//
// Parts of this program were developed within the context of the
// following publicly funded projects or measures:
//   - Helmholtz Earth and Environment DataHub
// (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
//
// Licensed under the HEESIL, Version 1.0 or - as soon they will be
// approved by the "Community" - subsequent versions of the HEESIL
// (the "Licence").
//
// You may not use this work except in compliance with the Licence.
//
//   You may obtain a copy of the Licence at:
//   https://gitext.gfz-potsdam.de/software/heesil
//
//     Unless required by applicable law or agreed to in writing, software
// distributed under the Licence is distributed on an "AS IS" basis,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
// implied. See the Licence for the specific language governing
// permissions and limitations under the Licence.

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
