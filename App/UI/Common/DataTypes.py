class String:
    @staticmethod
    def is_valid(input_data):
        # Filtrare l'input se non é un carattere alfanumerico (tipo Alt, Ctrl, ecc... non devono ritornare True)
        return True

    @staticmethod
    def get_converted_data(input_data):
        return str(input_data)


class Char:
    @staticmethod
    def is_valid(input_data):
        if len(input_data) > 1:
            return False
        return True

    @staticmethod
    def get_converted_data(input_data):
        return str(input_data)


class Integer:
    @staticmethod
    def is_valid(input_data):
        try:
            int(input_data)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_converted_data(input_data):
        try:
            return int(input_data)
        except ValueError:
            return 1
