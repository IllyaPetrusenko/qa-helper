from functions import *
from flask import Flask, render_template, request, flash

app = Flask(__name__)

host = 'http://10.0.20.126:8900/api/v1'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/create_ei", methods=["GET", "POST"])
def create_ei():
    if request.method == 'POST':
        result = request.form
        payload = {
            "tender": {
                "title": result['tender_title'],
                "description": result['tender_description'],
                "classification": {
                    "id": result['classification']
                }
            },
            "planning": {
                "budget": {
                    "period": {
                        "startDate": result['startDate'] + 'T00:00:00Z',
                        "endDate": result['endDate'] + 'T00:00:00Z'
                    }
                }
            },
            "buyer": {
                "name": result['buyer_name'],
                "identifier": {
                    "id": result['buyer_identifier_legalName'],
                    "scheme": result['buyer_identifier_scheme'],
                    "legalName": result['buyer_identifier_legalName']
                },
                "address": {
                    "streetAddress": result['buyer_address_streetAddress'],
                    "addressDetails": {
                        "country": {
                            "id": result['country']
                        },
                        "region": {
                            "id": result['region']
                        },
                        "locality": {
                            "scheme": "iso-alpha2",
                            "id": result['locality'],
                            "description": "kek"
                        }
                    }
                },
                "contactPoint": {
                    "name": result['contact_point_name'],
                    "email": result['contact_point_email'],
                    "telephone": result['contact_point_email']
                }
            }
        }
        access_token = get_access_token(host)
        x_operation_id = get_x_operation_id(host=host, token=access_token)
        ei = create_ei_env(host=host, token=access_token, x_operation_id=x_operation_id, payload=payload)
        if 'errors' in ei:
            flash(ei, 'error')
            return render_template('1.html')
        else:
            data = get_ei_release(host=host, cpid=ei)
            flash('EI was successfully created!', 'success')
            return render_template('results.html', data=data)
    else:
        return render_template('1.html')


@app.route("/srs")
def srs():
    return render_template('srs.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = False
    app.run(host="0.0.0.0", port=5002)
