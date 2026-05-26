import frappe
from frappe.desk.page.setup_wizard.setup_wizard import setup_complete


def complete_wizard():
    setup_complete(
        {
            "language": "english",
            "country": "India",
            "timezone": "Asia/Kolkata",
            "currency": "INR",
            "full_name": "RDS Administrator",
            "email": "ra.pandey008@gmail.com",
            "password": frappe.generate_hash(length=20),
            "company_name": "RD School Betul",
            "company_abbr": "RSB",
            "company_tagline": "RD School Betul",
            "chart_of_accounts": "Standard with Numbers",
            "fy_start_date": "2026-04-01",
            "fy_end_date": "2027-03-31",
            "domains": [],
            "setup_demo": 0,
            "bank_account": "",
        }
    )
    frappe.db.commit()
