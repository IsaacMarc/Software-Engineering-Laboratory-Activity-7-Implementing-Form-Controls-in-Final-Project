import flet as ft


def main(page: ft.Page):
    page.window_resizable = True
    page.title = "Booking System"
    page.theme_mode = "light"  # Default theme
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ============================
    # Theme toggle
    # ============================
    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        theme_button.text = "🌙 Dark Mode" if page.theme_mode == "light" else "☀️ Light Mode"
        page.update()

    theme_button = ft.TextButton("🌙 Dark Mode", on_click=toggle_theme)

    # ============================
    # Page navigation helper
    # ============================
    def navigate_to(target):
        page.controls.clear()
        page.add(theme_button, target)
        page.update()

    # ============================
    # 1️⃣ USER REGISTRATION FORM
    # ============================
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

    def submit_registration(e):
        if not all([name.value, email.value, password.value, confirm_password.value, contact.value]):
            message.value = "⚠ Please fill in all required fields."
            message.color = "red"
        elif password.value != confirm_password.value:
            message.value = "⚠ Passwords do not match!"
            message.color = "red"
        else:
            message.value = f"✅ Registration successful! Welcome, {name.value}."
            message.color = "green"
        page.update()

    registration_form = ft.Column([
        ft.Text("User Registration Form", size=22, weight=ft.FontWeight.BOLD),
        name, email, password, confirm_password, contact, gender, dob, address, agree,
        ft.ElevatedButton("Register", on_click=submit_registration),
        ft.Container(content=message, alignment=ft.alignment.center),
        ft.TextButton("Go to Booking Form", on_click=lambda e: navigate_to(booking_form))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # ============================
    # 2️⃣ BOOKING FORM
    # ============================
    service_type = ft.Dropdown(
        label="Service / Room Type",
        options=[
            ft.dropdown.Option("Single Room"),
            ft.dropdown.Option("Double Room"),
            ft.dropdown.Option("Conference Hall"),
            ft.dropdown.Option("Event Package")
        ],
        width=300
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
        width=300
    )
    special_request = ft.TextField(label="Special Requests", multiline=True, width=300)
    confirm_terms = ft.Checkbox(label="I confirm the above booking details")
    booking_msg = ft.Text(size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def submit_booking(e):
        if not all([service_type.value, booking_date.value, booking_time.value, guests.value, payment.value]):
            booking_msg.value = "⚠ Please complete all required fields."
            booking_msg.color = "red"
        else:
            booking_msg.value = f"✅ Booking confirmed for {booking_date.value} at {booking_time.value}!"
            booking_msg.color = "green"
        page.update()

    booking_form = ft.Column([
        ft.Text("Booking Form", size=22, weight=ft.FontWeight.BOLD),
        service_type, booking_date, booking_time, guests, payment, special_request, confirm_terms,
        ft.ElevatedButton("Submit Booking", on_click=submit_booking),
        ft.Container(content=booking_msg, alignment=ft.alignment.center),
        ft.TextButton("Go to Search Form", on_click=lambda e: navigate_to(search_form))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # ============================
    # 3️⃣ SEARCH FORM
    # ============================
    search_keyword = ft.TextField(label="Search Booking / Room", width=300)
    search_date = ft.TextField(label="Date (Optional)", width=300)
    search_result = ft.Text(size=16, text_align=ft.TextAlign.CENTER)

    def perform_search(e):
        if not search_keyword.value:
            search_result.value = "⚠ Please enter a keyword."
            search_result.color = "red"
        else:
            search_result.value = f"🔍 Showing results for '{search_keyword.value}' on {search_date.value or 'any date'}."
            search_result.color = "green"
        page.update()

    search_form = ft.Column([
        ft.Text("Search Form", size=22, weight=ft.FontWeight.BOLD),
        search_keyword, search_date,
        ft.ElevatedButton("Search", on_click=perform_search),
        ft.Container(content=search_result, alignment=ft.alignment.center),
        ft.TextButton("Go to Feedback Form", on_click=lambda e: navigate_to(feedback_form))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # ============================
    # 4️⃣ FEEDBACK FORM
    # ============================
    fb_name = ft.TextField(label="Your Name", width=300)
    fb_email = ft.TextField(label="Your Email", width=300)
    fb_subject = ft.Dropdown(
        label="Subject",
        options=[
            ft.dropdown.Option("Service Quality"),
            ft.dropdown.Option("Website UI"),
            ft.dropdown.Option("Booking Experience"),
            ft.dropdown.Option("Other")
        ],
        width=300
    )
    fb_message = ft.TextField(label="Message", multiline=True, width=300)
    fb_rating = ft.Slider(label="Rate us (1–5)", min=1, max=5, divisions=4, value=3)
    fb_output = ft.Text(size=16, text_align=ft.TextAlign.CENTER)

    def submit_feedback(e):
        if not all([fb_name.value, fb_email.value, fb_subject.value, fb_message.value]):
            fb_output.value = "⚠ Please complete all fields."
            fb_output.color = "red"
        else:
            fb_output.value = f"✅ Thank you, {fb_name.value}! Feedback received."
            fb_output.color = "green"
        page.update()

    feedback_form = ft.Column([
        ft.Text("Feedback Form", size=22, weight=ft.FontWeight.BOLD),
        fb_name, fb_email, fb_subject, fb_message, fb_rating,
        ft.ElevatedButton("Submit Feedback", on_click=submit_feedback),
        ft.Container(content=fb_output, alignment=ft.alignment.center),
        ft.TextButton("Back to Registration", on_click=lambda e: navigate_to(registration_form))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Start on registration form
    navigate_to(registration_form)

# Add resizable=False to prevent window resizing
ft.app(target=main)