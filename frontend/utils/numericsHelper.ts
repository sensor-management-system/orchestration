/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export const parseFloatOrDefault = (value: any, defaultValue: number): number => isNaN(parseFloat(value)) ? defaultValue : parseFloat(value)
export const parseFloatOrNull = (value: any): number | null => isNaN(parseFloat(value)) ? null : parseFloat(value)
export const parseIntOrDefault = (value: any, defaultValue: number): number => isNaN(parseInt(value)) ? defaultValue : parseInt(value)
export const parseIntOrNull = (value: any): number | null => isNaN(parseInt(value)) ? null : parseInt(value)
export const round = (value: number, ndigits: number = 0) => Math.round(value * 10 ** ndigits) / 10 ** ndigits
