-- SPDX-FileCopyrightText: 2020
-- - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
-- - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
--
-- SPDX-License-Identifier: EUPL-1.2


INSERT INTO public.device (description, short_name, long_name, serial_number, manufacturer_uri, manufacturer_name,
                           dual_use, model, inventory_number, persistent_identifier, website, device_type_uri,
                           device_type_name, status_uri, status_name, created_by_id, updated_by_id)
VALUES (null, 'device1', null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
INSERT INTO public.device (description, short_name, long_name, serial_number, manufacturer_uri, manufacturer_name,
                           dual_use, model, inventory_number, persistent_identifier, website, device_type_uri,
                           device_type_name, status_uri, status_name, created_by_id, updated_by_id)
VALUES (null, 'device2', null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
INSERT INTO public.device (description, short_name, long_name, serial_number, manufacturer_uri, manufacturer_name,
                           dual_use, model, inventory_number, persistent_identifier, website, device_type_uri,
                           device_type_name, status_uri, status_name, created_by_id, updated_by_id)
VALUES (null, 'device3', null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);

INSERT INTO platform(created_at, updated_at, long_name, short_name, platform_type_name, model)
VALUES (now(), now(), 'Cosmic-Ray-Station Seelhausener See', 'Cosmic Ray Sensor 2', 'Station', 'HYDROINNOVA_FTP');
INSERT INTO platform(created_at, updated_at, long_name, short_name, platform_type_name, model)
VALUES (now(), now(), 'Mikroklimamessstation Global Change Experimental Facility (GCEF)', 'THL_0351', 'Station',
        'SENSYS');
INSERT INTO platform(created_at, updated_at, long_name, short_name, platform_type_name, model)
VALUES (now(), now(), 'Mikroklimamessstation Global Change Experimental Facility (GCEF)', 'THL_0352', 'Station',
        'SENSYS');
INSERT INTO platform(created_at, updated_at, long_name, short_name, platform_type_name, model)
VALUES (now(), now(), 'Mikroklimamessstation Global Change Experimental Facility (GCEF)', 'ROUTER_0210', 'Station',
        'SENSYS');
INSERT INTO public.contact (id, given_name, family_name, website, email)
VALUES (1, 'Max', 'Mustermann', '', 'max@test.test');

INSERT INTO public."user" (id, subject, contact_id)
VALUES (1, 'testUser2', 1);
INSERT INTO public.device_property (id, measuring_range_min, measuring_range_max, failure_value, accuracy, label,
                                    unit_uri, unit_name, compartment_uri, compartment_name, property_uri, property_name,
                                    sampling_media_uri, sampling_media_name, device_id)
VALUES (1, 0, 1, 9999, null, null, null, null, null, null, null, null, null, null, 1);
INSERT INTO public.configuration (start_date, end_date, location_type, longitude, latitude, elevation, project_uri,
                                  project_name, label, status, longitude_src_device_property_id,
                                  latitude_src_device_property_id, elevation_src_device_property_id, created_by_id,
                                  updated_by_id)
VALUES (null, null, 'dynamic', null, null, null, null, null, 'ConfigTest4', 'draft', null, 1, 1, null, 1);

INSERT INTO public.configuration (start_date, end_date, location_type, longitude, latitude, elevation, project_uri,
                                  project_name, label, status, longitude_src_device_property_id,
                                  latitude_src_device_property_id, elevation_src_device_property_id, created_by_id,
                                  updated_by_id)
VALUES (null, null, 'dynamic', 1, 1, 1, null, null, 'ConfigTest1', 'draft', null, null, null, 1, 1);

INSERT INTO public.configuration (start_date, end_date, location_type, longitude, latitude, elevation, project_uri,
                                  project_name, label, status, longitude_src_device_property_id,
                                  latitude_src_device_property_id, elevation_src_device_property_id, created_by_id,
                                  updated_by_id)
VALUES (null, null, 'static', null, null, null, null, null, 'ConfigTest2', 'draft', 1, 1, 1, 1, 1);

INSERT INTO public.configuration (start_date, end_date, location_type, longitude, latitude, elevation, project_uri,
                                  project_name, label, status, longitude_src_device_property_id,
                                  latitude_src_device_property_id, elevation_src_device_property_id, created_by_id,
                                  updated_by_id)
VALUES (null, null, 'dynamic', null, null, null, null, null, 'ConfigTest3', 'draft', null, null, 1, 1, null);


INSERT INTO public.configuration_platform (offset_x, offset_y, offset_z, configuration_id, platform_id,
                                           parent_platform_id, created_by_id, updated_by_id)
VALUES (1, null, null, 1, 1, null, null, null);

INSERT INTO public.configuration_platform (offset_x, offset_y, offset_z, configuration_id, platform_id,
                                           parent_platform_id, created_by_id, updated_by_id)
VALUES (1, null, null, 2, 1, null, null, null);

INSERT INTO public.configuration_device (offset_x, offset_y, offset_z, calibration_date, configuration_id, device_id,
                                         parent_platform_id, created_by_id, updated_by_id)
VALUES (0.5, null, null, null, 1, 1, 1, null, null);

INSERT INTO public.configuration_device (offset_x, offset_y, offset_z, calibration_date, configuration_id, device_id,
                                         parent_platform_id, created_by_id, updated_by_id)
VALUES (0.5, null, null, null, 2, 1, 1, null, null);

commit;