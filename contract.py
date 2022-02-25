from errors import ContractError


# Input Data Keys
# todo: turn then into a structure like enum
AGE = "age"  # 35
DEPENDENTS = "dependents"  # 2
HOUSE = "house"
OWNERSHIP_STATUS = "ownership_status"  # "owned"
HOUSE_OWNERSHIP_STATUS = 'house_onwership_status'
INCOME = "income"  # 0
MARITAL_STATUS = "marital_status"  # "married"
RISK_QUESTIONS = "risk_questions"  # [0, 1, 0]
VEHICLE = "vehicle"
YEAR = "year"  # 2018
VEHICLE_YEAR = 'vehicle_year'

# Response Keys
# todo: turn then into a structure like enum
AUTO_KEY = 'auto'
DISABILITY_KEY = 'disability'
HOME_KEY = 'home'
LIFE_KEY = 'life'

MAP_INPUT_TO_TYPE = {
    AGE: int,
    DEPENDENTS: int,
    HOUSE_OWNERSHIP_STATUS: str,
    INCOME: int,
    MARITAL_STATUS: str,
    RISK_QUESTIONS: list,
    VEHICLE_YEAR: int,
}

LIFE_INSURANCE = 'life'
DISABILITY_INSURANCE = 'disability'
HOME_INSURANCE = 'home'
AUTO_INSURANCE = 'auto'

INSURANCE_LINES = [
    LIFE_INSURANCE,
    DISABILITY_INSURANCE,
    HOME_INSURANCE,
    AUTO_INSURANCE
]

MORTGAGED = 'mortgaged'
OWNED = 'owned'

MARRIED = 'married'
SINGLE = 'single'

validations = []


def validation(func):
    validations.append(func)
    return func


@validation
def fix_nested_data(data):
    house_ownership_status = data.pop(HOUSE, {}).pop(OWNERSHIP_STATUS, None)
    data[HOUSE_OWNERSHIP_STATUS] = house_ownership_status

    vehicle_year = data.pop(VEHICLE, {}).pop(YEAR, None)
    data[VEHICLE_YEAR] = vehicle_year

    return data


@validation
def add_missing_keys(data):
    for key in MAP_INPUT_TO_TYPE.keys():
        if key not in data:
            data[key] = None
    return data


@validation
def check_input_types(data):
    for key, type_ in MAP_INPUT_TO_TYPE.items():
        if data[key]:
            info_type = type(data[key])
            if info_type != type_:
                raise ContractError(
                    'Invalid Type {type_} for {key} info.'.format(
                        type_=info_type, key=key))
    return data


def do_valid_input(data):
    for validation in validations:
        data = validation(data)
    return data


def is_house_mortgaged(data):
    return data[HOUSE_OWNERSHIP_STATUS] == MORTGAGED


def is_married(data):
    return data[MARITAL_STATUS] == MARRIED


def assemble_empty_result(base_score):
    return {
        "auto": base_score,
        "disability": base_score,
        "home": base_score,
        "life": base_score
    }
