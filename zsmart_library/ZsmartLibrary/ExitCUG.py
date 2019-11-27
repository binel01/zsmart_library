import requests
from lxml import etree

def ExitCUG(cug_id, msisdn, user_pwd='00000000'):
	xml = """ <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ocs="http://ocs.ztesoft.com">
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
							      <ACTION_ID>ExitCUG</ACTION_ID>
							      <REQUEST_ID>015210914126656</REQUEST_ID>
							    </header>
							    <body>
								 <CUGID>cug_id</CUGID>
							         <AdminMSISDN></AdminMSISDN>
							         <AdminPwd></AdminPwd>
							         <MSISDN>msisdn</MSISDN>
							         <UserPwd>user_pwd</UserPwd>
							         <ChargeFlag>0</ChargeFlag>
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
		
	xml = xml.replace("cug_id", str(cug_id))
	xml = xml.replace("msisdn", str(msisdn))
	xml = xml.replace("user_pwd", str(user_pwd))
		
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
		print('ExitCUG request has been executed successfully !')
	else:
		raise Exception('ExitCUG: ' + return_msg)
	
	return return_msg

	