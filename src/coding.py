from flask import *
from src.dbconnection import *

app = Flask(__name__)


@app.route('/')
def login():
    return render_template("login.html")


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")

#Admin===============================================================================
@app.route("/add_panchayath")
def add_panchayath():
    return render_template("Admin/add_panchayath.html")


@app.route("/add_scheme")
def add_scheme():
    return render_template("Admin/add_scheme.html")


@app.route("/manage_panchayath")
def manage_panchayath():
    return render_template("Admin/manage_panchayath.html")


@app.route("/manage_scheme")
def manage_scheme():
    return render_template("Admin/manage_scheme.html")


@app.route("/view_report")
def view_report():
    return render_template("Admin/view_report.html")

#panchayath==================================================================================
@app.route('/add_ashaworker')
def add_ashaworker():
    return render_template("panchayath/add_ashaworker.html")


@app.route("/add_food_details")
def add_food_details():
    return render_template("panchayath/add_food_details.html")


@app.route("/add_program")
def add_program():
    return render_template("panchayath/add_program.html")


@app.route("/add_vaccine_details")
def add_vaccine_details():
    return render_template("panchayath/add_vaccine_details.html")


@app.route("/manage_ashaworker")
def manage_ashaworker():
    return render_template("panchayath/manage_ashaworker.html")


@app.route("/manage_food")
def manage_food():
    return render_template("panchayath/manage_food.html")


@app.route("/manage_panchayath_program")
def manage_panchayath_program():
    return render_template("Admin/manage_panchayath_program.html")


@app.route("/manage_vaccination_details")
def manage_vaccination_details():
    return render_template("Admin/manage_vaccination_details.html")


@app.route("/view_mothers_details")
def view_mothers_details():
    return render_template("Admin/view_mothers_details.html")

#ashaworker============================================================================
@app.route("/add_child")
def add_child():
    return render_template("Ashaworker/add_child.html")


@app.route("/manage_child_details")
def manage_child_details():
    return render_template("Ashaworker/manage_child_details.html")


@app.route("/manage_users")
def manage_users():
    return render_template("Ashaworker/manage_users.html")


@app.route("/verify_users")
def verify_users():
    return render_template("Ashaworker/verify_users.html")


@app.route("/view_programs_schemes")
def view_programs_schemes():
    return render_template("Ashaworker/view_programs_schemes.html")

#User===========================================================================
@app.route("/view_food_details")
def view_food_details():
    return render_template("User/view_food_details.html")


@app.route("/view_programs_and_schemes")
def view_programs_and_schemes():
    return render_template("User/view_programs_and_schemes.html")


@app.route("/view_vaccine_details")
def view_vaccine_details():
    return render_template("User/view_vaccine_details.html")

app.run(debug=True)