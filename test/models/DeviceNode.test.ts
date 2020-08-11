import Device from '@/models/Device'
import { DeviceNode } from '@/models/DeviceNode'

describe('DeviceNode', () => {
  it('should create a DeviceNode object', () => {
    const device = new Device()
    device.id = 1

    const node = new DeviceNode(device)
    expect(node.unpack()).toBe(device)
    expect(node).toHaveProperty('id', 1)
    expect(node).toHaveProperty('type', 'device')
  })

  it('should create a DeviceNode from another one', () => {
    const firstDevice = new Device()
    firstDevice.id = 1

    const firstNode = new DeviceNode(firstDevice)
    const secondNode = DeviceNode.createFromObject(firstNode)

    expect(secondNode).not.toBe(firstNode)
    expect(secondNode.unpack()).toBe(firstNode.unpack())
  })

  it('should not be allowed to have children', () => {
    const device = new Device()

    const node = new DeviceNode(device)
    expect(node.canHaveChildren()).toBeFalsy()
  })
})
