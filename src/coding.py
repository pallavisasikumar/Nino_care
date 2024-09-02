from flask import *
from src.dbconnection import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "651283481564283"

@app.route('/')
def login():
    return render_template("login_index.html")


@app.route("/login_code",methods=['post'])
def login_code():
    username=request.form['textfield']
    password=request.form['textfield2']

    qry="SELECT * FROM login WHERE `username`=%s AND `password`=%s"
    val=(username,password)

    res=selectone(qry, val)
    if res is None:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''
    elif res['type']=="admin":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Admin");window.location="admin_home"</script>'''
    elif res['type']=="panchayath":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Panchayath");window.location="panchayath_home"</script>'''
    elif res['type']=="ashaworker":
        session['lid'] = res['id']
        return '''<script>alert("Welcome Ashaworker");window.location="panchayath_home"</script>'''
    elif res['type']=="user":
        session['lid'] = res['id']
        return '''<script>alert("Welcome User");window.location="user_home"</script>'''


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/registration_code", methods=['post'])
def registration_code():
    name = request.form['textfield']
    place=request.form['textfield2']
    post=request.form['textfield3']
    pin=request.form['textfield4']
    panchayath=request.form['panchayath']
    area=request.form['select']
    ph_no=request.form['textfield5']
    email=request.form['textfield6']
    pregnant=request.form['select2']
    number_of_child=request.form['child']
    latitude=request.form['textfield7']
    longitude=request.form['textfield8']
    username=request.form['textfield9']
    password=request.form['textfield10']

    qry = "INSERT INTO login VALUES(NULL,%s,%s,'pending')"
    id = iud(qry,(username,password))

    qry = "INSERT INTO USER VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    iud(qry,(id,panchayath, name, place, post, pin, area, ph_no, email, number_of_child, pregnant, latitude, longitude))

    return '''<script>alert("Successfully registered");window.location="/"</script>'''


#Admin===============================================================================


@app.route("/admin_home")
def admin_home():
    return render_template("Admin/admin_index.html")


@app.route("/add_panchayath", methods=['post'])
def add_panchayath():
    return render_template("Admin/add_panchayath.html")


@app.route("/insert_panchayath", methods=["post"])
def insert_panchayath():
    name = request.form["textfield"]
    taluk_name = request.form["textfield2"]
    district = request.form["textfield3"]
    ph_no = request.form["textfield4"]
    email = request.form["textfield5"]
    username = request.form["textfield6"]
    password = request.form["textfield7"]

    qry = "INSERT INTO login VALUES(NULL,%s,%s,'panchayath')"
    id = iud(qry,(username,password))

    qry = "INSERT INTO panchayath VALUES(NULL,%s,%s,%s,%s,%s,%s)"
    iud(qry,(id, name, taluk_name, district, ph_no, email))

    return '''<script>alert("Successfully Inserted Panchayath");window.location="manage_panchayath"</script>'''

@app.route("/delete_panchayath")
def delete_panchayath():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE id=%s"
    iud(qry, id)
    qry = "DELETE FROM `panchayath` WHERE `l_id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_panchayath"</script>'''


@app.route("/edit_panchayath")
def edit_panchayath():
    id = request.args.get('id')
    session['pid'] = id
    qry = "SELECT * FROM `panchayath` JOIN `login` ON `panchayath`.`l_id`=`login`.`id` WHERE panchayath.l_id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_panchayath.html", val = res)


@app.route("/update_panchayath" , methods=['post'])
def update_panchayath():
    print(request.form)
    name = request.form["textfield"]
    taluk_name = request.form["textfield2"]
    district = request.form["textfield3"]
    ph_no = request.form["textfield4"]
    email = request.form["textfield5"]
    username = request.form["textfield6"]
    password = request.form["textfield7"]

    qry = "UPDATE `login` SET `username`=%s, `password`=%s WHERE `id`=%s"
    iud(qry, (username,password,session['pid']))

    qry = "UPDATE `panchayath` SET `name`=%s, `taluk_name`=%s, `district`=%s, `ph_no`=%s, `email`=%s WHERE `l_id`=%s"
    iud(qry, (name, taluk_name, district, ph_no, email, session['pid']))

    return '''<script>alert("Successfully edited");window.location="manage_panchayath"</script>'''


@app.route("/insert_scheme", methods=["post"])
def insert_scheme():
    name = request.form["textfield"]
    details = request.form["textfield2"]

    qry = "INSERT INTO `gov_schemes` VALUES(NULL,%s,%s,CURDATE())"
    val =  (name, details)
    iud(qry,val)
    return '''<script>alert("Success");window.location="manage_scheme"</script>'''


@app.route("/delete_scheme")
def delete_scheme():
    id=request.args.get('id')
    qry="DELETE FROM `gov_schemes` WHERE id=%s"
    iud(qry,id)
    return '''<script>alert("Successfully Deleted");window.location="manage_scheme"</script>'''


@app.route("/edit_scheme")
def edit_scheme():
    id = request.args.get('id')
    session['sid'] = id
    qry = "SELECT * FROM`gov_schemes` WHERE id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_scheme.html" , val=res )


@app.route("/update_scheme", methods=['post'])
def update_scheme():
    name = request.form["textfield"]
    details = request.form["textfield2"]

    qry="UPDATE `gov_schemes` SET `scheme_name`=%s, `details`=%s WHERE id=%s"
    iud(qry,(name,details, session['sid']))
    return '''<script>alert("Successfully edited");window.location="manage_scheme"</script>'''


@app.route("/add_scheme",methods=["post"])
def add_scheme():
    return render_template("Admin/add_scheme.html")


@app.route("/manage_panchayath")
def manage_panchayath():
    qry = "SELECT * FROM `panchayath`"
    res = selectall(qry)
    # print(res) (just to check if the code works)
    return render_template("Admin/manage_panchayath.html", val = res)


@app.route("/manage_scheme")
def manage_scheme():
    qry = "SELECT * FROM `gov_schemes`"
    res = selectall(qry)
    # print(res) (just to check if the code works)
    return render_template("Admin/manage_scheme.html",val=res)


@app.route("/view_report")
def view_report():
    qry="SELECT panchayath.name,reports.* FROM panchayath JOIN reports ON panchayath.l_id=reports.panchayath_id"
    res=selectall(qry)
    return render_template("Admin/view_report.html",val=res)


@app.route("/add_food_details",methods=["post"])
def add_food_details():
    return render_template("Admin/add_food_details.html")


@app.route("/insert_food", methods=["post"])
def insert_food():
    food = request.form["textfield"]
    image = request.files["file1"]
    details = request.form["textfield2"]
    consumer_type = request.form["select"]

    image_name = secure_filename(image.filename)
    image.save(os.path.join('static/uploads',image_name))


    qry = "INSERT INTO food VALUES(NULL,%s,%s,%s,%s)"
    val = (food,image_name,details,consumer_type)
    iud(qry, val)
    return '''<script>alert("added food details");window.location="manage_food"</script>'''


@app.route("/delete_food")
def delete_food():
    id=request.args.get('id')
    qry="DELETE FROM `food` WHERE id=%s"
    iud(qry,id)
    return '''<script>alert("Successfully Deleted");window.location="manage_food"</script>'''


@app.route("/edit_food")
def edit_food():
    id = request.args.get('id')
    session['fid'] = id
    qry = "SELECT * FROM `food` WHERE id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_food_details.html", val=res)


@app.route("/update_food", methods=['post'])
def update_food():

    try:
        food = request.form["textfield"]
        image = request.files["file1"]
        details = request.form["textfield2"]
        consumer_type = request.form["select"]

        image_name = secure_filename(image.filename)
        image.save(os.path.join('static/uploads', image_name))

        qry = "UPDATE `food` SET `food`=%s, `image`=%s, `details`=%s, `type`=%s WHERE `id`=%s"
        val = (food, image_name, details, consumer_type, session['fid'])
        iud(qry, val)
        return '''<script>alert("Food details updated");window.location="manage_food"</script>'''

    except:
        food = request.form["textfield"]

        details = request.form["textfield2"]
        consumer_type = request.form["select"]

        qry = "UPDATE `food` SET `food`=%s, `details`=%s, `type`=%s WHERE `id`=%s"
        val = (food, details, consumer_type, session['fid'])
        iud(qry, val)
        return '''<script>alert("Successfully edited");window.location="manage_food"</script>'''


@app.route("/manage_food")
def manage_food():
    qry = "SELECT * FROM food"
    res = selectall(qry)
    return render_template("Admin/manage_food.html",val=res)


#panchayath==========================================================================
@app.route("/panchayath_home")
def panchayath_home():
    return render_template("panchayath/panchayath_index.html")


@app.route("/manage_area")
def manage_area():
    qry = "SELECT * FROM `area` WHERE pid=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_area.html", val=res)


@app.route("/add_area", methods=['post'])
def add_area():
    return render_template("panchayath/add_area.html")


@app.route("/insert_area", methods=['post'])
def insert_area():
    area = request.form['textfield']
    qry = "INSERT INTO `area` VALUES(NULL,%s,%s)"
    iud(qry, (session['lid'], area))
    return '''<script>alert("Susscessfully Added");window.location="manage_area"</script>'''


@app.route("/delete_area")
def delete_area():
    id = request.args.get('id')
    qry = "DELETE FROM `area` WHERE id=%s"
    iud(qry, id)
    return '''<script>alert("Successfully deleted");window.location="manage_area"</script>'''


@app.route('/add_ashaworker', methods=['post'])
def add_ashaworker():
    qry = "select * from area where pid=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/add_ashaworker.html", val=res)


@app.route("/insert_ashaworker", methods=['post'])
def insert_ashaworker():
    name = request.form['textfield']
    post_office = request.form['textfield2']
    place = request.form['textfield3']
    pincode = request.form['textfield4']
    email = request.form['textfield5']
    phone = request.form['textfield6']
    area = request.form['select']
    username = request.form['textfield7']
    password = request.form['textfield8']

    qry = "INSERT INTO login VALUES(NULL,%s,%s,'ashaworker')"
    id = iud(qry, (username, password))

    qry = "INSERT INTO `ashaworker` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    iud(qry, (id,session['lid'],name, post_office, place, pincode, email, phone, area))
    return '''<script>alert("Successfully Added Ashaworker");window.location="manage_ashaworker"</script>'''


@app.route("/delete_ashaworker")
def delete_ashaworker():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE id=%s"
    iud(qry, id)
    qry = "DELETE FROM `ashaworker` WHERE `l_id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_ashaworker"</script>'''



@app.route("/edit_ashaworker")
def edit_ashaworker():
    id = request.args.get('id')
    session['aid'] = id
    qry = "SELECT * FROM `ashaworker` WHERE l_id= %s"
    res = selectone(qry, id)

    qry = "SELECT `area`.* FROM `area` where pid=%s"
    res1 = selectall2(qry, session['lid'])

    return render_template("panchayath/edit_ashaworker.html", val=res, val2=res1)


@app.route("/update_ashaworker", methods=['post'])
def update_ashaworker():
    name = request.form['textfield']
    post_office = request.form['textfield2']
    place = request.form['textfield3']
    pincode = request.form['textfield4']
    email = request.form['textfield5']
    phone = request.form['textfield6']
    area = request.form['select']

    qry = "UPDATE `ashaworker` SET `name`=%s, `place`=%s, `post`=%s, `pin`=%s, `email`=%s, `ph_no`=%s, `area`=%s WHERE `l_id`=%s"
    iud(qry,(name, place, post_office, pincode, email, phone, area, session['aid']))

    return '''<script>alert("Susscessfully edited");window.location="manage_ashaworker"</script>'''


@app.route("/add_program", methods=['post'])
def add_program():
    return render_template("panchayath/add_program.html")


@app.route("/insert_program", methods=['post'])
def insert_program():
    program = request.files['textfield']

    prgrm_name = secure_filename(program.filename)
    program.save(os.path.join("static/uploads", prgrm_name))

    qry = "INSERT `programs` VALUES(NULL,%s,%s,CURDATE())"
    iud(qry, (session['lid'], prgrm_name))

    return '''<script>alert("Success");window.location="manage_panchayath_program"</script>'''


@app.route("/delete_program")
def delete_program():
    id = request.args.get('id')

    qry = "DELETE FROM `programs` WHERE `id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_panchayath_program"</script>'''


@app.route("/add_vaccine_details", methods=['post'])
def add_vaccine_details():
    return render_template("panchayath/add_vaccine_details.html")


@app.route("/insert_vaccine_details", methods=['post'])
def insert_vaccine_details():
    vaccine_name = request.form['textfield']
    details = request.form['textfield2']
    type = request.form['textfield3']

    qry = "INSERT INTO `vaccine` VALUES(NULL,%s,%s,%s,%s)"
    iud(qry,(session['lid'],vaccine_name,details,type))
    return '''<script>alert("successfully added");window.location="manage_vaccination_details"</script>'''


@app.route("/delete_vaccination_details")
def delete_vaccination_details():
    id = request.args.get('id')

    qry = "DELETE FROM `vaccine` WHERE `id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_vaccination_details"</script>'''


@app.route("/edit_vaccination_details")
def edit_vaccination_details():
    id = request.args.get('id')
    session['vid'] = id
    qry = "SELECT * FROM `vaccine` WHERE id=%s"
    res = selectone(qry, id)
    print(res)
    return render_template("panchayath/edit_vaccine_details.html", val=res)


@app.route("/update_vaccination_details", methods=['post'])
def update_vaccination_details():
    vaccine_name = request.form['textfield']
    details = request.form['textfield2']
    type = request.form['textfield3']

    qry = "UPDATE `vaccine` SET `vaccine_name`=%s , `details`=%s, `type`=%s WHERE `id`=%s"
    iud(qry,(vaccine_name,details,type,session['vid']))

    return '''<script>alert("Successfully Edited");window.location="manage_vaccination_details"</script>'''


@app.route("/manage_ashaworker")
def manage_ashaworker():
    qry = "SELECT `ashaworker`.*,`area`.area AS area_name FROM `ashaworker` JOIN `area` ON `ashaworker`.`area`=`area`.id WHERE `panchayath_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_ashaworker.html",val=res)


@app.route("/manage_panchayath_program")
def manage_panchayath_program():
    qry="SELECT * FROM `programs` WHERE `panchayath_id`=%s"
    res=selectall2(qry,session['lid'])
    return render_template("panchayath/manage_panchayath_program.html", val=res)


@app.route("/view_food")
def view_food():
    qry = "SELECT * FROM `food`"
    res = selectall(qry)
    return render_template("panchayath/view_food.html", val = res)


@app.route("/manage_vaccination_details")
def manage_vaccination_details():
    qry="SELECT * FROM `vaccine` WHERE `panchayath_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_vaccination_details.html", val=res)


@app.route("/view_mothers_details")
def view_mothers_details():
    return render_template("panchayath/view_mothers_details.html")

#ashaworker============================================================================
@app.route("/ashaworker_home")
def ashaworker_home():
    return render_template("Ashaworker/ashaworker_home.html")


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
@app.route("/user_home")
def user_home():
    return render_template("User/user_home.html")


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