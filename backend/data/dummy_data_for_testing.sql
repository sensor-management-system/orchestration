-- SPDX-FileCopyrightText: 2021
-- - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
-- - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
--
-- SPDX-License-Identifier: HEESIL-1.0

insert into public.contact (id, given_name, family_name, website, email)
values  (1, 'Test', 'User1', null, 'test-user1@ufz.de'),
        (2, 'Test', 'User2', null, 'test-user2@ufz.de'),
        (3, 'Test', 'User3', null, 'test-user3@ufz.de');

insert into public.user (id, subject, contact_id)
values  (1, 'testuser1@ufz.de', 1),
        (2, 'testuser2@ufz.de', 2),
        (3, 'testuser3@ufz.de', 3);





insert into public.device (created_at, updated_at, id, description, short_name, long_name, serial_number, manufacturer_uri, manufacturer_name, dual_use, model, inventory_number, persistent_identifier, website, device_type_uri, device_type_name, status_uri, status_name, created_by_id, updated_by_id)
values  ('2021-07-21 10:20:52.362541', null, 1, 'Digital Temperature Sensor KY-028 for Arduino, it measures temperature changes based on the thermistor resistance. This module has both digital and analog outputs, there''s a potentiometer to adjusts the detection threshold on the digital interface.', 'KY-028', 'KY-028 DIGITAL TEMPERATURE SENSOR MODULE', '', '', '', false, '', '', null, 'https://arduinomodules.info/ky-028-digital-temperature-sensor-module/', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmenttypes/1/', 'Sensor', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmentstatus/3/', 'Under Construction', 1, null),
        ('2021-07-21 10:58:29.259763', null, 2, 'Arduino KY-032 obstacle avoidance sensor is a distance-adjustable, infrared proximity sensor designed for wheeled robots. Also known as AD-032.

The sensor detection distance ranges from 2cm to 40cm, it can be adjusted by turning the potentiometer knob. The operating voltage is 3.3V-5V so it is suitable for a variety of microcontrollers like Arduino, ESP32, Teensy, ESP8266, Raspberry Pi, and others.

It has strong adaptability to ambient light and it is fairly accurate to sense changes in the surrounding environment.', 'KY-032', 'KY-032 INFRARED OBSTACLE AVOIDANCE SENSOR MODULE', '', '', '', false, '', '', null, 'https://arduinomodules.info/ky-032-infrared-obstacle-avoidance-sensor-module/', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmenttypes/1/', 'Sensor', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmentstatus/2/', 'In Use', 1, null),
        ('2021-07-28 07:49:28.541363', null, 5, '', 'SMT100', 'Soil Temperature and Humidity Sensor ', '123456789', '', '', false, 'SMT100', '', null, '', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmenttypes/1/', 'Sensor', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/equipmentstatus/2/', 'In Use', 3, null);


insert into public.custom_field (id, key, value, device_id)
values  (1, 'Board Dimensions', '	15mm x 36mm [0.6in x 1.4in]', 1),
        (2, ' Operating Voltage', '	3.3V to 5.5V', 1),
        (3, 'Detection distance ', '	2cm – 40cm', 2),
        (4, ' Working voltage', '3.3V – 5V DC', 2),
        (5, '', '', 5);

insert into public.device_attachment (id, label, url, device_id)
values  (1, 'Fritzing Part: KY-028 Digital Temperature Sensor Module.', 'https://arduinomodules.info/download/ky-028-digital-temperature-sensor-module-zip-file/', 1),
        (2, 'Fritzing Part: KY-032 IR Obstacle Avoidance Sensor Module.', 'https://arduinomodules.info/download/ky-032-infrared-obstacle-avoidance-sensor-module-zip-file/', 2),
        (4, 'UFZ kjasghfas', 'https://ufz.de', 5);


insert into public.device_calibration_action (created_at, updated_at, id, description, current_calibration_date, next_calibration_date, formula, value, device_id, contact_id, created_by_id, updated_by_id)
values  ('2021-07-21 10:50:41.844987', null, 1, '', '2021-07-20 12:49:00.000000', '2021-08-31 12:49:00.000000', '', null, 1, 1, 1, null),
        ('2021-07-28 07:56:47.800814', null, 2, '', '2021-06-01 09:55:00.000000', null, '', 1, 5, 3, 3, null);

insert into public.device_contacts (device_id, contact_id)
values  (1, 1),
        (2, 1),
        (5, 3);



insert into public.device_property (id, measuring_range_min, measuring_range_max, failure_value, accuracy, label, unit_uri, unit_name, compartment_uri, compartment_name, property_uri, property_name, sampling_media_uri, sampling_media_name, device_id, resolution, resolution_unit_name, resolution_unit_uri)
values  (2, null, null, null, null, '', '', '', '', '', '', '', '', '', 2, null, '', ''),
        (1, -55, 125, 999, 0.5, 'Temperature', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/units/51/', '°C', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/compartments/5/', 'Technical Parameters', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/measuredquantities/146/', 'Temperature Device', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/samplingmedia/1/', 'Devices', 1, null, '', ''),
        (4, null, null, null, null, '', '', '', '', '', '', '', '', '', 1, null, '', ''),
        (6, -50, 50, null, null, 'Soil Temperature', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/units/51/', '°C', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/compartments/4/', 'Pedosphere', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/measuredquantities/133/', 'Soil Temperature', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/samplingmedia/6/', 'Soil', 5, null, '', ''),
        (8, 1, 100, null, null, 'Soil Permittivity', '', '', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/compartments/4/', 'Pedosphere', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/measuredquantities/127/', 'Relative Permittivity', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/samplingmedia/6/', 'Soil', 5, null, '', '');

insert into public.device_property_calibration (id, calibration_action_id, device_property_id, created_at, created_by_id, updated_at, updated_by_id)
values  (1, 1, 1, '2021-07-21 10:50:42.115466', 1, null, null),
        (2, 2, 6, '2021-07-28 07:56:48.058998', 3, null, null);


insert into public.device_software_update_action (created_at, updated_at, id, device_id, software_type_name, software_type_uri, update_date, version, repository_url, description, contact_id, created_by_id, updated_by_id)
values  ('2021-07-22 07:22:37.199997', null, 1, 1, 'OS', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/softwaretypes/3/', '2021-07-19 09:19:00.000000', '1.0', '', '', 1, 1, null);


insert into public.generic_device_action (created_at, updated_at, id, device_id, description, action_type_name, action_type_uri, begin_date, end_date, contact_id, created_by_id, updated_by_id)
values  ('2021-07-21 10:51:18.237723', null, 1, 1, '', 'Device Maintenance', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/5/', '2021-07-04 12:50:00.000000', '2021-07-21 12:51:00.000000', 1, 1, null),
        ('2021-07-21 10:52:30.081704', null, 2, 1, '', 'Device Observation', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/6/', '2021-07-21 12:52:00.000000', '2021-07-22 12:52:00.000000', 1, 1, null);



insert into public.platform (created_at, updated_at, id, description, short_name, long_name, manufacturer_uri, manufacturer_name, model, platform_type_uri, platform_type_name, status_uri, status_name, website, inventory_number, serial_number, persistent_identifier, created_by_id, updated_by_id)
values  ('2021-07-21 11:10:17.106484', '2021-07-21 11:10:47.447243', 1, 'Features:

- ATmega328 microcontroller
- Input voltage - 7-12V
- 14 Digital I/O Pins (6 PWM outputs)
- 6 Analog Inputs
- 32k Flash Memory
- 16Mhz Clock Speed', 'Uno R3', 'Arduino Uno R3', '', '', '', '', '', '', '', '', '', '', null, 1, 1);


insert into public.platform_attachment (id, label, url, platform_id)
values  (1, 'Schematic', 'https://www.arduino.cc/en/uploads/Main/Arduino_Uno_Rev3-schematic.pdf', 1),
        (2, 'Datasheet', 'http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf', 1);


insert into public.platform_contacts (platform_id, contact_id)
values  (1, 1);


insert into public.generic_platform_action (created_at, updated_at, id, platform_id, description, action_type_name, action_type_uri, begin_date, end_date, contact_id, created_by_id, updated_by_id)
values  ('2021-07-22 07:24:26.825787', null, 1, 1, '', 'Platform Application', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/4/', '2021-07-18 09:24:00.000000', '2021-07-22 09:24:00.000000', 1, 1, null),
        ('2021-07-22 07:24:43.744716', null, 2, 1, '', 'Platform Maintenance', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/2/', '2021-07-21 09:24:00.000000', '2021-07-22 09:24:00.000000', 1, 1, null),
        ('2021-07-22 07:25:10.008132', null, 3, 1, '', 'Platform Observation', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/3/', '2021-07-19 09:24:00.000000', '2021-07-20 09:24:00.000000', 1, 1, null),
        ('2021-07-22 07:25:38.569610', null, 4, 1, '', 'Platform Visit', 'https://rdm-test.intranet.ufz.de/sms-cv/api/v1/actiontypes/1/', '2021-07-06 09:25:00.000000', '2021-07-06 09:25:00.000000', 1, 1, null);





insert into public.configuration (created_at, updated_at, id, start_date, end_date, location_type, longitude, latitude, elevation, project_uri, project_name, longitude_src_device_property_id, latitude_src_device_property_id, elevation_src_device_property_id, created_by_id, updated_by_id, label, status)
values  ('2021-07-21 11:13:06.280412', '2021-07-23 13:00:21.415848', 1, '2021-07-22 01:12:00.000000', '2021-07-23 01:12:00.000000', 'Stationary', 12.388215, 51.337825, null, '', '', null, null, null, 1, 1, 'Test room 217', 'draft');

insert into public.configuration_contacts (configuration_id, contact_id)
values  (1, 1);


insert into public.device_mount_action (created_at, updated_at, id, configuration_id, device_id, parent_platform_id, begin_date, description, contact_id, offset_x, offset_y, offset_z, created_by_id, updated_by_id)
values  ('2021-07-21 11:15:42.561930', '2021-07-23 13:00:21.911842', 1, 1, 1, null, '2021-07-21 23:14:09.534000', '', 1, 4, 4, 4, 1, 1),
        ('2021-07-21 11:15:43.118320', '2021-07-23 13:00:22.053452', 2, 1, 2, null, '2021-07-21 23:14:09.534000', '', 1, 0, 0, 0, 1, 1);

insert into public.platform_mount_action (created_at, updated_at, id, configuration_id, platform_id, parent_platform_id, begin_date, description, contact_id, offset_x, offset_y, offset_z, created_by_id, updated_by_id)
values  ('2021-07-21 11:15:42.150340', '2021-07-23 13:00:21.685402', 1, 1, 1, null, '2021-07-23 16:59:06.165000', '', 1, 3, 0, 3, 1, 1);

