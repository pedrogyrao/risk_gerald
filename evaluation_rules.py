import datetime
from contract import assemble_empty_result

# input related
from contract import (
    AGE,
    DEPENDENTS,
    HOUSE_OWNERSHIP_STATUS,
    INCOME,
    RISK_QUESTIONS,
    VEHICLE_YEAR,
)
# ensurance related
from contract import (
    INSURANCE_LINES,
    AUTO_KEY,
    DISABILITY_KEY,
    HOME_KEY,
    LIFE_KEY,
)
from contract import is_house_mortgaged, is_married

INELIGIBLE = 'ineligible'
INFO_TO_INSURANCE = {
    INCOME: DISABILITY_KEY,
    VEHICLE_YEAR: AUTO_KEY,
    HOUSE_OWNERSHIP_STATUS: HOME_KEY
}
DISABLED_INSURANCE_KEYS = [INCOME, VEHICLE_YEAR, HOUSE_OWNERSHIP_STATUS]
FIRST_AGE_THRESHOLD = 30
SECOND_AGE_THRESHOLD = 40
LAST_AGE_THRESHOLD = 60
INCOME_THRESHOLD = 200000
VEHICLE_YEAR_THRESHOLD = 5

ECONOMIC = 'economic'
REGULAR = 'regular'
RESPONSIBLE = 'responsible'

RULE_ARGNAMES = ('data', 'result')
risk_rules = []


class BadRuleFormat(Exception):
    pass


def risk_rule(rule):
    func_args = rule.__code__.co_varnames
    if func_args != RULE_ARGNAMES:
        raise BadRuleFormat(
            'Rule {rule} has bad arguments {args}'.format(
                rule=rule.__name__,
                args=func_args
            ))
    risk_rules.append(rule)
    return rule


def _run_deduction(result, deduct, insurance_lines=INSURANCE_LINES):
    for insurance_line in insurance_lines:
        if type(result[insurance_line]) == int:
            result[insurance_line] -= deduct
    return result


def run_risk_rules(data, result):
    for risk_rule in risk_rules:
        result = risk_rule(data, result)
    return result


@risk_rule
def disable_rule(data, result):
    '''
    If the user doesn’t have income, vehicles or houses, the user is
    ineligible for disability, auto, and home insurance, **respectively**.
    '''

    for key in DISABLED_INSURANCE_KEYS:
        if not data[key]:
            insurance_type = INFO_TO_INSURANCE[key]
            result[insurance_type] = INELIGIBLE
    return result


@risk_rule
def age_rule(data, result):
    '''
    If the user is over 60 years old, the user is
    ineligible for disability and life insurance.
    '''
    if data[AGE] > LAST_AGE_THRESHOLD:
        result['life'] = INELIGIBLE
        result['disability'] = INELIGIBLE
    return result


@risk_rule
def age_points(data, result):
    '''
    If the user is under 30 years old, deduct 2 risk points from all
    lines of insurance. If the user is between 30 and 40 years old, deduct 1.
    '''
    deduct = 0
    if data[AGE] < FIRST_AGE_THRESHOLD:
        deduct = 2
    elif data[AGE] < SECOND_AGE_THRESHOLD:
        deduct = 1
    return _run_deduction(result, deduct)


@risk_rule
def income_rule(data, result):
    '''
    If the user's income is above $200k, deduct 1 risk point
    from all lines of insurance.
    '''
    deduct = 1 if data[INCOME] > INCOME_THRESHOLD else 0
    return _run_deduction(result, deduct)


@risk_rule
def house_ownership_rule(data, result):
    '''
    If the user's house is mortgaged, add 1 risk point to the
    users’s home score and add 1 risk point to her disability score.
    '''
    if is_house_mortgaged(data):
        return _run_deduction(result, -1, insurance_lines=[HOME_KEY, DISABILITY_KEY])
    return result


@risk_rule
def dependents_rule(data, result):
    '''
    If the user has dependents, add 1 risk point to
    both the disability and life scores.
    '''
    if data[DEPENDENTS]:
        return _run_deduction(result, -1, insurance_lines=[DISABILITY_KEY, LIFE_KEY])
    return result


@risk_rule
def marital_state_rule(data, result):
    '''
    If the user is married, add 1 risk point to the life score
    and remove 1 risk point from disability.
    '''
    if is_married(data):
        return _run_deduction(result, -1, insurance_lines=[LIFE_KEY, DISABILITY_KEY])
    return result


@risk_rule
def vehicle_rule(data, result):
    '''
    If the user's vehicle was produced in the last 5 years,
    add 1 risk point to that vehicle’s score.
    '''
    current_year = datetime.datetime.now().year
    last_acceptable_year = current_year - VEHICLE_YEAR_THRESHOLD
    if (data[VEHICLE_YEAR] != None) and data[VEHICLE_YEAR] >= last_acceptable_year:
        return _run_deduction(result, -1, insurance_lines=[AUTO_KEY])
    return result


def calculate_base_score(data):
    base_score = sum(data[RISK_QUESTIONS])
    return base_score


def map_scores(result):
    '''
    - 0 and below -> “economic”
    - 1 and 2 -> “regular”
    - 3 and above -> “responsible”
    '''
    for key, value in result.items():
        if value == INELIGIBLE:
            continue
        if value < 1:
            result[key] = ECONOMIC
        elif value < 3:
            result[key] = REGULAR
        else:
            result[key] = RESPONSIBLE
    return result


def evaluate(data):
    base_score = calculate_base_score(data)
    result = assemble_empty_result(base_score)
    result = run_risk_rules(data, result)
    result = map_scores(result)
    return result
