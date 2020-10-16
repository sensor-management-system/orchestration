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
import Platform from '@/models/Platform'
import { PlatformNode } from '@/models/PlatformNode'

describe('PlatformNode', () => {
  it('should create a PlatformNode object', () => {
    const platform = new Platform()
    platform.id = '1'

    const node = new PlatformNode(platform)
    expect(Object.is(node.unpack(), platform)).toBeTruthy()
    expect(node).toHaveProperty('id', PlatformNode.ID_PREFIX + platform.id)
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
