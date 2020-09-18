import Platform from '@/models/Platform'
import { PlatformNode } from '@/models/PlatformNode'

describe('PlatformNode', () => {
  it('should create a PlatformNode object', () => {
    const platform = new Platform()
    platform.id = '1'

    const node = new PlatformNode(platform)
    expect(Object.is(node.unpack(), platform)).toBeTruthy()
    expect(node).toHaveProperty('id', '1')
  })

  it('should create a PlatformNode from another one', () => {
    const firstPlatform = new Platform()
    firstPlatform.id = '1'

    const firstNode = new PlatformNode(firstPlatform)
    const secondNode = PlatformNode.createFromObject(firstNode)

    expect(Object.is(secondNode, firstNode)).toBeFalsy()
    expect(Object.is(secondNode.unpack(), firstNode.unpack())).toBeTruthy()
    expect(Object.is(secondNode.getTree(), firstNode.getTree())).toBeFalsy()
  })

  it('should be allowed to have children', () => {
    const platform = new Platform()

    const node = new PlatformNode(platform)
    expect(node.canHaveChildren()).toBeTruthy()
  })

  it('should return an Array for children', () => {
    const firstPlatform = new Platform()
    const firstNode = new PlatformNode(firstPlatform)

    const secondPlatform = new Platform()
    const secondNode = new PlatformNode(secondPlatform)

    firstNode.getTree().push(secondNode)

    expect(firstNode.children).toBeInstanceOf(Array)
    expect(firstNode.children).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })

  it('should set the tree from an array of children', () => {
    const firstPlatform = new Platform()
    const firstNode = new PlatformNode(firstPlatform)

    const secondPlatform = new Platform()
    const secondNode = new PlatformNode(secondPlatform)

    firstNode.children = [secondNode]
    expect(firstNode.getTree()).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })
})
