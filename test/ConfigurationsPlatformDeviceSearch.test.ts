/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

Vue.use(Vuetify)

describe('ConfigurationsPlatformDeviceSearch', () => {
  const createWrapper = (platformsResult: Platform[], devicesResult: Device[]) => {
    const localVue = createLocalVue()
    const vuetify = new Vuetify()

    return mount(ConfigurationsPlatformDeviceSearch, {
      localVue,
      vuetify,
      data () {
        return {
          platformsResult,
          devicesResult,
          searchOptions: {
            searchType: devicesResult.length ? 'Device' : 'Platform'
          }
        }
      }
    })
  }

  it('should trigger an add-platform event when a platform is added', async () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'a platform'

    const wrapper: any = createWrapper([platform], [])

    await wrapper.get('button[data-role="add-platform"]').trigger('click')
    expect(wrapper.emitted('add-platform')).toBeTruthy()
    expect(wrapper.emitted('add-platform').length).toBe(1)
    expect(wrapper.emitted('add-platform')[0]).toEqual([platform])
  })

  it('should trigger an add-device event when a device is added', async () => {
    const device = new Device()
    device.id = '1'
    device.shortName = 'a device'

    const wrapper: any = createWrapper([], [device])

    await wrapper.get('button[data-role="add-device"]').trigger('click')
    expect(wrapper.emitted('add-device')).toBeTruthy()
    expect(wrapper.emitted('add-device').length).toBe(1)
    expect(wrapper.emitted('add-device')[0]).toEqual([device])
  })
})
