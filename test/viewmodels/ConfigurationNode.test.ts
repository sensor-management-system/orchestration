/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
import { Configuration } from '@/models/Configuration'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'

describe('ConfigurationNode', () => {
  it('should create a ConfigurationNode object', () => {
    const config = new Configuration()
    config.id = '1'

    const node = new ConfigurationNode(config)
    expect(Object.is(node.unpack(), config)).toBeTruthy()
    expect(node).toHaveProperty('id', ConfigurationNode.ID_PREFIX + config.id)
  })
  it('should create a ConfigurationNode from another one', () => {
    const config = new Configuration()
    config.id = '1'

    const firstNode = new ConfigurationNode(config)
    const secondNode = ConfigurationNode.createFromObject(firstNode)

    expect(Object.is(secondNode, firstNode)).toBeFalsy()
    expect(Object.is(secondNode.unpack(), firstNode.unpack())).toBeTruthy()
    expect(Object.is(secondNode.getTree(), firstNode.getTree())).toBeFalsy()
  })
  it('should be allowed to have children', () => {
    const config = new Configuration()
    config.id = '1'

    const node = new ConfigurationNode(config)
    expect(node.canHaveChildren()).toBeTruthy()
  })
  it('should return an Array for children', () => {
    const firstConfig = new Configuration()
    firstConfig.id = '1'
    const firstNode = new ConfigurationNode(firstConfig)

    const secondConfig = new Configuration()
    const secondNode = new ConfigurationNode(secondConfig)

    firstNode.getTree().push(secondNode)

    expect(firstNode.children).toBeInstanceOf(Array)
    expect(firstNode.children).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })
  it('should set the tree from an array of children', () => {
    const firstConfig = new Configuration()
    firstConfig.id = '1'
    const firstNode = new ConfigurationNode(firstConfig)

    const secondConfig = new Configuration()
    const secondNode = new ConfigurationNode(secondConfig)

    firstNode.children = [secondNode]
    expect(firstNode.getTree()).toHaveLength(1)
    expect(Object.is(firstNode.children[0], secondNode)).toBeTruthy()
  })

  it('should return a name', () => {
    const config = new Configuration()
    config.id = '1'
    config.label = 'ABC'

    const node = new ConfigurationNode(config)
    const name = node.name
    const expectedName = 'ABC'

    expect(name).toEqual(expectedName)
  })
})
