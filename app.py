from flask import Flask, request, abort

from contract import do_valid_input, ContractError
from evaluation_rules import evaluate

app = Flask(__name__)



@app.route('/evaluate_risk', methods = ['POST'])
def evalulate_risk():
    try:
        data = do_valid_input(request.json)
        response = evaluate(data)
    except ContractError as e:
        return abort(400)
    except Exception as e:
        return abort(500)
    return response


if __name__ == '__main__':
   app.run()
