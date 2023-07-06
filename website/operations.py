from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from . import query_obj
from . import helpers

operations = Blueprint('operations', __name__)

# Route to the single record display page
@operations.route("/single-record-display", methods=["GET", "POST"])
def single_record_display():
	# Check if the user is logged in
	if 'is_login' not in session:
		return render_template('404.html')
	
	# Fetch the session variables
	data = session['data']
	print(session['page'])
	if request.method == "POST":
		print("what")
		val = request.form.get('idea_operation')
		print(val)
		
	# Render the single record display page with the data from the session variable
	return render_template("single_record_display.html", data=data)
