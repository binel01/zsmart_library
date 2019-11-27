import AdjustBalance
import CRMActivation
import helpers
import ModUserIndiPricePlan
import NewConnection
import QueryProfileAndBal
import Termination
import QueryCDR
import SponsorUserIndiPricePlan
import AddCUG
import DelCUG
import JoinCUG
import ExitCUG
import QueryCUG

class ZsmartLibrary:

    ROBOT_LIBRARY_VERSION = 1.0

    def __init__(self):
    	pass

    def adjust_balance(self, phone_number, tx_seq_num, acc_res_code=1, balance=-80000000, add_days=30):
    	"""
    	Calls ZSMART's AdjustBalance API
    	Used to Adjust the balance of a defined number
    	negative amount to increase the balance and positive amount to decrease the balance
    	"""
        return AdjustBalance.AdjustBalance(phone_number, tx_seq_num, acc_res_code, balance, add_days)
        
    def crm_activation(self, phone_number):
    	"""
    	Calls ZSMART's CRMActivation API
    	Used to activate a number
    	"""
    	return CRMActivation.CRMActivation(phone_number)
    	
    def add_sub_account(self, phone_number, acc_res_code='1', balance='-1073741824', add_days=30):
    	"""
    	Adds a sub account on a subscriber's line. If the sub account already exists, it will
    	just adjust its balance and expiry date
    	"""
    	phone_number = str(phone_number)
    	tx_seq_num = helpers.get_transaction_number()
    	result = AdjustBalance.AdjustBalance(phone_number, tx_seq_num, acc_res_code, balance, add_days)
    	return result
    	
    def create_sub_account(self, phone_number, acc_res_code, balance, add_days='30'):
    	"""
    	Similar to Add Sub Account keyword, it adds a new sub account on the line
    	"""
    	#balance = balance * 100
    	return helpers.create_sub_account(phone_number, acc_res_code, balance, add_days)
    	
    	
    def create_all_sms_sub_accounts(self, phone_number):
    	"""
	    Adds all the sub accounts of the SMS service on a line
	    """
    	return helpers.add_all_sms_sub_accounts(phone_number)
    	
	def create_all_data_sub_accounts(self, phone_number):
		"""
		Adds all the Data sub accounts of the Data service
		"""
		return helpers.add_all_data_sub_accounts(phone_number)
		 		
    def terminate_and_activate_number(self, phone_number, price_plan = '985'):
    	"""
		1. Terminate the subscriber's line
		2. NewConnection
		"""
    	return helpers.terminate_and_activate(phone_number, price_plan = '985')
    	
    def add_price_plan(self, phone_number, ind_price_plan, exp_date):
    	"""
	    Adds an Individual Price Plan from the line
	    """
    	return ModUserIndiPricePlan.add_ind_price_plan(phone_number, ind_price_plan, exp_date)
    	
    def remove_price_plan(self, phone_number, ind_price_plan):
    	"""
	    Deletes an Individual Price Plan from the line
	    """
    	return ModUserIndiPricePlan.delete_ind_price_plan(phone_number, ind_price_plan)
    	
    def new_connection(self, phone_number, brand_index=985, start_state='G'):
    	"""
    	Calls ZSMART's NewConnection API
    	"""
    	return NewConnection.NewConnection(phone_number, brand_index=985, start_state='G')

    def query_profile(self, phone_number):
    	"""
    	Calls ZSMART's QueryProfileAndBal API
    	"""
    	return QueryProfileAndBal.QueryProfileAndBal(phone_number)
    	
    def termination(self, phone_number):
   		"""
   		Calls ZSMART's Termination API
   		"""
   		return Termination.Termination(phone_number)
    	
    def get_sub_account_balance(self, phone_number, account="Main Balance"):
    	"""
    	Get the account balance of the specified number
    	"""
    	return helpers.get_account_balance(phone_number, account)
    	
	def query_cdr(self, phone_number, billing_cycle, cdr_type=1):
		"""
		Gets all the CDRs of a number on a defined billing_cycle
		"""
		return QueryCDR.QueryCDR(phone_number, billing_cycle, cdr_type)
	
	def get_last_cdr(self, phone_number, date_time, cdr_type):
		"""
		Gets the last CDR of a phone number
		"""
		return QueryCDR.get_last_cdr(phone_number, date_time, 'voice')
    	
    def sponsor_user_indi_price_plan(self, msisdn_prin, msisdn_benef, indi_ppp):
    	"""
    	Subscribes to an IPP using one number as principal number and 
    	makes an ipp deposit on another number
    	"""
    	return SponsorUserIndiPricePlan.SponsorUserIndiPricePlan(msisdn_prin, msisdn_benef, indi_ppp)
    	
    def del_cug(self, cug_id, admin_msisdn='', admin_pwd=''):
    	"""
    	Deletes a VPN group
    	"""
    	return DelCUG.DelCUG(cug_id, admin_msisdn, admin_pwd)
    	
    def join_cug(self, cug_id, msisdn, user_pwd='00000000'):
    	"""
    	Adds a number to the VPN group
    	"""
    	return JoinCUG.JoinCUG(cug_id, msisdn, user_pwd)
    	
    def exit_cug(self, cug_id, msisdn, user_pwd='00000000'):
    	"""
    	Removes a number from the VPN group
    	"""
    	return ExitCUG.ExitCUG(cug_id, msisdn, user_pwd)
    	
    def add_cug(self, cug_name, admin_msisdn='', admin_pwd='', cug_type='C', ipp_code='20360', member_amount='5'):
		"""
		This API create a VPN group for numbers, and 
		returns the CUG_id which uniquely identify the VPN group
		"""
		return AddCUG.AddCUG(cug_name, admin_msisdn, admin_pwd, cug_type, ipp_code, member_amount)
    
    def query_cug(self, cug_name):
    	"""
    	Gets the CUG ID by the name of the CUG
    	"""
    	return QueryCUG.QueryCUG(cug_name)
    
    def integer_division(self, number_1, number_2):
		"""
		Return the Integer division of `number_1` by `number_2`
		"""
		result = 0
		if number_2 != 0:
			result = number_1 / number_2
		else:
			raise Exception('Division impossible')
		
		return result

    def integer_subtraction(self, number_1, number_2):
		"""
		Returns the subtraction of number_1 by number_2
		"""
		return number_1 - number_2		
		
		
		