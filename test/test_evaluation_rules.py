import sys,os
sys.path.append(os.getcwd())

import pytest
from parameterized import parameterized

from errors import ContractError, BadRuleFormat
from evaluation_rules import (
    risk_rule,
    map_scores,
    calculate_base_score,
    INELIGIBLE,
    REGULAR,
    RESPONSIBLE,
    ECONOMIC
)
from contract import assemble_empty_result, do_valid_input
from contract import (
    RISK_QUESTIONS,
    OWNED, MORTGAGED,
    INCOME,
    VEHICLE_YEAR,
    HOUSE_OWNERSHIP_STATUS,
)
from evaluation_rules import (
    disable_rule,
    age_rule,
    age_points,
    income_rule,
    house_ownership_rule,
    dependents_rule,
    marital_state_rule,
    vehicle_rule,
    INFO_TO_INSURANCE
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
        return data, result


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
def test_disable_rule_not_ELGIBLE_CASES(key, value):
    result = assemble_empty_result(0)
    data = do_valid_input({})
    data[key] = value
    result = disable_rule(data, result)

    line_result = result[INFO_TO_INSURANCE[key]]
    assert line_result != INELIGIBLE
