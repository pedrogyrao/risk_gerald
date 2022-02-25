import sys,os
sys.path.append(os.getcwd())

import pytest
from parameterized import parameterized

from errors import ContractError, BadRuleFormat
from evaluation_rules import (
    risk_rule,
    map_scores,
    calculate_base_score,
    run_risk_rules,
)
from contract import assemble_empty_result, do_valid_input
from contract import (
    RISK_QUESTIONS,
    OWNED, MORTGAGED,
    INCOME,
    VEHICLE_YEAR,
    HOUSE_OWNERSHIP_STATUS,
    AGE,
    DISABILITY_KEY,
    LIFE_KEY
)
from evaluation_rules import (
    disable_rule,
    age_rule,
    age_points,
    income_rule,  #todo: add tests for the remaining rules
    house_ownership_rule,
    dependents_rule,
    marital_state_rule,
    vehicle_rule,
)
from evaluation_rules import (
    INFO_TO_INSURANCE,
    LAST_AGE_THRESHOLD,
    INELIGIBLE,
    REGULAR,
    RESPONSIBLE,
    ECONOMIC,
    FIRST_AGE_THRESHOLD,
    SECOND_AGE_THRESHOLD,
)

SCORE_MAP_CASES = [
    (3, RESPONSIBLE),
    (10, RESPONSIBLE),
    (1, REGULAR),
    (2, REGULAR),
    (0, ECONOMIC),
    (-10, ECONOMIC)
]


DISABLE_RULE_ELEGIBLE_CASES = [
    (INCOME, 10),
    (INCOME, 1000000000000),
    (VEHICLE_YEAR, 1900),
    (VEHICLE_YEAR, 2022),
    (HOUSE_OWNERSHIP_STATUS, OWNED),
    (HOUSE_OWNERSHIP_STATUS, MORTGAGED),
]


AGE_POINTS_CASES = [
    (FIRST_AGE_THRESHOLD - 1, -2),
    (SECOND_AGE_THRESHOLD - 1, -1),
    (SECOND_AGE_THRESHOLD, 0),
    (SECOND_AGE_THRESHOLD + 1, 0)
]


def test_calculate_base_score():
    base_data = {
        RISK_QUESTIONS: [1, 1, 1]
    }
    base_score = calculate_base_score(base_data)
    assert base_score == 3


def test_calculate_base_score_contract_break():
    base_data = {
        RISK_QUESTIONS: ['']
    }
    with pytest.raises(ContractError):
        calculate_base_score(base_data)


def test_good_rule_format():
    @risk_rule
    def my_rule(data, result):
        return result


def test_bad_rule_format():
    with pytest.raises(BadRuleFormat):
        @risk_rule
        def wrong_order_rule(result, data):
            return data, result

    with pytest.raises(BadRuleFormat):
        @risk_rule
        def more_arguments_rule(data, result, key=10):
            return data, result


@parameterized.expand(SCORE_MAP_CASES)
def test_map_scores(score, ensurance_line_result):
    base_result = assemble_empty_result(score)
    result = map_scores(base_result)
    for value in result.values():
        assert value == ensurance_line_result


@parameterized.expand(DISABLE_RULE_ELEGIBLE_CASES)
def test_disable_rule_eligible(key, value):
    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[key] = value
    result = disable_rule(data, result)

    line_result = result[INFO_TO_INSURANCE[key]]
    assert line_result != INELIGIBLE


def test_disable_rule_ineligible():
    result = assemble_empty_result(0)
    data = do_valid_input({})
    result = disable_rule(data, result)

    for value in INFO_TO_INSURANCE.values():
        line_result = result[value]
        assert line_result == INELIGIBLE


def test_age_rule_ineligible():
    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[AGE] = LAST_AGE_THRESHOLD + 1
    result = age_rule(data, result)
    assert result[LIFE_KEY] == INELIGIBLE
    assert result[DISABILITY_KEY] == INELIGIBLE

    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[AGE] = LAST_AGE_THRESHOLD + 100
    result = age_rule(data, result)
    assert result[LIFE_KEY] == INELIGIBLE
    assert result[DISABILITY_KEY] == INELIGIBLE

def test_age_rule_eligible():
    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[AGE] = LAST_AGE_THRESHOLD
    result = age_rule(data, result)
    assert result[LIFE_KEY] != INELIGIBLE
    assert result[DISABILITY_KEY] != INELIGIBLE

    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[AGE] = LAST_AGE_THRESHOLD - 10
    result = age_rule(data, result)
    assert result[LIFE_KEY] != INELIGIBLE
    assert result[DISABILITY_KEY] != INELIGIBLE


@parameterized.expand(AGE_POINTS_CASES)
def test_age_points(age, expected_value):
    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[AGE] = age
    result = age_points(data, result)
    for value in result.values():
        assert value == expected_value


def test_run_risk_rules_should_not_remove_inelegible_states():
    base_data = {
        "age": 35,
        "dependents": 2,
        "house_onwership_status": "owned",
        "income": 200000,
        "marital_status": "married",
        "vehicle_year": 2018
    }
    result = assemble_empty_result(base_score=INELIGIBLE)
    result = run_risk_rules(base_data, result)
    for value in result.values():
        assert value == INELIGIBLE
