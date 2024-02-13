import io
import os
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ScholarshipApplication, VendorApplication
from reportlab.lib.pagesizes import letter


from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage

@login_required
def generate_scholarship_pdf(request, application_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    application = ScholarshipApplication.objects.get(id=application_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Scholarship_Application_{application_id}.pdf"'
    
    p = canvas.Canvas(response)
    y = 800  # Start from the top of the page.
    x = 50   # Margin from the left.

    # Adjust the line height as needed
    line_height = 14

    # Draw each field.
    fields = [
        f"First Name: {application.first_name}",
        f"Last Name: {application.last_name}",
        f"Phone Number: {application.phone_number}",
        f"Email: {application.email}",
        f"Date of Birth: {application.date_of_birth.strftime('%Y-%m-%d') if application.date_of_birth else 'N/A'}",
        f"Education Level: {application.get_education_level_display()}",
        f"Gender: {application.get_gender_display()}",
        f"Business Name: {application.business_name}",
        f"Business Description: {application.business_description}",
        f"Video Link: {application.video_link}",
        # For the PDF field, you might want to display a message rather than the URL
        "PDF: Attached",
        f"SQuestion1: {application.squestion1}",
        f"SQuestion2: {application.squestion2}",
        f"SQuestion3: {application.squestion3}",
    ]

    for field in fields:
        p.drawString(x, y, field)
        y -= line_height  # Move down for the next line.

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

@login_required
def generate_vendor_pdf(request, application_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    application = VendorApplication.objects.get(id=application_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Vendor_Application_{application_id}.pdf"'
    
    p = canvas.Canvas(response)
    y = 800  # Start from the top of the page for text.
    y_image = 650  # Start position for the image.
    x = 50   # Margin from the left for text.
    x_image = 50  # Margin from the left for the image.

    # Adjust the line height as needed
    line_height = 14

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Get the dimensions of the page
    y = height - 50  # Start from the top of the page for text
    x_text = 300  # X position for text, assuming the image is on the left side

        # Draw the logo
    if application.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, application.logo.name)
        logo_height = 100  # Or calculate the height based on the width to maintain aspect ratio
        logo_width = 200  # Adjust as necessary
        x_image = 50  # Margin from the left for the image
        y_image = height - 50 - logo_height  # Position the top of the image at the same y as text
        p.drawImage(logo_path, x_image, y_image, width=logo_width, height=logo_height, mask='auto')

    # Adjust the y position for text start after the image
    y_text_start = y_image - 15  # Start the text below the image

    # Draw each field.
    fields = [
        f"Logo: Attached",
        f"First Name: {application.first_name}",
        f"Last Name: {application.last_name}",
        f"Phone Number: {application.phone_number}",
        f"VQuestion1: {application.vquestion1}",
        f"VQuestion2: {application.vquestion2}",
        f"Product Suite Overview: {application.product_suite_overview}",
        f"URL/API Details: {application.url_api_details}",
        f"Partnership Outcome: {application.partnership_outcome}",
        f"Business Name: {application.business_name}",
        f"Business Description: {application.business_desciption}",
        f"Website Link: {application.website_link}",        
        f"Business Proposal: " + (application.business_proposal.name if application.business_proposal else "Not provided"),
        "Fee Structure: " + (application.fee_structure.name if application.fee_structure else "Not provided"),
    ]


        # Check if the logo exists and draw it.
    if application.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, application.logo.name)
        p.drawImage(logo_path, x_image, y_image, width=200, height=100, mask='auto')  # You may need to adjust the width and height.

        # Draw the text fields below the image
    for field in fields:
        p.drawString(x_text, y_text_start, field)
        y_text_start -= line_height  # Move down for the next line

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def send_status_email(application, feedback=None):
    subject = 'Application Status Update'
    message = f'Your application status has been updated to: {application.status}.'
    if feedback:
        message += f"\n\nFeedback: {feedback}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [application.user.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list
    )

    if isinstance(application, ScholarshipApplication):
        pdf = generate_scholarship_pdf(application)
        email.attach(f'Scholarship_Application_{application.id}.pdf', pdf.read(), 'application/pdf')
    elif isinstance(application, VendorApplication):
        pdf = generate_vendor_pdf(application)
        email.attach(f'Vendor_Application_{application.id}.pdf', pdf.read(), 'application/pdf')

    email.send()