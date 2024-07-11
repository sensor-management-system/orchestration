-- SPDX-FileCopyrightText: 2020
-- - Martin Abbrent <martin.abbrent@ufz.de>
-- - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
--
-- SPDX-License-Identifier: EUPL-1.2

INSERT INTO public.contact (given_name, family_name, website, email)
VALUES ('Max', 'Mustermann', null, 'max@example.com');
INSERT INTO public."user" (subject, contact_id)
VALUES ('abbrent', 1);
INSERT INTO public.device (created_at, updated_at, description, short_name, long_name, serial_number,
                           manufacturer_uri, manufacturer_name, dual_use, model, inventory_number,
                           persistent_identifier, website, device_type_uri, device_type_name, status_uri, status_name,
                           created_by_id, updated_by_id)
VALUES (null, null, 'sdfasdf', 'fasdfas', 'sadfasdfad', 'sadfasdf', 'sadfasdfas', 'sadfasdf', null, null, null,
        null,
        null, null, null, null, null, 1, 1);
INSERT INTO public.device_contacts (device_id, contact_id)
VALUES (1, 1);
INSERT INTO public.device_property (measuring_range_min, measuring_range_max, failure_value, accuracy, label,
                                    unit_uri, unit_name, compartment_uri, compartment_name, property_uri, property_name,
                                    sampling_media_uri, sampling_media_name, device_id)
VALUES (1, 2, 1, null, 'asdfasdfas', 'asdsafd', 'asdfsadf', 'sadfasdf', 'sfafdas', 'asdfasd', 'sdfafasd',
        'fasdfas',
        'sadfasdfa', 1);

INSERT INTO public.configuration (created_at, updated_at, start_date, end_date, location_type, longitude, latitude,
                                  elevation, project_uri, project_name, longitude_src_device_property_id,
                                  latitude_src_device_property_id, elevation_src_device_property_id, created_by_id,
                                  updated_by_id)
VALUES ('2020-09-08 15:26:22.000000', '2020-09-08 15:26:25.000000', '2020-01-01 00:00:00.000000',
        '2021-01-01 00:00:00.000000', 'static', 56.1, 12.3, 42.23, null, null, 1, 1, 1, 1, 1);

INSERT INTO public.configuration_contacts
values (1, 1);

INSERT INTO public.platform (created_at, updated_at, description, short_name, long_name, manufacturer_uri,
                             manufacturer_name, model, platform_type_uri, platform_type_name, status_uri, status_name,
                             website, inventory_number, serial_number, persistent_identifier, created_by_id,
                             updated_by_id)
VALUES (null, null, 'sadfasdfas', 'asdfasd', 'afdas', 'asdfasd', 'asfdasf', 'asfasdf', 'afssdfa', 'asfdasdf',
        'asfdsafdas', 'afdasfas', 'asfdasf', 'asfdsafas', 'afdasdf', 'fasdfs', 1, 1);

INSERT INTO public.platform (created_at, updated_at, description, short_name, long_name, manufacturer_uri,
                             manufacturer_name, model, platform_type_uri, platform_type_name, status_uri, status_name,
                             website, inventory_number, serial_number, persistent_identifier, created_by_id,
                             updated_by_id)
VALUES (null, null, 'ewrtewr', 'wertwre', 'ewrtew', 'ewrtwe', 'ewrtwer', 'wert', 'afssdfa', 'asfdasdf', 'asfdsafdas',
        'afdasfas', 'asfdasf', 'asfdsafas', 'afdasdf', 'wertwertewr', 1, 1);


INSERT INTO public.configuration_device (created_at, updated_at, offset_x, offset_y, offset_z, calibration_date,
                                         configuration_id, device_id, parent_platform_id,
                                         created_by_id, updated_by_id)
VALUES (null, null, 1, 2, 3, '2020-09-09 13:14:28.000000', 1, 1, 1, 1, 1);
INSERT INTO public.configuration_platform (created_at, updated_at, offset_x, offset_y, offset_z, configuration_id,
                                           parent_platform_id, platform_id, created_by_id, updated_by_id)
VALUES (null, null, 3, 4, 5, 1, null, 1, 1, 1);

INSERT INTO public.configuration_platform (created_at, updated_at, offset_x, offset_y, offset_z, configuration_id,
                                           parent_platform_id, platform_id, created_by_id, updated_by_id)
VALUES (null, null, 6, 6, 6, 1, 1, 2, 1, 1);

commit;