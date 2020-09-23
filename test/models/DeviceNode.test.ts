import Device from '@/models/Device'
import { DeviceNode } from '@/models/DeviceNode'

describe('DeviceNode', () => {
  it('should create a DeviceNode object', () => {
    const device = new Device()
    device.id = '1'

    const node = new DeviceNode(device)
    expect(Object.is(node.unpack(), device)).toBeTruthy()
    expect(node).toHaveProperty('id', '1')
  })

  it('should create a DeviceNode from another one', () => {
    const firstDevice = new Device()
    firstDevice.id = '1'

    const firstNode = new DeviceNode(firstDevice)
    const secondNode = DeviceNode.createFromObject(firstNode)

    expect(Object.is(secondNode, firstNode)).toBeFalsy()
    expect(Object.is(secondNode.unpack(), firstNode.unpack())).toBeTruthy()
  })

  it('should not be allowed to have children', () => {
    const device = new Device()

    const node = new DeviceNode(device)
    expect(node.canHaveChildren()).toBeFalsy()
  })
})
