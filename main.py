import os
from flask import Flask, jsonify, request, abort
from data.smarthome_device_dao import SmartHomeDeviceDAO
from data.smarthome_dao import SmartHomeDAO

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return 'Hello!'


@app.route('/device', methods=['GET'])
def get_devices():
    if request.method == 'GET':
        print("\nGET /device")
        args = request.args
        if len(args) != 0:
            communication = args.get('communication')
            manufacturer = args.get('manufacturer')
            product_name = args.get('product_name')
            print(f"GET smarthome/device get_smart_home_devices args: {communication}, {manufacturer}, {product_name}")
            filtered_smarthome_device = SmartHomeDeviceDAO.get_smarthome_devices_by_query(communication,
                                                                                          manufacturer,
                                                                                          product_name)
            for device_index in range(len(filtered_smarthome_device)):
                filtered_smarthome_device[device_index] = vars(filtered_smarthome_device[device_index])
            output = filtered_smarthome_device
        else:
            all_smarthome_device = SmartHomeDeviceDAO.get_all_smarthome_device()
            for device_index in range(len(all_smarthome_device)):
                all_smarthome_device[device_index] = vars(all_smarthome_device[device_index])
            output = all_smarthome_device
        print(output)
        return jsonify(output)
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/device/<device_id>', methods=['GET'])
def get_device_by_id(device_id):
    if request.method == 'GET':
        try:
            print("\nGET /device/<device_id>")
            print(f"device_id: {int(device_id)}")
            result_smart_home_device = SmartHomeDeviceDAO.get_smarthome_device_by_id(device_id)
            if result_smart_home_device is not None:
                output = vars(result_smart_home_device)
                print(output)
                return jsonify(output)
            else:
                print(f"Message: No device by id: {int(device_id)}")
                return jsonify({"Message": f"No device by id: {int(device_id)}"})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome', methods=['GET'])
def get_smarthomes():
    if request.method == 'GET':
        print("\nGET /smarthome")
        all_smarthome = SmartHomeDAO.get_all_smarthome()
        for smarthome_index in range(len(all_smarthome)):
            all_smarthome[smarthome_index] = vars(all_smarthome[smarthome_index])
        output = clean_nones(all_smarthome)
        print(output)
        return jsonify(output)
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome/<smarthome_id>', methods=['GET'])
def get_smarthome_by_id(smarthome_id):
    if request.method == 'GET':
        try:
            print("\nGET /smarthome/<smarthome_id>")
            print(f"smarthome_id: {int(smarthome_id)}")
            result_smart_home = SmartHomeDAO.get_smarthome_by_id(smarthome_id)
            if result_smart_home is not None:
                output = clean_nones(vars(result_smart_home))
                print(output)
                return jsonify(output)
            else:
                print(f"Message: No smart home by id: {int(smarthome_id)}")
                return jsonify({"Message": f"No smart home by id: {int(smarthome_id)}"})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome/<smarthome_id>/device', methods=['GET'])
def get_devices_by_smart_home_id(smarthome_id):
    if request.method == 'GET':
        try:
            print("\nGET /smarthome/<smarthome_id>/device")
            authorization_token = ""
            try:
                print("\nGet Authorization token from header: "
                      f"\n{request.headers.get('Authorization')}, ")
                authorization_token = request.headers.get('Authorization').split()[1]
            except AttributeError:
                print("\nabort(401)")
                abort(401)

            if not authorization_token or authorization_token.isspace() or authorization_token != f"A1B2C3D4E5":
                print("\nabort(401)")
                abort(401)

            print(f"smarthome_id: {int(smarthome_id)}")
            result_smarthome_devices = SmartHomeDAO.get_devices_from_smarthome_by_id(smarthome_id)
            if len(result_smarthome_devices) != 0:
                for device_index in range(len(result_smarthome_devices)):
                    result_smarthome_devices[device_index] = vars(result_smarthome_devices[device_index])
                output = result_smarthome_devices
                print(output)
                return jsonify(output)
            else:
                print(f"Message: No devices in the smart home by id: {int(smarthome_id)}")
                return jsonify({"Message": f"No devices in the smart home by id: {int(smarthome_id)}"})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome/<smarthome_id>/device/<device_id>', methods=['GET'])
def get_device_by_smart_home_id_and_device_id(smarthome_id, device_id):
    if request.method == 'GET':
        try:
            print("\nGET /smarthome/<smarthome_id>/device/<device_id>")
            print(f"smarthome_id: {int(smarthome_id)} , device_id: {int(device_id)}")
            smart_home = SmartHomeDAO.get_smarthome_by_id(smarthome_id)
            if smart_home is None:
                print(f"Message: No smart home by id: {int(smarthome_id)}")
                return jsonify({"Message": f"No smart home by id: {int(smarthome_id)}"})
            smarthome_devices = SmartHomeDAO.get_devices_from_smarthome_by_id(smart_home.home_id)
            if smarthome_devices is not None:
                result_smart_home_device = None
                for device in smarthome_devices:
                    if int(device.device_id) is int(device_id):
                        result_smart_home_device = device
                        break
                if result_smart_home_device is None:
                    print(f"Message: No device by id: {int(device_id)}")
                    return jsonify({"Message": f"No device by id: {int(device_id)}"})
                output = vars(result_smart_home_device)
                print(output)
                return jsonify(output)
            else:
                print(f"Message: No devices in the smart home by id: {int(smarthome_id)}")
                return jsonify({"Message": f"No devices in the smart home by id: {int(smarthome_id)}"})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/device', methods=['POST'])
def add_smart_home_device():
    if request.method == 'POST':
        try:
            print("\nPOST /device by params: "
                  f"\n{request.json['product_name']}, "
                  f"\n{request.json['manufacturer']}, "
                  f"\n{request.json['communication']}, ")
            new_product_name = request.json['product_name']
            new_manufacturer = request.json['manufacturer']
            new_communication = request.json['communication']
        except KeyError:
            print(f"ErrorCode: -2, All fields is required (product name, manufacturer, communication)")
            return jsonify(
                {"ErrorCode": -2,
                 "ErrorMessage": "All fields is required (product name, manufacturer, communication)."})

        if (not new_product_name or not new_manufacturer or not new_communication) \
                or (new_product_name.isspace() or new_manufacturer.isspace() or new_communication.isspace()):
            print(f"ErrorCode: -2, All fields is required (product name, manufacturer, communication)")
            return jsonify(
                {"ErrorCode": -2,
                 "ErrorMessage": "All fields is required (product name, manufacturer, communication)."})

        smart_home_device_exists = SmartHomeDeviceDAO.is_smarthome_device_exists(new_product_name,
                                                                                 new_manufacturer,
                                                                                 new_communication)
        if smart_home_device_exists:
            print(f"ErrorCode: -3, Data already exists")
            return jsonify({"ErrorCode": -3, "ErrorMessage": "Data already exists."})
        else:
            is_set_success = SmartHomeDeviceDAO.set_smarthome_device(new_product_name,
                                                                     new_manufacturer,
                                                                     new_communication)
            print(f"Success: {is_set_success}")
            return jsonify({"Success": is_set_success})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/device/<device_id>', methods=['DELETE'])
def del_device_by_id(device_id):
    if request.method == 'DELETE':
        try:
            print("\nDELETE /device/<device_id>")
            print(f"device_id: {int(device_id)}")
            is_removing_success = SmartHomeDeviceDAO.remove_device_by_id(int(device_id))
            if not is_removing_success:
                print(f"ErrorCode: -4, No device by id: {int(device_id)}")
                return jsonify({"ErrorCode": -4, "ErrorMessage": f"No device by id: {int(device_id)}"})
            else:
                all_smarthome = SmartHomeDAO.get_all_smarthome()
                all_smarthome_id_array = []
                for smarthome in all_smarthome:
                    all_smarthome_id_array.append(smarthome.home_id)
                for smarthome_home_id in all_smarthome_id_array:
                    SmartHomeDAO.remove_device_from_smarthome_by_id(smarthome_home_id, device_id)
                print(f"Success: {True}")
                return jsonify({"Success": True})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome/<smarthome_id>/device/<device_id>', methods=['DELETE'])
def del_device_by_smart_home_id_and_device_id(smarthome_id, device_id):
    if request.method == 'DELETE':
        try:
            print("\nDELETE /smarthome/<smarthome_id>/device/<device_id>")
            print(f"smarthome_id: {int(smarthome_id)} , device_id: {int(device_id)}")
            smart_home = SmartHomeDAO.get_smarthome_by_id(smarthome_id)
            if smart_home is None:
                print(f"Message: No smart home by id: {int(smarthome_id)}")
                return jsonify({"Message": f"No smart home by id: {int(smarthome_id)}"})
            smarthome_devices = SmartHomeDAO.get_devices_from_smarthome_by_id(smart_home.home_id)
            if smarthome_devices is not None:
                result_smart_home_device = None
                for device in smarthome_devices:
                    if int(device.device_id) is int(device_id):
                        result_smart_home_device = device
                        break
                if result_smart_home_device is None:
                    print(f"ErrorCode: -4, No device by id: {int(device_id)}")
                    return jsonify({"ErrorCode": -4, "ErrorMessage": f"No device by id: {int(device_id)}"})
                is_removing_success = SmartHomeDAO.remove_device_from_smarthome_by_id(smarthome_id, device_id)
                print(f"Success: {is_removing_success}")
                return jsonify({"Success": is_removing_success})
            else:
                print(f"ErrorCode: -5, No devices in the smart home by id: {int(smarthome_id)}")
                return jsonify(
                    {"ErrorCode": -5, "ErrorMessage": f"No devices in the smart home by id: {int(smarthome_id)}"})
        except ValueError:
            print(f"ErrorCode: -1, ErrorMessage: ID is not right value type")
            return jsonify({"ErrorCode": -1, "ErrorMessage": "ID is not right value type"})
    print("\nMessage: Nothing to See Here")
    return jsonify({"Message": "Nothing to See Here"})


@app.route('/smarthome/authentication', methods=['POST'])
def auth_to_smart_home():
    if request.method == 'POST':
        try:
            print("\nPOST /device by params: "
                  f"\n{request.json['password']}, ")
            user_password = request.json['password']
        except KeyError:
            print(f"ErrorCode: -6, Password is required to authenticate the user.")
            return jsonify(
                {"ErrorCode": -6,
                 "ErrorMessage": "Password is required to authenticate the user."})

        if not user_password or user_password.isspace():
            print(f"ErrorCode: -6, Password is required to authenticate the user.")
            return jsonify(
                {"ErrorCode": -6,
                 "ErrorMessage": "Password is required to authenticate the user."})

        if user_password != f"welcome":
            print(f"ErrorCode: -7, Invalid password.")
            return jsonify(
                {"ErrorCode": -7,
                 "ErrorMessage": "Invalid password."})

    return jsonify({"access_token": f"A1B2C3D4E5"})


#######################################################
# Helpers

def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    FROM: https://stackoverflow.com/questions/4255400/exclude-empty-null-values-from-json-serialization
    BY: https://stackoverflow.com/users/5563977/matanrubin
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value


if __name__ == '__main__':
    print(f"✏️ script is working in: {os.getcwd()}")
    app.run()
