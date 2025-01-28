/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { IStaEntity, StaApiEntity, StaEntity } from '@/models/sta/StaEntity'

export interface StaApiDatastream extends StaApiEntity {

}

export interface IStaDatastream extends IStaEntity {

}

export class StaDatastream extends StaEntity implements IStaDatastream {

}
