from flask import *
from src.dbconnection import *
from werkzeug.utils import secure_filename
import os
from flask_mail import *
from email import encoders
import random
import functools
from apscheduler.schedulers.background import BackgroundScheduler
import google.generativeai as genai


def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('login_index.html')
        return func()

    return secure_function





genai.configure(api_key="AIzaSyBAwI-VC--dAg9opup6ZihgFrwNHsipKkM")


app = Flask(__name__)

app.secret_key = "651283481564283"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ninocareproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'ioon ywiq cqkk bfaf'

@app.route('/')
def login():
    return render_template("login_index.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


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
        return '''<script>alert("Welcome Ashaworker");window.location="ashaworker_home"</script>'''
    elif res['type']=="user":
        session['lid'] = res['id']
        return '''<script>alert("Welcome User");window.location="user_home"</script>'''
    else:
        return '''<script>alert("Invalid Username or Password");window.location="/"</script>'''


@app.route("/user_reg1")
def user_reg1():

    return render_template("user_register_one.html")

@app.route("/select_taluks2")
def select_taluks2():
    dist = request.args.get("dist")
    qry = "SELECT DISTINCT(`taluk_name`) FROM `panchayath` WHERE `district`=%s"
    res = selectall2(qry, dist)
    return jsonify(res) #client server communication

@app.route("/user_reg_filter", methods=['POST'])
def user_reg_filter():
    district = request.form['dist']
    taluk = request.form['taluk']
    qry = "SELECT * FROM `panchayath` WHERE `district`=%s AND `taluk_name`=%s"
    res = selectall2(qry, (district, taluk))
    return jsonify(res)

@app.route("/user_registration", methods=['post'])
def user_registration():
    pid = request.form['select']
    session['pid'] = pid
    qry = "SELECT * FROM `area` WHERE pid=%s"
    res = selectall2(qry, pid)
    print(res)
    return render_template("user_registration.html", val=res)


@app.route("/registration_code", methods=['post'])
def registration_code():
    try:
        name = request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        area=request.form['select']
        ph_no=request.form['textfield5']
        email=request.form['textfield6']
        pregnant=request.form['select2']
        number_of_child=request.form['child']
        latitude=request.form['textfield7']
        longitude=request.form['textfield8']
        username=request.form['textfield9']
        password=request.form['textfield10']

        qry = "SELECT * FROM `login` WHERE `username`=%s"
        res = selectone(qry, username)

        if res is None:

            qry = "INSERT INTO login VALUES(NULL,%s,%s,'pending')"
            id = iud(qry,(username,password))

            qry = "INSERT INTO USER VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            iud(qry,(id, session['pid'], name, place, post, pin, area, ph_no, email, number_of_child, pregnant, latitude, longitude))

            return '''<script>alert("Successfully registered");window.location="/"</script>'''
        else:
            return '''<script>alert("Username already exists");window.location="/"</script>'''

    except:
        return '''<script>alert("Email or phone already exists");window.location="/"</script>'''


#Admin===============================================================================


@app.route("/admin_home")
@login_required
def admin_home():
    return render_template("Admin/admin_index.html")


@app.route("/add_panchayath")
@login_required
def add_panchayath():
    return render_template("Admin/add_panchayath.html")


@app.route("/insert_panchayath", methods=["post"])
@login_required
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
@login_required
def delete_panchayath():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE id=%s"
    iud(qry, id)
    qry = "DELETE FROM `panchayath` WHERE `l_id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_panchayath"</script>'''

@app.route("/edit_panchayath")
@login_required
def edit_panchayath():
    id = request.args.get('id')
    session['pid'] = id
    qry = "SELECT * FROM `panchayath` JOIN `login` ON `panchayath`.`l_id`=`login`.`id` WHERE panchayath.l_id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_panchayath.html", val = res)


@app.route("/update_panchayath" , methods=['post'])
@login_required
def update_panchayath():
    try:
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
    except:
        return '''<script>alert("Email or Phone already exists");window.location="manage_panchayath"</script>'''



@app.route("/insert_scheme", methods=["post"])
@login_required
def insert_scheme():
    name = request.form["textfield"]
    details = request.form["textfield2"]

    qry = "INSERT INTO `gov_schemes` VALUES(NULL,%s,%s,CURDATE())"
    val =  (name, details)
    iud(qry,val)
    return '''<script>alert("Success");window.location="manage_scheme"</script>'''


@app.route("/delete_scheme")
@login_required
def delete_scheme():
    id=request.args.get('id')
    qry="DELETE FROM `gov_schemes` WHERE id=%s"
    iud(qry,id)
    return '''<script>alert("Successfully Deleted");window.location="manage_scheme"</script>'''


@app.route("/edit_scheme")
@login_required
def edit_scheme():
    id = request.args.get('id')
    session['sid'] = id
    qry = "SELECT * FROM`gov_schemes` WHERE id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_scheme.html" , val=res )


@app.route("/update_scheme", methods=['post'])
@login_required
def update_scheme():
    name = request.form["textfield"]
    details = request.form["textfield2"]

    qry="UPDATE `gov_schemes` SET `scheme_name`=%s, `details`=%s WHERE id=%s"
    iud(qry,(name,details, session['sid']))
    return '''<script>alert("Successfully edited");window.location="manage_scheme"</script>'''


@app.route("/add_scheme",methods=["post"])
@login_required
def add_scheme():
    return render_template("Admin/add_scheme.html")


@app.route("/manage_panchayath", methods=['GET'])
@login_required
def manage_panchayath():
    selected_district = request.args.get('district')  # Get the selected district from query params
    if selected_district:
        qry = "SELECT * FROM `panchayath` WHERE `district` = %s"
        res = selectall2(qry, (selected_district,))  # Filter by selected district
    else:
        qry = "SELECT * FROM `panchayath`"
        res = selectall(qry)  # No filter, get all Panchayaths

    districts = ['Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam',
                 'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram',
                 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod']  # List of districts

    return render_template("Admin/manage_panchayath.html", val=res, districts=districts,
                           selected_district=selected_district)


@app.route("/manage_scheme")
@login_required
def manage_scheme():
    qry = "SELECT * FROM `gov_schemes`"
    res = selectall(qry)
    # print(res) (just to check if the code works)
    return render_template("Admin/manage_scheme.html",val=res)


@app.route("/select_taluks")
@login_required
def select_taluks():
    dist = request.args.get("dist")
    qry = "SELECT DISTINCT(`taluk_name`) FROM `panchayath` WHERE `district`=%s"
    res = selectall2(qry, dist)
    return jsonify(res)


@app.route("/select_panchayath")
@login_required
def select_panchayath():
    taluk_name = request.args.get("taluk")
    qry = "SELECT * FROM `panchayath` WHERE `taluk_name`=%s"
    res = selectall2(qry, taluk_name)
    return jsonify(res)



@app.route("/view_report")
@login_required
def view_report():

    qry = "SELECT DISTINCT(`district`) FROM `panchayath` "
    res = selectall(qry)

    # qry="SELECT panchayath.name,reports.* FROM panchayath JOIN reports ON panchayath.l_id=reports.panchayath_id"
    # res2=selectall(qry)
    return render_template("Admin/view_report.html", val2=res)


@app.route("/filter_report", methods = ['post'])
@login_required
def filter_report():
    panchayath = request.form['pid']
    print(request.form)

    qry = "SELECT * FROM `reports` WHERE `panchayath_id`=%s"
    res = selectall2(qry, panchayath)

    qry = "SELECT DISTINCT(`district`) FROM `panchayath` "
    res2 = selectall(qry)

    return render_template("Admin/view_report.html", val=res, val2=res2)


@app.route("/add_food_details",methods=["post"])
@login_required
def add_food_details():
    return render_template("Admin/add_food_details.html")


@app.route("/insert_food", methods=["post"])
@login_required
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
@login_required
def delete_food():
    id=request.args.get('id')
    qry="DELETE FROM `food` WHERE id=%s"
    iud(qry,id)
    return '''<script>alert("Successfully Deleted");window.location="manage_food"</script>'''


@app.route("/edit_food")
@login_required
def edit_food():
    id = request.args.get('id')
    session['fid'] = id
    qry = "SELECT * FROM `food` WHERE id=%s"
    res = selectone(qry, id)
    return render_template("Admin/edit_food_details.html", val=res)


@app.route("/update_food", methods=['post'])
@login_required
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
@login_required
def manage_food():
    qry = "SELECT * FROM food"
    res = selectall(qry)
    return render_template("Admin/manage_food.html",val=res)


#panchayath==========================================================================
@app.route("/panchayath_home")
@login_required
def panchayath_home():
    return render_template("panchayath/panchayath_index.html")


@app.route("/manage_area")
@login_required
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
@login_required
def delete_area():
    id = request.args.get('id')
    qry = "DELETE FROM `area` WHERE id=%s"
    iud(qry, id)
    return '''<script>alert("Successfully deleted");window.location="manage_area"</script>'''


@app.route('/add_ashaworker', methods=['post'])
@login_required
def add_ashaworker():
    qry = "select * from area where pid=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/add_ashaworker.html", val=res)


@app.route("/insert_ashaworker", methods=['post'])
@login_required
def insert_ashaworker():
    try:
        name = request.form['textfield']
        post_office = request.form['textfield2']
        place = request.form['textfield3']
        pincode = request.form['textfield4']
        email = request.form['textfield5']
        phone = request.form['textfield6']
        area = request.form['select']
        username = request.form['textfield7']
        password = request.form['textfield8']


        qry = "SELECT * FROM `login` WHERE `username`=%s"
        res = selectone(qry, username)

        if res is None:

            qry = "INSERT INTO login VALUES(NULL,%s,%s,'ashaworker')"
            id = iud(qry, (username, password))

            qry = "INSERT INTO `ashaworker` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            iud(qry, (id,session['lid'],name, post_office, place, pincode, email, phone, area))
            return '''<script>alert("Successfully Added Ashaworker");window.location="manage_ashaworker"</script>'''
        else:
            return '''<script>alert("Username already exists");window.location="manage_ashaworker"</script>'''
    except:
        return '''<script>alert("Email or Phone already exists");window.location="manage_ashaworker"</script>'''


@app.route("/manage_reports")
@login_required
def manage_reports():
    qry = "SELECT * FROM `reports` WHERE panchayath_id = %s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_reports.html", val=res)


@app.route("/add_report", methods=['post'])
@login_required
def add_report():
    return render_template("panchayath/add_report.html")


@app.route("/insert_report", methods=['post'])
@login_required
def insert_report():
    report = request.files['file1']

    report_name = secure_filename(report.filename)
    report.save(os.path.join("static/uploads", report_name))

    qry = "INSERT `reports` VALUES(NULL,%s,%s,CURDATE())"
    iud(qry, (session['lid'], report_name))

    return '''<script>alert("Successfully added");window.location="manage_reports"</script>'''


@app.route("/delete_report")
@login_required
def delete_report():
    id = request.args.get('id')

    qry = "DELETE FROM `reports` WHERE `id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_reports"</script>'''


@app.route("/delete_ashaworker")
@login_required
def delete_ashaworker():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE id=%s"
    iud(qry, id)
    qry = "DELETE FROM `ashaworker` WHERE `l_id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_ashaworker"</script>'''


@app.route("/edit_ashaworker")
@login_required
def edit_ashaworker():
    id = request.args.get('id')
    session['aid'] = id
    qry = "SELECT * FROM `ashaworker` WHERE l_id= %s"
    res = selectone(qry, id)

    qry = "SELECT `area`.* FROM `area` where pid=%s"
    res1 = selectall2(qry, session['lid'])

    return render_template("panchayath/edit_ashaworker.html", val=res, val2=res1)


@app.route("/update_ashaworker", methods=['post'])
@login_required
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
@login_required
def add_program():
    return render_template("panchayath/add_program.html")


@app.route("/insert_program", methods=['post'])
@login_required
def insert_program():
    program = request.files['textfield']

    prgrm_name = secure_filename(program.filename)
    program.save(os.path.join("static/uploads", prgrm_name))

    name = request.form['name']
    details = request.form['details']
    date = request.form['details']

    qry = "INSERT `programs` VALUES(NULL,%s,%s,%s,%s,%s)"
    iud(qry, (session['lid'], name, prgrm_name, details, date))

    qry = "SELECT * FROM `user` JOIN `login` ON `user`.l_id=`login`.id WHERE `user`.panchayath_id=%s AND `login`.type='user'"
    res = selectall2(qry,session['lid'])
    print(res)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('ninocareproject@gmail.com', 'ioon ywiq cqkk bfaf')
        except Exception as e:
            print("Couldn't setup email!! " + str(e))
            return '''<script>alert("Could not setup email!"); window.location="/"</script>'''

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = 'ninocareproject@gmail.com'
        msg['To'] = email
        msg['Subject'] = 'New Panchayath Program'

        # Attach the text message
        body = "New program added. check it out."
        msg.attach(MIMEText(body, 'plain'))

        # Attach the PDF file
        pdf_filename = "static/uploads/"+prgrm_name
        try:
            with open(pdf_filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {pdf_filename}')
                msg.attach(part)
        except Exception as e:
            print("Couldn't attach the PDF file!! " + str(e))
            return '''<script>alert("Could not attach the PDF!"); window.location="/"</script>'''

        # Send the email
        try:
            gmail.send_message(msg)
            gmail.quit()
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
            return '''<script>alert("Couldn't send email!"); window.location="/"</script>'''

        return '''<script>alert("Email sent successfully!"); window.location="/"</script>'''

    for i in res:
        email = i['email']
        mail(email)

    return '''<script>alert("Success");window.location="manage_panchayath_program"</script>'''


@app.route("/delete_program")
@login_required
def delete_program():
    id = request.args.get('id')

    qry = "DELETE FROM `programs` WHERE `id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_panchayath_program"</script>'''


@app.route("/add_vaccine_details", methods=['post'])
@login_required
def add_vaccine_details():
    return render_template("panchayath/add_vaccine_details.html")


@app.route("/insert_vaccine_details", methods=['post'])
@login_required
def insert_vaccine_details():
    vaccine_name = request.form['textfield']
    details = request.form['textfield2']
    type = request.form['textfield3']
    date = request.form['date']

    email_content = request.form['email']

    qry = "INSERT INTO `vaccine` VALUES(NULL,%s,%s,%s,%s,%s)"
    iud(qry,(session['lid'],vaccine_name,details,date,type))

    qry = "SELECT * FROM `user` JOIN `login` ON `user`.l_id=`login`.id WHERE `user`.panchayath_id=%s AND `login`.type='user'"
    res = selectall2(qry, session['lid'])

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('ninocareproject@gmail.com', 'ioon ywiq cqkk bfaf')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText(email_content)
        print(msg)
        msg['Subject'] = 'Vaccination'
        msg['To'] = email
        msg['From'] = 'ninocareproject@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    for i in res:
        print(i)
        email = i['email']
        mail(email)

    return '''<script>alert("successfully added");window.location="manage_vaccination_details"</script>'''


@app.route("/delete_vaccination_details")
@login_required
def delete_vaccination_details():
    id = request.args.get('id')

    qry = "DELETE FROM `vaccine` WHERE `id`=%s"
    iud(qry, id)

    return '''<script>alert("Successfully deleted");window.location="manage_vaccination_details"</script>'''


@app.route("/edit_vaccination_details")
@login_required
def edit_vaccination_details():
    id = request.args.get('id')
    session['vid'] = id
    qry = "SELECT * FROM `vaccine` WHERE id=%s"
    res = selectone(qry, id)
    print(res)
    return render_template("panchayath/edit_vaccine_details.html", val=res)


@app.route("/update_vaccination_details", methods=['post'])
@login_required
def update_vaccination_details():
    vaccine_name = request.form['textfield']
    details = request.form['textfield2']
    type = request.form['textfield3']
    date = request.form['date']

    qry = "UPDATE `vaccine` SET `vaccine_name`=%s , `details`=%s, `type`=%s WHERE `id`=%s"
    iud(qry,(vaccine_name,details,type,session['vid']))

    return '''<script>alert("Successfully Edited");window.location="manage_vaccination_details"</script>'''


@app.route("/manage_ashaworker")
@login_required
def manage_ashaworker():
    qry = "SELECT `ashaworker`.*,`area`.area AS area_name FROM `ashaworker` JOIN `area` ON `ashaworker`.`area`=`area`.id WHERE `panchayath_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_ashaworker.html",val=res)


@app.route("/manage_panchayath_program")
@login_required
def manage_panchayath_program():
    qry="SELECT * FROM `programs` WHERE `panchayath_id`=%s"
    res=selectall2(qry,session['lid'])
    return render_template("panchayath/manage_panchayath_program.html", val=res)


@app.route("/view_food")
@login_required
def view_food():
    qry = "SELECT * FROM `food`"
    res = selectall(qry)
    return render_template("panchayath/view_food.html", val = res)


@app.route("/manage_vaccination_details")
@login_required
def manage_vaccination_details():
    qry="SELECT * FROM `vaccine` WHERE `panchayath_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/manage_vaccination_details.html", val=res)


@app.route("/view_mothers_details")
def view_mothers_details():
    qry = "SELECT * FROM `user` JOIN `login` ON `user`.l_id=`login`.id WHERE `user`.panchayath_id=%s AND `login`.type='user'"
    res = selectall2(qry, session['lid'])
    return render_template("panchayath/view_mothers_details.html", val=res)


@app.route("/panchayath_view_child_details")
@login_required
def panchayath_view_child_details():
    id = request.args.get('id')
    qry = "SELECT * FROM `child` WHERE `parent_id`=%s"
    res = selectall2(qry,id)
    return render_template("panchayath/view_child_details.html", val=res)


#ashaworker============================================================================
@app.route("/ashaworker_home")
@login_required
def ashaworker_home():
    return render_template("Ashaworker/ashaworker_index.html")


@app.route("/add_child", methods=['post'])
@login_required
def add_child():
    qry = "SELECT * FROM `user` JOIN `ashaworker` ON `user`.`area` = `ashaworker`.area WHERE `ashaworker`.l_id=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Ashaworker/add_child.html", val=res)


@app.route("/insert_child", methods=['post'])
@login_required
def insert_child():
    parent = request.form['select']
    name = request.form['textfield']
    gender = request.form['gender']
    dob = request.form['textfield2']

    qry = "INSERT INTO `child` VALUES(NULL, %s, %s, %s, %s)"
    iud(qry,(parent, name, gender, dob))

    return '''<script>alert("Successfully added");window.location="manage_child_details"</script>'''


@app.route("/delete_child")
@login_required
def delete_child():
    id = request.args.get('id')
    qry = "DELETE FROM `child` WHERE id =%s"
    iud(qry, id)
    return '''<script>alert("Successfully added");window.location="manage_child_details"</script>'''



@app.route("/manage_child_details")
@login_required
def manage_child_details():
    qry = "SELECT `user`.name as pname, `child`.* FROM `child` JOIN `user` ON `child`.`parent_id`=`user`.l_id JOIN `ashaworker` ON `user`.area=`ashaworker`.area WHERE `ashaworker`.`l_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Ashaworker/manage_child_details.html", val=res)


@app.route("/manage_users")
@login_required
def manage_users():
    qry = "SELECT `user`.* FROM `user` JOIN `ashaworker` ON `user`.area=`ashaworker`.area where ashaworker.l_id=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Ashaworker/manage_users.html", val=res)


@app.route("/add_user", methods=['post'])
@login_required
def add_user():
    return render_template("/Ashaworker/add_user.html")


@app.route("/insert_code", methods=['post'])
@login_required
def insert_code():
    try:
        name = request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        ph_no=request.form['textfield5']
        email=request.form['textfield6']
        pregnant=request.form['select2']
        number_of_child=request.form['child']
        latitude=request.form['textfield7']
        longitude=request.form['textfield8']
        username=request.form['textfield9']
        password=request.form['textfield10']

        qry = "SELECT * FROM `login` WHERE `username`=%s"
        res = selectone(qry, username)

        if res is None:

            qry = "INSERT INTO login VALUES(NULL,%s,%s,'user')"
            id = iud(qry,(username,password))

            qry = "SELECT * FROM  `ashaworker` WHERE l_id=%s"
            res = selectone(qry, session['lid'])

            qry = "INSERT INTO USER VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            iud(qry,(id, res['panchayath_id'], name, place, post, pin, res['area'], ph_no, email, number_of_child, pregnant, latitude, longitude))

            return '''<script>alert("Successfully Added");window.location="/manage_users"</script>'''

        else:
            return '''<script>alert("Username already exists");window.location="/manage_users"</script>'''
    except:
        return '''<script>alert("Email or phone already exists");window.location="/manage_users"</script>'''


@app.route("/verify_users")
@login_required
def verify_users():
    qry = "SELECT `user`.* FROM `user` JOIN `ashaworker` ON `user`.area=`ashaworker`.area JOIN `login` ON `user`.l_id=`login`.id WHERE `login`.type='pending' and ashaworker.l_id=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Ashaworker/verify_users.html", val=res)


@app.route("/delete_user")
@login_required
def delete_user():
    id = request.args.get('id')
    qry = "delete from login where id=%s"
    iud(qry, id)
    qry = "DELETE FROM `user` WHERE l_id=%s"
    iud(qry, id)
    return '''<script>alert("Deleted");window.location="manage_users"</script>'''


@app.route("/accept_user")
@login_required
def accept_user():
    id = request.args.get('id')
    qry = "UPDATE `login` SET TYPE='user' WHERE id=%s"
    iud(qry, id)
    return '''<script>alert("Accepted");window.location="verify_users"</script>'''


@app.route("/reject_user")
@login_required
def reject_user():
    id = request.args.get('id')
    qry = "UPDATE `login` SET TYPE='rejected' WHERE id=%s"
    iud(qry, id)
    return '''<script>alert("Rejected");window.location="verify_users"</script>'''


@app.route("/view_programs_schemes")
@login_required
def view_programs_schemes():
    return render_template("Ashaworker/view_programs_schemes.html")


#User===========================================================================
@app.route("/user_home")
@login_required
def user_home():
    return render_template("User/user_index.html")


@app.route("/view_food_details")
@login_required
def view_food_details():
    qry = "SELECT * FROM `food`"
    res = selectall(qry)
    return render_template("User/view_food_details.html", val=res)


@app.route("/view_programs")
@login_required
def view_programs():
    qry = "SELECT * FROM `programs` JOIN `user` ON `programs`.`panchayath_id`=`user`.`panchayath_id` WHERE `user`.`l_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("User/view_programs.html", val=res)


@app.route("/view_schemes")
@login_required
def view_schemes():
    qry = "SELECT * FROM `gov_schemes`"
    res = selectall(qry)
    return render_template("User/view_scheme_card.html", val=res)


@app.route("/view_scheme_details")
@login_required
def view_scheme_details():
    id = request.args.get('id')
    qry = "SELECT * FROM `gov_schemes` where id=%s"
    res = selectone(qry, id)
    return render_template("User/view_scheme_details.html", val=res)


@app.route("/ashaworker_view_programs")
@login_required
def ashaworker_view_programs():
    qry = "SELECT * FROM `programs` JOIN `ashaworker` ON `programs`.`panchayath_id`=`ashaworker`.`panchayath_id` WHERE `ashaworker`.`l_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template("Ashaworker/view_programs.html", val=res)


@app.route("/ashaworker_view_schemes")
@login_required
def ashaworker_view_schemes():
    qry = "SELECT * FROM `gov_schemes`"
    res = selectall(qry)
    return render_template("Ashaworker/view_schemes.html", val=res)


@app.route("/view_vaccine_details")
@login_required
def view_vaccine_details():
    return render_template("User/view_vaccine_details.html")


@app.route("/view_vaccine_details2", methods=['post'])
@login_required
def view_vaccine_details2():
    type = request.form['select']

    qry = "SELECT * FROM `vaccine` JOIN `user` ON `vaccine`.`panchayath_id`=`user`.`panchayath_id` WHERE  `vaccine`.`type`=%s and user.l_id=%s"
    res = selectall2(qry, (type,session['lid']))
    return render_template("User/view_vaccine_details.html", val=res, t = type)


@app.route("/forgot_password")
def forgot_password():
    return  render_template("forgot_password.html")

@app.route("/forgot_password_otp", methods=['post'])
def forgot_password_otp():
    type= request.form['type']
    gmail = request.form['textfield']
    otp = random.randint(1000, 9999)
    session['otp'] = str(otp)

    def mail(email):
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('ninocareproject@gmail.com', 'ioon ywiq cqkk bfaf')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText(str(otp))
        print(msg)
        msg['Subject'] = 'Vaccination'
        msg['To'] = email
        msg['From'] = 'ninocareproject@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:
            print("COULDN'T SEND EMAIL", str(e))
        return '''<script>alert("SEND"); window.location="/"</script>'''

    if type == "Ashaworker":
        qry = "SELECT * FROM `ashaworker` WHERE `email`=%s"
        res = selectone(qry, gmail)


        if res is None:
            return '''<script>alert("Invalid Email Address"); window.location="/"</script>'''
        else:
            session['id'] = res['l_id']
            mail(gmail)
            return render_template("enter_otp.html")

    elif type == "User":
        qry = "SELECT * FROM `user` WHERE `email`=%s"
        res = selectone(qry, gmail)


        if res is None:
            return '''<script>alert("Invalid Email Address"); window.location="/"</script>'''
        else:
            session['id'] = res['l_id']
            mail(gmail)
            return render_template("enter_otp.html")
    else:
        qry = "SELECT * FROM `panchayath` WHERE `email`=%s"
        res = selectone(qry, gmail)


        if res is None:
            return '''<script>alert("Invalid Email Address"); window.location="/"</script>'''
        else:
            session['id'] = res['l_id']
            mail(gmail)
            return render_template("enter_otp.html")


@app.route("/verify_otp", methods=['post'])
def verify_otp():
    otp = request.form['textfield']

    if otp == session['otp']:
        return render_template("new_password.html")
    else:
        return '''<script>alert("OTP missmatch"); window.location="/"</script>'''


@app.route("/update_password", methods=['post'])
def update_password():
    new_password = request.form['textfield']
    qry = "UPDATE `login` SET PASSWORD = %s where id=%s"
    iud(qry,(new_password, session['id']))
    return '''<script>alert("Password changed successfully"); window.location="/"</script>'''


def send_vaccine_notification():
    try:
        print("=================================")
        qry = "SELECT * FROM `vaccine` WHERE DATEDIFF(`date`, CURDATE()) IN (1)"
        res = selectall(qry)

        print("===============", res)

        for i in res:
            qry = "SELECT * FROM `user` WHERE `panchayath_id` = %s AND `l_id` NOT IN (SELECT `l_id` FROM `vaccine_notified_users` where vaccine_id=%s)"
            res2 = selectall2(qry, (i['panchayath_id'],i['id']))

            print("=============res2", res2)

            for j in res2:
                qry = "INSERT INTO `vaccine_notified_users` VALUES(NULL, %s, %s, CURDATE())"
                iud(qry, (j['l_id'], i['id']))

                subject = i['vaccine_name']
                message = i['details']
                email = j['email']
                send_email(email, message, subject)

        qry = "SELECT * FROM `programs` WHERE DATEDIFF(`date`, CURDATE()) IN (1)"
        res = selectall(qry)

        for i in res:
            print("programs================")
            qry = "SELECT * FROM `user` WHERE `panchayath_id` = %s AND `l_id` NOT IN (SELECT `l_id` FROM `program_notified_users` where program_id=%s)"
            res2 = selectall2(qry, (i['panchayath_id'], i['id']))

            print("=============res2", res2)

            for j in res2:
                qry = "INSERT INTO `program_notified_users` VALUES(NULL, %s, %s, CURDATE())"
                iud(qry, (j['l_id'], i['id']))

                subject = i['program name']
                message = i['details']
                email = j['email']
                send_email(email, message, subject)



    except Exception as e:
        print(str(e))

def send_email(email, message, subject):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('ninocareproject@gmail.com', 'ioon ywiq cqkk bfaf')  # Secure this in production!!
    except Exception as e:
        print(f"Couldn't setup email!! {e}")
        return

    msg = MIMEText(str(message))
    msg['Subject'] = subject
    msg['To'] = email
    msg['From'] = 'ninocareproject@gmail.com'

    try:
        gmail.send_message(msg)
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"COULDN'T SEND EMAIL to {email}: {e}")
    finally:
        gmail.quit()

# Initialize the scheduler
scheduler = BackgroundScheduler()

def initialize_scheduler():
    # Schedule the task to run every 1 minute
    scheduler.add_job(func=send_vaccine_notification, trigger="interval", minutes=1)
    scheduler.start()


@app.route("/chat_with_gemini")
@login_required
def chat_with_gemini():
    return render_template("User/chat_with_ai.html")


@app.route('/gemini_chat', methods=['POST'])
@login_required
def gemini_chat():
    # Get the message sent by the user
    user_message = request.json.get('message')

    if user_message:
        # Generate AI response using Gemini AI
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_message)

        # Return AI's response to the frontend
        return jsonify({'reply': response.text})

    return jsonify({'reply': 'Error: No message received'}), 400


@app.route("/edit_user")
@login_required
def edit_user():
    id = request.args.get('id')
    session['user_id'] = id
    qry = "SELECT * FROM `user` WHERE l_id=%s"
    res = selectone(qry, id)

    return render_template("Ashaworker/edit_user.html", val=res)



@app.route("/edit_code", methods=['post'])
@login_required
def edit_code():
    try:
        name = request.form['textfield']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        ph_no=request.form['textfield5']
        email=request.form['textfield6']
        pregnant=request.form['select2']
        number_of_child=request.form['child']
        latitude=request.form['textfield7']
        longitude=request.form['textfield8']

        qry = "UPDATE `user` SET `name`=%s, `place`=%s, `post`=%s, `pin`=%s, `ph_no`=%s, email=%s, `no_of_child`=%s, `type`=%s, `latitude`=%s, `longitude`=%s WHERE `l_id`=%s"
        iud(qry,( name, place, post, pin, ph_no, email, number_of_child, pregnant, latitude, longitude, session['user_id']))

        return '''<script>alert("Successfully Edited");window.location="/manage_users"</script>'''

    except:
        return '''<script>alert("Email or phone already exists");window.location="/manage_users"</script>'''



if __name__ == "__main__":
    initialize_scheduler()  # Start the scheduler when the app starts
    try:
        app.run(debug=True)
    finally:
        scheduler.shutdown()  # Shut down the scheduler when the app is stopped