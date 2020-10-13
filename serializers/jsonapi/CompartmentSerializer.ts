import Compartment from '@/models/Compartment'

import { IJsonApiObjectList, IJsonApiDataWithId } from '@/serializers/jsonapi/JsonApiTypes'

import { removeBaseUrl } from '@/utils/urlHelpers'

export class CompartmentSerializer {
  private cvBaseUrl: string | undefined

  constructor (cvBaseUrl: string | undefined) {
    this.cvBaseUrl = cvBaseUrl
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): Compartment[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId): Compartment {
    const id = jsonApiData.id
    const name = jsonApiData.attributes.name
    const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

    return Compartment.createWithData(id, name, url)
  }
}
