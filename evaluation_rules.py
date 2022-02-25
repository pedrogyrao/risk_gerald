'''
4. If the user's income is above $200k, deduct 1 risk point from all lines of insurance.
5. If the user's house is mortgaged, add 1 risk point to the users’s home score and add 1 risk point to her disability score.
6. If the user has dependents, add 1 risk point to both the disability and life scores.
7. If the user is married, add 1 risk point to the life score and remove 1 risk point from disability.
8. If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.
'''
from contract import assemble_empty_result

# input related keys
from contract import (
    AGE,
    DEPENDENTS,
    HOUSE_OWNERSHIP_STATUS,
    INCOME,
    MARITAL_STATUS,
    RISK_QUESTIONS,
    VEHICLE_YEAR,
)
from contract import INSURANCE_LINES

INELIGIBLE = 'ineligible'

INFO_TO_INSURANCE = {
    'income': 'disability',
    'vehicle': 'auto',
    'house': 'insurance'
}

#todo: move keys to a contract file
DISABLED_INSURANCE_KEYS = [INCOME, VEHICLE_YEAR, HOUSE_OWNERSHIP_STATUS]

FIRST_AGE_THRESHOLD = 30
SECOND_AGE_THRESHOLD = 40
LAST_AGE_THRESHOLD = 60



def disable_rule(data, result):  # 1
    '''
    If the user doesn’t have income, vehicles or houses, the user is
    ineligible for disability, auto, and home insurance, **respectively**.
    '''

    for key in DISABLED_INSURANCE_KEYS:
        if not data[key]:
            insurance_type = INFO_TO_INSURANCE[key]
            result[insurance_type] = INELIGIBLE
    return result


def age_rule(data, result):  # 2
    '''
    If the user is over 60 years old, the user is
    ineligible for disability and life insurance.
    '''
    if data[AGE] > LAST_AGE_THRESHOLD:
        result['life'] = INELIGIBLE
        result['disability'] = INELIGIBLE
    return result



def age_points(data, result):
    '''If the user is under 30 years old, deduct 2 risk points from all
    lines of insurance. If the user is between 30 and 40 years old, deduct 1.
    '''
    deduct = 0
    if data[AGE] < FIRST_AGE_THRESHOLD:
        deduct = 2
    elif data[AGE] < SECOND_AGE_THRESHOLD:
        deduct = 1

    for insurance_line in INSURANCE_LINES:
        if type(result[insurance_line]) == int:
            result[insurance_line] -= deduct


    return result


def evaluate(data):
    result = assemble_empty_result()
    result = disable_rule(data, result)
    result = age_rule(data, result)
    result = age_points(data, result)
    return result
