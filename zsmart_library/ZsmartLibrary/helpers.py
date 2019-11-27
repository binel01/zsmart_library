import AdjustBalance
import Termination
import NewConnection
import QueryProfileAndBal

from lxml import etree

def get_transaction_number():
	"""
	Gets a new transaction_number from the file
	"""
	try:
		f = open('./transaction_number.txt', 'r')
		tx_number = f.readline(15)
		f.close()
		set_transaction_index(tx_number)
		return tx_number
	except:
		set_transaction_index()
	return

def set_transaction_index(transaction_index="3201264915097"):
	"""
	Sets the new index for the transaction numbers
	"""
	tx_ind = int(transaction_index) + 1
	f = open('./transaction_number.txt', 'w')
	f.write(str(tx_ind))
	f.close()

def create_sub_account(phone_number, acc_res_code, balance, add_days):
	"""
	Adds a sub account on a subscriber's line
	"""
	phone_number = str(phone_number)
	tx_seq_num = get_transaction_number()
	result = AdjustBalance.AdjustBalance(phone_number, tx_seq_num, acc_res_code, balance, add_days)
	return result

def add_all_sms_sub_accounts(phone_number):
	"""
	Adds all the sub accounts of the SMS service on a line
	"""
	sub_acc_list = [5,7,48,57,8,9,58,185,12,61,73,170,11,41,177,80,163,176,124,52,98,43,13,10,68,232,183,46,30,85,51,76,94,45,89,168,172,634,171,131,222,47,55,169,86,159,72,3,54,27,22,71]

	for acc_code in sub_acc_list:
		res = create_sub_account(phone_number, acc_code)
		print(res)

def add_all_data_sub_accounts(phone_number):
	"""
	Adds all the sub accounts of the Data service on a line
	"""
	sub_acc_list = [50,197,59,88,93,235,236,237,238,239,240,91,636,53,242,245,246,247,248,249,834,\
		81,83,82,62,75,184,35,230,157,182,228,223,36,95,37,174,115,181,96,161,38,125,179,227,107,114,\
		87,97,175,112,111,109,63,156,194,121,122,225,224,130,49,244,243,250,69,233]
	
	for acc_code in sub_acc_list:
		res = create_sub_account(phone_number, acc_code)
		print(res)
	

def terminate_and_activate(phone_number, price_plan = '985'):
	"""
	1. Terminate the subscriber's line
	2. NewConnection
	"""
	tx_num = get_transaction_number()
	print (Termination.Termination(phone_number))
	print (NewConnection.NewConnection(phone_number, price_plan, 'A'))
	print (AdjustBalance.AdjustBalance(phone_number, tx_num))
	return
	
def get_account_balance(phone_number, account):
	"""
	Gets the value of the balance of a Sub account
	"""
	res = QueryProfileAndBal.QueryProfileAndBal(phone_number)
	res = res.replace("&gt;", '>')
	res = res.replace('&lt;', '<')
	
	root = etree.fromstring(res)
	res_state = root.xpath('//zsmart/Data/header/returnMsg')[0].text
	
	acc_codes = root.xpath('//zsmart/Data/body/BalDtoList/BalDto/AcctResCode')
	acc_names = root.xpath('//zsmart/Data/body/BalDtoList/BalDto/AcctResName')
	acc_bal = root.xpath('//zsmart/Data/body/BalDtoList/BalDto/Balance')
	acc_exp_date = root.xpath('//zsmart/Data/body/BalDtoList/BalDto/ExpDate')
	
	response = [0]
	if (res_state == 'Successful'):
		print('The request has been executed successfully !')
		old_balance = 0
		for i in range(0, len(acc_names)):
			balance = int(acc_bal[i].text) * (-1.0)
			if acc_names[i].text == account:
				if acc_names[i].text == 'Main Balance':
					balance = balance / 100.0
				balance = old_balance + balance
				old_balance = balance
				response = [acc_codes[i].text, acc_names[i].text, balance, acc_exp_date[i].text]
			elif acc_codes[i].text == account:
				if acc_names[i].text == 'Main Balance':
					balance = balance / 100.0
				balance = old_balance + balance
				old_balance = balance
				response = [acc_codes[i].text, acc_names[i].text, balance, acc_exp_date[i].text]
	else:
		print('The request has failed !')
	
	return response
	