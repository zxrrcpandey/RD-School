"""One-shot ERPNext Setup Wizard completion for an RD School site.

Run BEFORE installing the rdschool app (its after_install seeds need a Company):

    bench --site <site> console
    >>> from rdschool.setup import complete_wizard
    >>> complete_wizard(company_name="RDPS Betul", company_abbr="RSB")

Company name/abbr are PARAMETERS — don't hardcode a site's company here. The
abbr suffixes every account head (e.g. "Cash - RSB") and is painful to change
later, so pass it deliberately per site.
"""

import frappe
from frappe.desk.page.setup_wizard.setup_wizard import setup_complete


def complete_wizard(
    company_name="RD School Betul",
    company_abbr="RSB",
    country="India",
    currency="INR",
    timezone="Asia/Kolkata",
    chart_of_accounts="Standard with Numbers",
    fy_start_date="2026-04-01",
    fy_end_date="2027-03-31",
    email="ra.pandey008@gmail.com",
    full_name="RDS Administrator",
):
    """Complete the Setup Wizard non-interactively. Skips if already complete."""
    if frappe.db.get_single_value("System Settings", "setup_complete"):
        print("complete_wizard: setup already complete — skipping")
        return

    setup_complete(
        {
            "language": "english",
            "country": country,
            "timezone": timezone,
            "currency": currency,
            "full_name": full_name,
            "email": email,
            "password": frappe.generate_hash(length=20),
            "company_name": company_name,
            "company_abbr": company_abbr,
            "company_tagline": company_name,
            "chart_of_accounts": chart_of_accounts,
            "fy_start_date": fy_start_date,
            "fy_end_date": fy_end_date,
            "domains": [],
            "setup_demo": 0,  # never seed ERPNext demo data
            "bank_account": "",
        }
    )
    frappe.db.commit()
    print(
        f"complete_wizard: done — company={company_name!r} abbr={company_abbr!r} "
        f"FY {fy_start_date}..{fy_end_date}"
    )
