import json
import constants


class SettingsDecoder:
    def __class_getitem__(cls, key):
        return getattr(cls, key)

    @staticmethod
    def load_settings_from_json():
        data = SettingsDecoder.get_decoded_json()
        for attr in data:
            SettingsDecoder.set_attribute(attr, data[attr])

    @staticmethod
    def set_attribute(attr_name, attr_value):
        setattr(SettingsDecoder, attr_name, attr_value)

    @staticmethod
    def save_current_settings_to_json():
        data = SettingsDecoder.get_decoded_json()
        attributes = vars(SettingsDecoder)
        for attr_name in attributes:
            if attr_name in data:
                data[attr_name] = attributes[attr_name]

        with open(constants.SETTINGS_FILE_NAME, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def get_decoded_json():
        with open(constants.SETTINGS_FILE_NAME, 'r') as file:
            return json.load(file)
