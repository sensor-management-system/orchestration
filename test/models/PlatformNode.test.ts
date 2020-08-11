import Platform from '@/models/Platform'
import { PlatformNode } from '@/models/PlatformNode'

describe('PlatformNode', () => {
  it('should create a PlatformNode object', () => {
    const platform = new Platform()
    platform.id = 1

    const node = new PlatformNode(platform)
    expect(node.unpack()).toBe(platform)
    expect(node).toHaveProperty('id', 1)
  })

  it('should create a PlatformNode from another one', () => {
    const firstPlatform = new Platform()
    firstPlatform.id = 1

    const firstNode = new PlatformNode(firstPlatform)
    const secondNode = PlatformNode.createFromObject(firstNode)

    expect(secondNode).not.toBe(firstNode)
    expect(secondNode.unpack()).toBe(firstNode.unpack())
    expect(secondNode.getTree()).not.toBe(firstNode.getTree())
  })
})
