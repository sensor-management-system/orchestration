import Vue from 'vue'
import Vuetify from 'vuetify'

import { mount, createLocalVue } from '@vue/test-utils'

// @ts-ignore
import ConfigurationsPlatformDeviceSearch from '@/components/ConfigurationsPlatformDeviceSearch.vue'
import Device from '@/models/Device'
import Platform from '@/models/Platform'

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
          devicesResult
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
