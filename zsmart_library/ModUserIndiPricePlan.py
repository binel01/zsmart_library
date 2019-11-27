import requests
from datetime import datetime
from lxml import etree

def ModUserIndiPricePlan(phone_number, price_plan, action=1, exp_date=''):
	xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ocs="http://ocs.ztesoft.com">
      <soapenv:Header>
    <AuthHeader xmlns="http://ZTEsoft.com/webservices/">
      <Username>zsmart</Username>
      <Password>zsmart</Password>
    </AuthHeader>
</soapenv:Header>
   <soapenv:Body>
      <ocs:doService>
         <ocs:in0><![CDATA[

					<?xml version="1.0" encoding="UTF-8"?>
					<zsmart> 
					  <Data>
					   <header>
					      <ACTION_ID>ModUserIndiPricePlan</ACTION_ID>
					      <REQUEST_ID>009009040266651</REQUEST_ID>
					    </header>
					    <body>
						  <MSISDN>phone_number</MSISDN>
					         <UserPwd>00000000</UserPwd>
					         <PricePlanChgDtoList>
					            <PricePlanChgDto>
					               <PricePlanIndex>price_plan</PricePlanIndex>
					               <Action>action</Action>
					               <EffType>2</EffType>
					               <EffDate></EffDate>
					               <ExpDate>exp_date</ExpDate>
					               <ChargeFlag>1</ChargeFlag>
					            </PricePlanChgDto>
					         </PricePlanChgDtoList>
					    </body>
					  </Data>
					</zsmart>

				]]></ocs:in0>
      </ocs:doService>
</soapenv:Body>
</soapenv:Envelope>"""
		
	# set the parameters
	end_point = 'http://172.27.82.33:9060/ocswebservices/services/WebServices.WebServicesHttpSoap11Endpoint/'
	headers = {'Content-Type': 'text/xml'}
	xml = xml.replace("phone_number", str(phone_number))
	xml = xml.replace("price_plan", str(price_plan))
	xml = xml.replace("action", str(action))
	xml = xml.replace("exp_date", str(exp_date))

	# send the request
	result = requests.post(end_point, data=xml, headers=headers)
	   
	# clean the result
	new_xml = result.text.replace('&lt;', '<')
	new_xml = new_xml.replace('&gt;', '>')
	new_xml = new_xml.replace("""<?xml version='1.0' encoding='UTF-8'?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><doServiceResponse xmlns="http://ocs.ztesoft.com"><doServiceReturn><?xml version="1.0" encoding="UTF-8"?>""", '')
	new_xml = new_xml.replace("""</doServiceReturn></doServiceResponse></soapenv:Body></soapenv:Envelope>""", '')
	   
	# We get the CUG
	root = etree.fromstring(new_xml)
	return_msg = root.xpath('//zsmart/Data/header/returnMsg')[0].text

	if return_msg == 'Successful':
		print('ModUserIndiPricePlan request has been executed successfully !')
	else:
		raise Exception('ModUserIndiPricePlan: ' + return_msg)
	
	return return_msg

def delete_ind_price_plan(phone_number, ind_price_plan):
    """
    Deletes an Individual Price Plan from the line
    """
    action = 0
    exp_date = "2019-01-01"
    result = ModUserIndiPricePlan(phone_number, ind_price_plan, action, exp_date)
    return result

def add_ind_price_plan(phone_number, ind_price_plan, exp_date = ''):
    """
    Adds an Individual Price Plan from the line
    """
    action = 1
    result = ModUserIndiPricePlan(phone_number, ind_price_plan, action, exp_date)
    return result
	

