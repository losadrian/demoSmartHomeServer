import os
import pandas as pd
from typing import Optional
from domain.entities.smarthome_device import SmartHomeDevice


class SmartHomeDeviceDAO:
    """A SmartHome class"""

    current_working_directory = os.path.dirname(__file__)

    @staticmethod
    def get_all_smarthome_device() -> []:
        all_smarthome_device = []
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            for row_index, row in data.iterrows():
                smarthome_device = SmartHomeDevice(row['deviceid'],
                                                   row['productname'],
                                                   row['manufacturer'],
                                                   row['communication'])
                all_smarthome_device.append(smarthome_device)
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return all_smarthome_device

    @staticmethod
    def get_smarthome_devices_by_query(communication, manufacturer, product_name) -> []:
        filtered_smarthome_devices = []
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            result_data = data
            if communication is not None:
                result_data = result_data[result_data['communication'] == communication]
            if manufacturer is not None:
                result_data = result_data[result_data['manufacturer'] == manufacturer]
            if product_name is not None:
                result_data = result_data[result_data['product_name'] == product_name]
            data = result_data
            for row_index, row in data.iterrows():
                smarthome_device = SmartHomeDevice(row['deviceid'],
                                                   row['productname'],
                                                   row['manufacturer'],
                                                   row['communication'])
                filtered_smarthome_devices.append(smarthome_device)
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return filtered_smarthome_devices

    @staticmethod
    def get_smarthome_device_by_id(device_id) -> Optional[SmartHomeDevice]:
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            result_data = data[data['deviceid'] == int(device_id)]
            if not result_data.empty:
                first_row = result_data.iloc[0]
                smart_home_device = SmartHomeDevice(int(first_row['deviceid']),
                                                    first_row['productname'],
                                                    first_row['manufacturer'],
                                                    first_row['communication'])
                return smart_home_device
            else:
                return None
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
            return None

    @staticmethod
    def is_smarthome_device_exists(new_product_name, new_manufacturer, new_communication) -> bool:
        result = False
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            result_data = data.query(f'communication == "{new_communication}"'
                                     f' and manufacturer == "{new_manufacturer}"'
                                     f' and productname == "{new_product_name}"')
            if not result_data.empty:
                result = True
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return result

    @staticmethod
    def set_smarthome_device(new_product_name, new_manufacturer, new_communication) -> bool:
        result = False
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            data.sort_values(by=['deviceid'], inplace=True, ascending=False)
            new_id = 1
            if not data.empty:
                last_id = data['deviceid'].values[:1]
                new_id = last_id + 1

            new_data_row = pd.DataFrame({
                'communication': [new_communication],
                'deviceid': [int(new_id)],
                'productname': [new_product_name],
                'manufacturer': [new_manufacturer]
            })
            data = pd.concat([data, new_data_row])
            data.to_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv', index=False)
            result = True
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return result

    @staticmethod
    def remove_device_by_id(device_id) -> bool:
        result = False
        try:
            data = pd.read_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv')
            result_to_delete = (data["deviceid"] == int(device_id))
            data_index_to_delete = data.index[result_to_delete]
            if not data_index_to_delete.empty:
                modified_data = data.drop(data_index_to_delete, axis=0, inplace=False)
                modified_data.to_csv(f'{SmartHomeDeviceDAO.current_working_directory}/smarthomedevices.csv', index=False)
                result = True
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return result
