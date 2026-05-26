app_name = "rdschool"
app_title = "RD School"
app_publisher = "Trustbit"
app_description = "Custom app for RD School Betul: purchase workflow, departments, approvals, reports"
app_email = "ra.pandey008@gmail.com"
app_license = "mit"


# Auto-seed masters & customizations on a fresh install.
after_install = "rdschool.setup_data.setup_all"


# Per-doctype event handlers.
doc_events = {
    "Material Request": {
        "validate": "rdschool.material_request.copy_cost_center_to_items",
    },
    "Purchase Order": {
        "validate": "rdschool.material_request.copy_cost_center_from_mr",
    },
}


# Row-level visibility. Teachers see only their own MRs; everyone else (Principal,
# Stores, Accountant, Auditor, sysadmins) sees all.
permission_query_conditions = {
    "Material Request": "rdschool.permissions.material_request_query",
}


# Customizations exported to apps/rdschool/rdschool/fixtures/ so they replay
# on any future `bench install-app rdschool`. Run `bench export-fixtures
# --app rdschool` after changing any of these in the UI to refresh the JSON.
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["fieldname", "like", "rsb_%"]],
    },
    {
        "doctype": "Role",
        "filters": [["name", "like", "School %"]],
    },
    {
        "doctype": "Role Profile",
        "filters": [["role_profile", "like", "School %"]],
    },
    {
        "doctype": "Workflow",
        "filters": [["workflow_name", "=", "MR Approval - RSB"]],
    },
    {
        "doctype": "Workflow State",
        "filters": [["name", "in", ["Pending Approval"]]],
    },
    {
        "doctype": "Workflow Action Master",
        "filters": [["name", "in", ["Submit for Approval", "Approve", "Reject"]]],
    },
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "rdschool",
# 		"logo": "/assets/rdschool/logo.png",
# 		"title": "RD School",
# 		"route": "/rdschool",
# 		"has_permission": "rdschool.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rdschool/css/rdschool.css"
# app_include_js = "/assets/rdschool/js/rdschool.js"

# include js, css files in header of web template
# web_include_css = "/assets/rdschool/css/rdschool.css"
# web_include_js = "/assets/rdschool/js/rdschool.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rdschool/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "rdschool/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "rdschool.utils.jinja_methods",
# 	"filters": "rdschool.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rdschool.install.before_install"
# after_install = "rdschool.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rdschool.uninstall.before_uninstall"
# after_uninstall = "rdschool.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "rdschool.utils.before_app_install"
# after_app_install = "rdschool.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "rdschool.utils.before_app_uninstall"
# after_app_uninstall = "rdschool.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rdschool.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"rdschool.tasks.all"
# 	],
# 	"daily": [
# 		"rdschool.tasks.daily"
# 	],
# 	"hourly": [
# 		"rdschool.tasks.hourly"
# 	],
# 	"weekly": [
# 		"rdschool.tasks.weekly"
# 	],
# 	"monthly": [
# 		"rdschool.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "rdschool.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rdschool.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "rdschool.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rdschool.utils.before_request"]
# after_request = ["rdschool.utils.after_request"]

# Job Events
# ----------
# before_job = ["rdschool.utils.before_job"]
# after_job = ["rdschool.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"rdschool.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

