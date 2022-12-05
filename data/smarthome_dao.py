import os
import pandas as pd
from typing import Optional
from domain.entities.smarthome import SmartHome
from data.smarthome_device_dao import SmartHomeDeviceDAO


class SmartHomeDAO:
    """A SmartHome class"""

    current_working_directory = os.path.dirname(__file__)

    @staticmethod
    def get_all_smarthome() -> []:
        all_smarthome = []
        try:
            data = pd.read_csv(f'{SmartHomeDAO.current_working_directory}/smarthomes.csv')
            for row_index, row in data.iterrows():
                smarthome = SmartHome(row['homeid'],
                                      row['homename'])
                all_smarthome.append(smarthome)
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return all_smarthome

    @staticmethod
    def get_smarthome_by_id(smarthome_id) -> Optional[SmartHome]:
        try:
            data = pd.read_csv(f'{SmartHomeDAO.current_working_directory}/smarthomes.csv')
            result_data = data[data['homeid'] == int(smarthome_id)]
            if not result_data.empty:
                first_row = result_data.iloc[0]
                smart_home = SmartHome(int(first_row['homeid']),
                                       first_row['homename'])
                return smart_home
            else:
                return None
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
            return None

    @staticmethod
    def get_devices_from_smarthome_by_id(smarthome_id) -> []:
        smart_home_devices = []
        try:
            data = pd.read_csv(f'{SmartHomeDAO.current_working_directory}/smarthomes.csv')
            result_data = data[data['homeid'] == int(smarthome_id)]
            if not result_data.empty:
                first_row = result_data.iloc[0]
                if "-" in str(first_row['devices']):
                    devices = first_row['devices'].split("-")
                    for device_id in devices:
                        result_smart_home_device = SmartHomeDeviceDAO.get_smarthome_device_by_id(device_id)
                        smart_home_devices.append(result_smart_home_device)
                else:
                    device_id = first_row['devices']
                    if pd.isna(device_id):
                        return []
                    result_smart_home_device = SmartHomeDeviceDAO.get_smarthome_device_by_id(device_id)
                    smart_home_devices.append(result_smart_home_device)
        except FileNotFoundError:
            print(f"Data file not found! Error: {FileNotFoundError}.")
        finally:
            return smart_home_devices

    @staticmethod
    def remove_device_from_smarthome_by_id(smarthome_id, device_id) -> bool:
        result = False
        try:
            data = pd.read_csv(f'{SmartHomeDAO.current_working_directory}/smarthomes.csv')
            result_data = data[data['homeid'] == int(smarthome_id)]
            if not result_data.empty:
                first_row = result_data.iloc[0]
                devices = first_row['devices'].split("-")
                devices.remove(str(device_id))
                if not len(devices) is 1:
                    devices_str = '-'.join(map(str, devices))
                else:
                    devices_str = str(devices[0])
                smarthome_index = int(smarthome_id) - 1
                data.loc[smarthome_index, 'devices'] = devices_str
                data.to_csv(f'{SmartHomeDAO.current_working_directory}/smarthomes.csv', index=False)
                result = True
        except FileNotFoundError:
            print(f"Data file not found!")
        except ValueError:
            print(f"device by id: {str(device_id)} not found in in the smart home by id: {str(smarthome_id)}!")
        finally:
            return result
