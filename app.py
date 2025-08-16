from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Email configuration
EMAIL_ADDRESS = "sheikh.maaz1308@gmail.com"
EMAIL_PASSWORD = "uxuharazqjdpvepc"
RECIPIENT_EMAIL = "sheikh.maaz1308@gmail.com"

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Contact Form Submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'subject', 'message']
        if not all(key in data for key in required_fields):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"New Contact Form Submission - {data['subject']}"
        
        # Get current date and time
        now = datetime.now()
        submission_time = now.strftime("%B %d, %Y at %I:%M %p")
        
        # Create HTML email body
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 15px; text-align: center; border-bottom: 1px solid #e9ecef; }}
                    .contact-details {{ margin: 20px 0; }}
                    .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #e9ecef; font-size: 0.9em; color: #6c757d; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>New Contact Form Submission</h2>
                        <p>Submitted on {submission_time}</p>
                    </div>
                    
                    <div class="contact-details">
                        <h3>Contact Information</h3>
                        <p><strong>Name:</strong> {data['name']}</p>
                        <p><strong>Phone:</strong> {data['phone']}</p>
                        <p><strong>Email:</strong> {data['email']}</p>
                        <p><strong>Subject:</strong> {data['subject']}</p>
                        
                        <h3>Message</h3>
                        <p>{data['message']}</p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated notification from Jiffy Logistics website.</p>
                        <p>© {now.year} Jiffy Logistics. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return jsonify({"success": True, "message": "Your message has been sent successfully!"})
    
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({"success": False, "error": "Failed to send message. Please try again later."}), 500

# Quote Form Submission
@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fullName', 'phone', 'serviceType', 'pickupAddress', 
                          'pickupCity', 'dropAddress', 'dropCity']
        if not all(key in data for key in required_fields):
            missing = [field for field in required_fields if field not in data]
            return jsonify({
                "success": False, 
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400
        
        # Format additional services
        additional_services = data.get('additionalServices', [])
        if isinstance(additional_services, str):
            additional_services = [additional_services]
        services_list = ", ".join(additional_services) if additional_services else "None selected"
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"New Quote Request - {data['serviceType']}"
        
        # Get current date and time
        now = datetime.now()
        submission_time = now.strftime("%B %d, %Y at %I:%M %p")
        
        # Create HTML email body
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 15px; text-align: center; border-bottom: 1px solid #e9ecef; }}
                    .customer-info, .shipment-details {{ margin: 20px 0; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #f8f9fa; }}
                    .footer {{ margin-top: 20px; padding-top: 10px; border-top: 1px solid #e9ecef; font-size: 0.9em; color: #6c757d; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>New Quote Request</h2>
                        <p>Submitted on {submission_time}</p>
                    </div>
                    
                    <div class="customer-info">
                        <h3>Customer Information</h3>
                        <p><strong>Name:</strong> {data['fullName']}</p>
                        <p><strong>Phone:</strong> {data['phone']}</p>
                        <p><strong>Email:</strong> {data.get('email', 'Not provided')}</p>
                    </div>
                    
                    <div class="shipment-details">
                        <h3>Shipment Details</h3>
                        <p><strong>Service Type:</strong> {data['serviceType']}</p>
                        
                        <h4>Pickup Information</h4>
                        <p><strong>Address:</strong> {data['pickupAddress']}</p>
                        <p><strong>City:</strong> {data['pickupCity']}</p>
                        
                        <h4>Delivery Information</h4>
                        <p><strong>Address:</strong> {data['dropAddress']}</p>
                        <p><strong>City:</strong> {data['dropCity']}</p>
                        
                        <h4>Cargo Details</h4>
                        <p><strong>Type:</strong> {data.get('cargoType', 'Not specified')}</p>
                        <p><strong>Weight:</strong> {data.get('weight', 'Not specified')} kg</p>
                        <p><strong>Dimensions:</strong> {data.get('dimensions', 'Not specified')}</p>
                        
                        <h4>Additional Services</h4>
                        <p>{services_list}</p>
                        
                        <h4>Additional Notes</h4>
                        <p>{data.get('additionalNotes', 'No additional notes')}</p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated notification from Jiffy Logistics website.</p>
                        <p>© {now.year} Jiffy Logistics. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML content
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return jsonify({"success": True, "message": "Your quote request has been submitted successfully!"})
    
    except Exception as e:
        print(f"Error processing quote form: {str(e)}")
        return jsonify({"success": False, "error": "Failed to submit quote. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)