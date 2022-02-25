# Risk Evaluation

This project provides a single endpoint backend that evaluates risk from the clients information.


# Risk Evaluation Engine

The risk evalulation engine is consisted of a series of rules that are applied to the result objects it has 3 steps:

1. base score calculation and base result creation;
1. risk evaluation rules applying;
1. mapping risk points to lines.

## 1. Base Score Calculation and Base Result Creation

This step calculates the base score and assemble an object containing this value for each ensurance line.

If ```risk_questions": [0, 1, 0]``` is provided by the client the base result will be:

```json
{
    "auto": 1,
    "disability": 1,
    "home": 1,
    "life": 1
}
```

## 2. Risk Evaluation Rules Applying

In order to make this step extensible a pattern of rule was created.

A rule is defined by a function that has as arguments "data" and "result" and returns the "result". It should not alter already "ineligible" lines in result object. To define a rule use the ```@risk_rule``` decorator.

If the rule does not have the right argument names in the right order a ```BadRuleFormat``` exception will be raised.

Creating a rule:

```python
@risk_rule
def my_rule(data, result):
    return data, result
```

## 3. Mapping Risk Points to Lines.

This last step does the range mapping between risk points and the expected ranges. Nothing fancy here:

```text
    - 0 and below -> “economic”
    - 1 and 2 -> “regular”
    - 3 and above -> “responsible”
```

# Running the Application

1. Clone repository:

    ```bash
    git clone https://github.com/pedrogyrao/risk_gerald
    cd risk_gerald
    ```

1. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

1. Run the application:

    ```bash
    python app.py
    ```

1. Run tests:

    ```bash
    pytest -s
    ```
