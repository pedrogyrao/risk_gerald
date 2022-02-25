from isodate import DT_BAS_ORD_COMPLETE
import pytest
from parameterized import parameterized

from risk_gerald.contract import (
    do_valid_input,
    AGE,
    DEPENDENTS,
    HOUSE,
    OWNERSHIP_STATUS,
    HOUSE_OWNERSHIP_STATUS,
    INCOME,
    MARITAL_STATUS,
    RISK_QUESTIONS,
    VEHICLE,
    YEAR,
    VEHICLE_YEAR,
    ContractError,
)

BREAK_CONTRACT_CASES = [
    (AGE, '10'),
    (DEPENDENTS, '10'),
    (HOUSE, {OWNERSHIP_STATUS: 10}),
    (INCOME, '10'),
    (MARITAL_STATUS, 10),
    (RISK_QUESTIONS, '10'),
    (VEHICLE, {YEAR: '2000'}),
]


def test_empty_data():
    data = do_valid_input({})
    expected_data = {
        AGE: None,
        DEPENDENTS: None,
        HOUSE_OWNERSHIP_STATUS: None,
        INCOME: None,
        MARITAL_STATUS: None,
        RISK_QUESTIONS: None,
        VEHICLE_YEAR: None,
    }
    assert data == expected_data


@parameterized.expand(BREAK_CONTRACT_CASES)
def test_wrong_contract_type_raises(key, value):
    data = {key: value}
    with pytest.raises(ContractError):
        data = do_valid_input(data)


def test_happy_contract():
    base_data = {
        "age": 35,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    expected_data = {
        'age': 35,
        'dependents': 2,
        'income': 0,
        'marital_status': 'married',
        'risk_questions': [0, 1, 0],
        'house_onwership_status': 'owned',
        'vehicle_year': 2018}
    data = do_valid_input(base_data)
    assert data == expected_data
