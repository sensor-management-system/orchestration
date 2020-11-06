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

import { Project } from '@/models/Project'

describe('Project', () => {
  describe('#id', () => {
    it('should be an empty string for a new object', () => {
      const emptyProject = new Project()
      expect(emptyProject.id).toEqual('')
    })
    it('should be possible to set it', () => {
      const project = new Project()
      project.id = 'newid'
      expect(project.id).toEqual('newid')
    })
  })
  describe('#name', () => {
    it('should be an empty string for a new object', () => {
      const emptyProject = new Project()
      expect(emptyProject.name).toEqual('')
    })
    it('should be possible to set it', () => {
      const project = new Project()
      project.name = 'new name'
      expect(project.name).toEqual('new name')
    })
  })
  describe('#uri', () => {
    it('should be an empty string for a new object', () => {
      const emptyProject = new Project()
      expect(emptyProject.uri).toEqual('')
    })
    it('should be possible t oset it', () => {
      const project = new Project()
      project.uri = 'newuri'
      expect(project.uri).toEqual('newuri')
    })
  })
  describe('#toString', () => {
    it('should be equal to the name', () => {
      const namesToSet = ['abc', 'cde']
      for (const name of namesToSet) {
        const project = new Project()
        project.name = name
        expect(project.toString()).toEqual(name)
      }
    })
  })
  describe('#createWithData', () => {
    it('should be possible to create the object right away with some data', () => {
      const project = Project.createWithData(
        'someId',
        'some name',
        'someuri'
      )
      expect(project.id).toEqual('someId')
      expect(project.name).toEqual('some name')
      expect(project.uri).toEqual('someuri')
    })
  })
  describe('#createFromObject', () => {
    it('should be possible to create from an object', () => {
      const project = Project.createFromObject({
        id: 'someId',
        name: 'some name',
        uri: 'someuri'
      })
      expect(project.id).toEqual('someId')
      expect(project.name).toEqual('some name')
      expect(project.uri).toEqual('someuri')
    })
  })
})
