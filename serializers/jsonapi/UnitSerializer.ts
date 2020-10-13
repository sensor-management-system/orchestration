import Unit from '@/models/Unit'

import { IJsonApiObjectList, IJsonApiDataWithId } from '@/serializers/jsonapi/JsonApiTypes'

import { removeBaseUrl } from '@/utils/urlHelpers'

export class UnitSerializer {
  private cvBaseUrl: string | undefined

  constructor (cvBaseUrl: string | undefined) {
    this.cvBaseUrl = cvBaseUrl
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): Unit[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId): Unit {
    const id = jsonApiData.id
    let name = jsonApiData.attributes.unitsname
    if (jsonApiData.attributes.unitsabbreviation) {
      name += ' [' + jsonApiData.attributes.unitsabbreviation + ']'
    }
    const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

    return Unit.createWithData(id, name, url)
  }
}
