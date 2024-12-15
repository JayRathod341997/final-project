import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email (you need to implement the actual email logic)
def send_email(to_email, subject, body):
    from_email = "your_email@gmail.com"  # Replace with your email address
    password = "your_email_password"  # Replace with your email password or app-specific password

    # Setup email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)

    # Prepare the email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Appointment Booking Function
def book_appointment():
    st.subheader("📞 Book an Appointment with a Specialist")

    # Doctor information
    doctors = [
        {"name": "Dr. John Doe", "specialization": "Neurosurgeon",
            "contact": "+1 555-123-4567", "email": "doctor1@example.com"},
        {"name": "Dr. Jane Smith", "specialization": "Neurologist",
            "contact": "+1 555-987-6543", "email": "doctor2@example.com"},
        {"name": "Dr. Robert Brown", "specialization": "Radiologist",
            "contact": "+1 555-456-7890", "email": "doctor3@example.com"}
    ]

    # Display doctor information
    doctor_options = [doctor["name"] for doctor in doctors]
    selected_doctor = st.selectbox("👨‍⚕️ Select a doctor", doctor_options)

    # Define available time slots
    time_slots = ["10:00 AM", "11:00 AM", "3:00 PM", "4:00 PM", "5:00 PM", "7:00 PM"]

    # Appointment booking form
    with st.form(key="appointment_form"):
        name = st.text_input("👤 Your Name")
        email = st.text_input("📧 Your Email Address")
        contact = st.text_input("📞 Your Contact Number")
        city = st.text_input("🏙️ City")
        state = st.text_input("🌆 State")
        country = st.text_input("🌍 Country")
        date = st.date_input("📅 Preferred Appointment Date")
        selected_time_slot = st.selectbox("⏰ Select a time slot", time_slots)
        message = st.text_area("💬 Message (optional)")

        # Submit button
        submit_button = st.form_submit_button("📤 Submit Appointment Request")

        if submit_button:
            # Find selected doctor's details
            doctor = next(doctor for doctor in doctors if doctor["name"] == selected_doctor)
            doctor_email = doctor["email"]

            subject = "🩺 New Appointment Request"
            body_to_doctor = f"""
            Appointment Request from {name} ({email}):
            🗓️ Appointment Date: {date}
            Time Slot: {selected_time_slot}
            Message: {message}
            """
            # Send email to doctor
            send_email(doctor_email, subject, body_to_doctor)

            st.success(f"✅ Appointment request sent! You will receive a confirmation email shortly. 📧")
