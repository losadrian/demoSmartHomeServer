class SmartHomeDevice:
    """A SmartHomeDevice class"""

    def __init__(self, device_id, product_name, manufacturer, communication):
        self.device_id = device_id
        self.product_name = product_name
        self.manufacturer = manufacturer
        self.communication = communication
