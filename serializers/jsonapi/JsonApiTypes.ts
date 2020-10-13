export type IJsonApiAttributes = {[idx: string]: any }

export interface IJsonApiLinks {
    self: string
}

export type IJsonApiNestedElement = {[idx: string]: any}

export interface IJsonApiTypeId {
    type: string
    id: string
}

export interface IJsonApiTypeIdDataList {
    data: IJsonApiTypeId[]
}

export type IJsonApiTypeIdDataListDict = {[idx: string]: IJsonApiTypeIdDataList}

export interface IJsonApiData {
    attributes: IJsonApiAttributes
    type: string
    relationships: IJsonApiTypeIdDataListDict
}

export interface IJsonApiDataWithOptionalId extends IJsonApiData {
    id?: string
}

export interface IJsonApiDataWithId extends IJsonApiData {
    id: string
    links: IJsonApiLinks
}

export interface IJsonApiTypeIdAttributes extends IJsonApiTypeId {
    attributes: IJsonApiAttributes
}

export interface IJsonApiObject {
    data: IJsonApiDataWithId
    included: IJsonApiTypeIdAttributes[]
}

export interface IJsonApiObjectList {
    data: IJsonApiDataWithId[],
    included: IJsonApiTypeIdAttributes[]
}
