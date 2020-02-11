import frappe

def before_install():
	"""runs before installation"""
	return check_setup_wizard_is_completed()
	
def check_setup_wizard_is_completed():
	if not frappe.db.get_default('desktop:home_page') == 'desktop':
		print()
		print("Fimax cannot be installed on a fresh site where the setup wizard is not completed")
		print("You can run the setup wizard and come back to finish with the installation")
		print()
		return False