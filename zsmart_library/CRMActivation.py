import requests
from lxml import etree

def CRMActivation(phone_number):
	xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://com.ztesoft.zsmart/xsd">
   		<soapenv:Header>
      		<xsd:AuthHeader>
		        <Username>zsmart</Username>
		        <Password>zsmart</Password>
			</xsd:AuthHeader>
   		</soapenv:Header>
   		<soapenv:Body>
      		<xsd:doService>
         		<in0><![CDATA[
						
				<?xml version="1.0" encoding="UTF-8"?>
				<zsmart>
					<Data>
						<header>
							<ACTION_ID>CRMActivation</ACTION_ID>
							<REQUEST_ID>003201708024085</REQUEST_ID>
						</header>
						<body>
					         <ProviderID></ProviderID>
					         <MSISDN>phone_number</MSISDN>
					         <BalanceType></BalanceType>
					         <BalanceAmount></BalanceAmount>
					         <ExpDate></ExpDate>
						</body>
					</Data>
				</zsmart>
				
				]]></in0>
			</xsd:doService>
		</soapenv:Body>
	</soapenv:Envelope>"""
		
	# set the parameters
	end_point = 'http://172.27.82.33:9060/ocswebservices/services/WebServices.WebServicesHttpSoap11Endpoint/'
	headers = {'Content-Type': 'text/xml'}
	xml = xml.replace("phone_number", str(phone_number))
		
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
		print('CRMActivation request has been executed successfully !')
	else:
		raise Exception('CRMActivation: ' + return_msg)
	
	return return_msg
