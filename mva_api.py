from PIL import Image, ImageDraw, ImageFont
import socket
import sys
from flask import Flask,jsonify,request
from PyQt5.QtWidgets import QApplication
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint
import requests
app=Flask(__name__)

#socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
dynamic_ipv4=str(s.getsockname()[0])
s.close()
print(dynamic_ipv4)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = "0.0.0.0"
port = 5004

server.bind((ip,port))
server.listen(1)

connection, address = server.accept()

#api route with parameters
@app.route("/")
def call_function():
	if "distance" and "position" and "dpi" and "chart_type" in request.args:
		distance=float(request.args['distance'])
		position=int(request.args['position'])
		dpi=int(request.args['dpi'])
		chart_type=str(request.args['chart_type'])
		letter,length_in_inch,accuity=render_letter(distance=distance,position=position,dpi=dpi,chart_type=chart_type) #initiates the process
		if(chart_type=='hindi'):
			return jsonify({'img_url':'http://{dynamic_ipv4}:1234/static/images/devnagri/{letter}.png'.format(dynamic_ipv4=dynamic_ipv4,letter=letter),'length_in_inch':length_in_inch,'accuity':accuity,'letter':letter})
		elif(chart_type=='english'):
			return jsonify({'img_url':'http://{dynamic_ipv4}:1234/static/images/{letter}.jpg'.format(dynamic_ipv4=dynamic_ipv4,letter=letter),'length_in_inch':length_in_inch,'accuity':accuity,'letter':letter}) #english
		else: #type landlot c
			return jsonify({'img_url':'http://{dynamic_ipv4}:1234/static/images/land/{letter}.png'.format(dynamic_ipv4=dynamic_ipv4,letter=letter),'length_in_inch':length_in_inch,'accuity':accuity,'letter':letter})
	else:
		return jsonify({'status':'input something'})

def calculate_size(distance,accuity): #accuity : 6/6,6/12  #distance in m from the user

	return distance*0.1454*(1/accuity) #in cm

def render_letter(position=0,dpi=352,distance=6,chart_type='english'):
	if chart_type=='english':
		chart_letter=['E','F','P','T','O','Z','L','P','E','D','P','E','C','F','D','E','D','F','C','Z','P','F','E','L','O','P','Z','D','D','E','F','P','O','T','E','C']
		accuit=[0.10,0.20,0.20,0.28,0.28,0.28,0.40,0.40,0.40,0.40,0.50,0.50,0.50,0.50,0.50,0.66,0.66,0.66,0.66,0.66,0.66,0.8,0.8,0.8,0.8,0.8,0.8,0.8,1,1,1,1,1,1,1,1]
		letter=chart_letter[position]
		# print(letter)
		length_in_cm=calculate_size(distance,accuit[position])
		length_in_inch=length_in_cm/2.54
		print(length_in_cm,"cm size to be displayed",accuit[position],"is the acuity",dpi,"is the dpi",distance,"is the distance")
		# dpix=get_dpi_current_device()
		side=round((length_in_cm/2.54)*dpi)
		# # print(side)
		# # print(side*2.2)

		# img = Image.new('RGB',(side,side), color = (255, 255, 255))
		 
		# fnt = ImageFont.truetype('D:\Downloads\snellenmk-optotype-font\snellen-mk\Snellen.ttf', side)
		# d = ImageDraw.Draw(img)
		# d.text((0,0), letter, font=fnt, fill=(0, 0, 0),anchor=None) 
		 
		# img.save('static/images/{letter}.jpg'.format(letter=letter))
		imgUrl=str(position)
		imgUrl='http://{dynamic_ipv4}:1234/static/images/{letter}.jpgrandom6{length_in_inch}'.format(dynamic_ipv4=dynamic_ipv4,letter=letter,length_in_inch=length_in_inch)
		print(imgUrl)
		url = imgUrl.encode('utf-8')
		connection.send(len(url).to_bytes(2,byteorder='big'))
		connection.send(url)
		return letter,length_in_inch,accuit[position]

	elif chart_type=='landlot_c':
		chart_letter=['down','right','left','left','down','up','right','right','up','down','left','down','down','up','left','down','right','up','left','right','up','down','right','down','up','right','left','left','up','left','down','right','right','left','up','left']
		print(len(chart_letter),"landolt_c")
		accuit=[0.10,0.20,0.20,0.28,0.28,0.28,0.40,0.40,0.40,0.40,0.50,0.50,0.50,0.50,0.50,0.66,0.66,0.66,0.66,0.66,0.66,0.8,0.8,0.8,0.8,0.8,0.8,0.8,1,1,1,1,1,1,1,1]
		# accuit=[20/125,20/125,20/125,20/100,20/100,20/100,20/100,20/80,20/80,20/80,20/80,20/80,20/63,20/63,20/63,20/63,20/63,20/50,20/50,20/50,20/50,20/50,20/40,20/40,20/40,20/40,20/40,20/32,20/32,20/32,20/32,20/32,20/25,20/25,20/25,20/25,20/25,20/20,20/20,20/20,20/20,20/20]
		# print(accuit)
		letter=chart_letter[position]
		length_in_cm=calculate_size(distance,accuit[position])
		length_in_inch=length_in_cm/2.54
		print(length_in_cm,"cm size to be displayed",accuit[position],"is the acuity",dpi,"is the dpi",distance,"is the distance")
		# dpix=get_dpi_current_device()
		side=round((length_in_cm/2.54)*dpi)
		
		imgUrl='http://{dynamic_ipv4}:1234/static/images/land/{letter}.pngrandom6{length_in_inch}'.format(dynamic_ipv4=dynamic_ipv4,letter=letter,length_in_inch=length_in_inch)
		print(imgUrl)
		url = imgUrl.encode('utf-8')
		connection.send(len(url).to_bytes(2,byteorder='big'))
		connection.send(url)
		return letter,length_in_inch,accuit[position]
	else: # it is in hindi
		chart_letter=['ra','ta','pa','na','ga','taa','ma','ta','ra','pha','ga','naaa','tha','ta','ra','pha','na','ra','va','ma','taa','na','saa','ma','ta','ra','ta','va','ma','saa']
		print(len(chart_letter))
		accuit=[0.10,6/36,6/36,6/24,6/24,6/24,6/18,6/18,6/18,6/18,6/12,6/12,6/12,6/12,6/12,6/9,6/9,6/9,6/9,6/9,6/6,6/6,6/6,6/6,6/6,6/5,6/5,6/5,6/5,6/5]
		letter=chart_letter[position]
		length_in_cm=calculate_size(distance,accuit[position])
		length_in_inch=length_in_cm/2.54
		print(length_in_cm,"cm size to be displayed",accuit[position],"is the acuity",dpi,"is the dpi",distance,"is the distance")
		# dpix=get_dpi_current_device()
		side=round((length_in_cm/2.54)*dpi)
		
		imgUrl='http://{dynamic_ipv4}:1234/static/images/devnagri/{letter}.pngrandom6{length_in_inch}'.format(dynamic_ipv4=dynamic_ipv4,letter=letter,length_in_inch=length_in_inch)
		print(imgUrl)
		url = imgUrl.encode('utf-8')
		connection.send(len(url).to_bytes(2,byteorder='big'))
		connection.send(url)
		return letter,length_in_inch,accuit[position]

#Getting Device DPI
def get_dpi_current_device():
	app = QApplication(sys.argv)
	screen = app.screens()[0]
	dpi = screen.physicalDotsPerInch()
	return dpi

#Sending Email with Total Score
@app.route('/total_score')
def send_mail():
	print("Api called")

	if ('name' in request.args and 'email' in request.args and 'distance' in request.args and 'age' in request.args and 'mobile_no' in request.args and 'gender' in request.args and 'chart_type' in request.args and 'left_eye' in request.args and 'right_eye' in request.args):
		print("changes made")
		name=str(request.args['name'])
		email=str(request.args['email'])
		age=str(request.args['age'])
		mobile_no=str(request.args['mobile_no'])
		gender=str(request.args['gender'])
		chart_type=str(request.args['chart_type'])
		left_eye=str(request.args['left_eye'])
		right_eye=str(request.args['right_eye'])
		distance=float(request.args['distance'])
		left_eye=left_eye.split('-')
		right_eye=right_eye.split('-')
		# print(left_eye,right_eye)
		if(len(left_eye)==3):
			left_eye='{numerator}/{denominator}-{minus}'.format(numerator=left_eye[0],denominator=left_eye[1],minus=left_eye[2])
		elif(len(left_eye)==2):
			left_eye='{numerator}/{denominator}'.format(numerator=left_eye[0],denominator=left_eye[1])
		else:
			left_eye = "please consult a doctor"
		if(len(right_eye)==3):
			right_eye='{numerator}/{denominator}-{minus}'.format(numerator=right_eye[0],denominator=right_eye[1],minus=right_eye[2])
		elif(len(right_eye)==2):
			right_eye='{numerator}/{denominator}'.format(numerator=right_eye[0],denominator=right_eye[1])
		else:
			right_eye = "please consult a doctor."


		# print(name,email,age,mobile_no,gender,chart_type,left_eye,right_eye)
		if(email==''):
			print("Email is not provided")
			return jsonify({'status':'success'})
			
		subject = "Acuity Result"
		body = '''
				Name:{name}
				Age:{age}
				Gender:{gender}
				Testing Distance:{distance}
				Chart Type:{chart_type}
				Left Eye Score:{left_eye}
				Right Eye Score:{right_eye}
				Thank You for visiting Us
				Team MVA-3
				'''.format(name=name,distance=distance,age=age,gender=gender,chart_type=chart_type,left_eye=left_eye,right_eye=right_eye)
		pprint(body)
		receiver_email = email
		sender_email = "chawdakartik1@gmail.com"
		password = 'dhwani01101999'

		# Create a multipart message and set headers
		message = MIMEMultipart()
		message["From"] = sender_email
		message["To"] = receiver_email
		message["Subject"] = subject
		message["Bcc"] = receiver_email  # Recommended for mass emails
		# Add body to email
		message.attach(MIMEText(body, "plain"))
		text = message.as_string()

# Log in to server using secure context and send email
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		    server.login(sender_email, password)
		    server.sendmail(sender_email, receiver_email, text)
		
		# insert_into_db(name,email,age,mobile_no,gender,chart_type,left_eye,right_eye,distance)
		send_sms(msg="Hello your left eye acuity is {left_eye} and your right eye acuity is {right_eye}".format(left_eye=left_eye,right_eye=right_eye))
		return jsonify({'status':'success'})
	else:
		print("All parameters not received in mail function")
		return jsonify({'status':'failed'})

if __name__=='__main__':
	app.run(debug=False,port=1234,host='0.0.0.0',threaded=True)