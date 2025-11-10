import flet as ft
from typing import Any, Dict, List
import re
from datetime import datetime

def main(page: ft.Page) -> None:
    """Main entry point for the booking system."""
    # =========================
    # Window configuration
    # =========================
    page.title = "Booking System"
    page.window_width = 500
    page.window_height = 700
    page.window_resizable = False

    page.theme_mode = "light"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # =========================
    # Local data storage
    # =========================
    records: List[Dict[str, Any]] = []

    # =========================
    # THEME TOGGLE
    # =========================
    def toggle_theme(e: ft.ControlEvent) -> None:
        """Switch between light and dark modes."""
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        theme_button.text = (
            "🌙 Dark Mode" if page.theme_mode == "light" else "☀️ Light Mode"
        )
        page.update()

    theme_button: ft.TextButton = ft.TextButton("🌙 Dark Mode", on_click=toggle_theme)

    # Helper function for navigation
    def navigate_to(target: ft.Control) -> None:
        """Clears page and navigates to a new form/page."""
        page.controls.clear()
        page.add(theme_button, target)
        page.update()

    # =========================
    # REGISTRATION FORM
    # =========================
    name = ft.TextField(label="Full Name", hint_text="Enter your full name", width=300)
    email = ft.TextField(label="Email", hint_text="example@mail.com", width=300)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300)
    contact = ft.TextField(label="Contact Number", hint_text="09XXXXXXXXX", width=300)
    gender = ft.Dropdown(
        label="Gender",
        options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female"), ft.dropdown.Option("Other")],
        width=300
    )
    dob = ft.TextField(label="Date of Birth (YYYY-MM-DD)", width=300)
    address = ft.TextField(label="Address", multiline=True, width=300)
    agree = ft.Checkbox(label="I agree to the Terms & Conditions")

    message = ft.Text(size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def validate_registration_inputs(
            name: str, email: str, password: str,
            confirm_password: str, contact: str, birthdate: str
    ) -> str | None:
        """Validates registration form inputs and returns an error string if invalid."""
        if not all([name.strip(), email.strip(), password.strip(),
                    confirm_password.strip(), contact.strip(), birthdate.strip()]):
            return "⚠ Please fill in all required fields."

        if not re.match(r"^[A-Za-z\s]+$", name):
            return "⚠ Name must contain only letters and spaces."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "⚠ Invalid email address format."

        if len(password) < 6:
            return "⚠ Password must be at least 6 characters long."

        if password != confirm_password:
            return "⚠ Passwords do not match!"

        if not contact.isdigit() or not (7 <= len(contact) <= 15):
            return "⚠ Contact number must contain 7–15 digits only."

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", birthdate):
            return "⚠ Invalid date format. Use YYYY-MM-DD."

        try:
            datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            return "⚠ Invalid date. Please enter a real calendar date."

        return None  # ✅ No errors found

    def submit_registration(e):
        """Handles registration submission with validation and centered message."""
        error = validate_registration_inputs(
            name.value, email.value, password.value,
            confirm_password.value, contact.value, dob.value
        )

        if error:
            message.value = error
            message.color = "red"
        else:
            records.append({
                "type": "Registration",
                "Name": str(name.value),
                "Email": str(email.value),
                "Contact": str(contact.value),
                "Gender": str(gender.value),
                "DOB": str(dob.value),
                "Address": str(address.value)
            })
            message.value, message.color = f":white_check_mark: Registration successful! Welcome, {name.value}.", "green"
        page.update()

    registration_form: ft.Column = ft.Column([
        ft.Text("User Registration Form", size=22, weight=ft.FontWeight.BOLD),
        name, email, password, confirm_password, contact, gender, dob, address, agree,
        ft.ElevatedButton("Register", on_click=submit_registration),
        ft.Container(content=message, alignment=ft.alignment.center),
        ft.Row([
            ft.TextButton("Go to Booking", on_click=lambda e: navigate_to(booking_form)),
            ft.TextButton("View All Records", on_click=lambda e: navigate_to(view_records_page))
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # =========================
    # BOOKING FORM
    # =========================
    service_type = ft.Dropdown(
        label="Service / Room Type",
        options=[
            ft.dropdown.Option("Single Room"),
            ft.dropdown.Option("Double Room"),
            ft.dropdown.Option("Conference Hall"),
            ft.dropdown.Option("Event Package"),
        ],
        width=300,
    )
    booking_date = ft.TextField(label="Booking Date (YYYY-MM-DD)", width=300)
    booking_time = ft.TextField(label="Booking Time (HH:MM)", width=300)
    guests = ft.TextField(label="Number of Guests", width=300)
    payment = ft.Dropdown(
        label="Payment Method",
        options=[
            ft.dropdown.Option("Cash"),
            ft.dropdown.Option("Credit Card"),
            ft.dropdown.Option("GCash"),
        ],
        width=300,
    )
    special_request = ft.TextField(label="Special Requests", multiline=True, width=300)
    confirm_terms = ft.Checkbox(label="I confirm the above booking details")
    booking_msg = ft.Text(size=16, text_align=ft.TextAlign.CENTER)

    def submit_booking(e: ft.ControlEvent) -> None:
        """Handles booking submission."""
        if not all([service_type.value, booking_date.value, booking_time.value, guests.value, payment.value]):
            booking_msg.value, booking_msg.color = "⚠ Please complete all required fields.", "red"
        else:
            records.append({
                "type": "Booking",
                "Service": str(service_type.value),
                "Date": str(booking_date.value),
                "Time": str(booking_time.value),
                "Guests": str(guests.value),
                "Payment": str(payment.value),
                "Special Request": str(special_request.value)
            })
            booking_msg.value, booking_msg.color = (
                f"✅ Booking confirmed for {booking_date.value} at {booking_time.value}!",
                "green",
            )
        page.update()

    booking_form: ft.Column = ft.Column([
        ft.Text("Booking Form", size=22, weight=ft.FontWeight.BOLD),
        service_type, booking_date, booking_time, guests, payment, special_request, confirm_terms,
        ft.ElevatedButton("Submit Booking", on_click=submit_booking),
        ft.Container(content=booking_msg, alignment=ft.alignment.center),
        ft.Row([
            ft.TextButton("Go to Feedback", on_click=lambda e: navigate_to(feedback_form)),
            ft.TextButton("View All Records", on_click=lambda e: navigate_to(view_records_page))
        ], alignment=ft.MainAxisAlignment.CENTER),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # =========================
    # FEEDBACK FORM
    # =========================
    fb_name = ft.TextField(label="Your Name", width=300)
    fb_email = ft.TextField(label="Your Email", width=300)
    fb_subject = ft.Dropdown(
        label="Subject",
        options=[
            ft.dropdown.Option("Service Quality"),
            ft.dropdown.Option("Website UI"),
            ft.dropdown.Option("Booking Experience"),
            ft.dropdown.Option("Other"),
        ],
        width=300,
    )
    fb_message = ft.TextField(label="Message", multiline=True, width=300)
    fb_rating = ft.Slider(label="Rate us (1–5)", min=1, max=5, divisions=4, value=3)
    fb_output = ft.Text(size=16, text_align=ft.TextAlign.CENTER)

    def submit_feedback(e: ft.ControlEvent) -> None:
        """Handles feedback form submission."""
        if not all([fb_name.value, fb_email.value, fb_subject.value, fb_message.value]):
            fb_output.value, fb_output.color = "⚠ Please complete all fields.", "red"
        else:
            records.append({
                "type": "Feedback",
                "Name": str(fb_name.value),
                "Email": str(fb_email.value),
                "Subject": str(fb_subject.value),
                "Message": str(fb_message.value),
                "Rating": int(fb_rating.value)
            })
            fb_output.value, fb_output.color = (
                f"✅ Thank you, {fb_name.value}! Feedback received.",
                "green",
            )
        page.update()

    feedback_form: ft.Column = ft.Column([
        ft.Text("Feedback Form", size=22, weight=ft.FontWeight.BOLD),
        fb_name, fb_email, fb_subject, fb_message, fb_rating,
        ft.ElevatedButton("Submit Feedback", on_click=submit_feedback),
        ft.Container(content=fb_output, alignment=ft.alignment.center),
        ft.Row([
            ft.TextButton("Back to Registration", on_click=lambda e: navigate_to(registration_form)),
            ft.TextButton("View All Records", on_click=lambda e: navigate_to(view_records_page))
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # =========================
    # VIEW RECORDS PAGE
    # =========================
    record_display: ft.ListView = ft.ListView(expand=True, spacing=10, padding=10)

    def update_records_view() -> None:
        """Refreshes record display with current records."""
        record_display.controls.clear()
        if not records:
            record_display.controls.append(ft.Text("No records found.", color="gray"))
        else:
            for i, rec in enumerate(records, start=1):
                details: str = "\n".join(f"{k}: {v}" for k, v in rec.items())
                record_display.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Text(f"Record #{i}\n{details}", selectable=True),
                            padding=10,
                        )
                    )
                )
        page.update()

    view_records_page: ft.Column = ft.Column([
        ft.Text("📋 View All Records", size=22, weight=ft.FontWeight.BOLD),
        record_display,
        ft.Row([
            ft.TextButton("Back to Registration", on_click=lambda e: navigate_to(registration_form))
        ], alignment=ft.MainAxisAlignment.CENTER),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def go_to_view_records(e: ft.ControlEvent) -> None:
        update_records_view()
        navigate_to(view_records_page)

    # Patch all “View All Records” buttons
    for form in [registration_form, booking_form, feedback_form]:
        for ctrl in form.controls:
            if isinstance(ctrl, ft.Row):
                for btn in ctrl.controls:
                    if "View All Records" in getattr(btn, "text", ""):
                        btn.on_click = go_to_view_records

    # Start app
    navigate_to(registration_form)


ft.app(target=main)
