import sys,os
sys.path.append(os.getcwd())

import pytest
from parameterized import parameterized

from errors import ContractError, BadRuleFormat
from evaluation_rules import (
    risk_rule,
    run_risk_rules,
    map_scores,
    evaluate,
    calculate_base_score,
)
from contract import RISK_QUESTIONS


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
