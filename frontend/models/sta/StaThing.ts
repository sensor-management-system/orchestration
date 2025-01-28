/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { IStaEntity, StaApiEntity, StaEntity } from '@/models/sta/StaEntity'

export interface StaApiThing extends StaApiEntity {

}

export interface IStaThing extends IStaEntity {

}

export class StaThing extends StaEntity implements IStaThing {

}
