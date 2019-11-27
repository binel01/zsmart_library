import requests
from lxml import etree

def AddCUG(cug_name, admin_msisdn='', admin_pwd='', cug_type='C', ipp_code='20360', member_amount='5'):
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
					      <ACTION_ID>AddCUG</ACTION_ID>
					      <REQUEST_ID>0152009040200139</REQUEST_ID>
					    </header>
					    <body>
						  <CUGName>cug_name</CUGName>
					         <AdminMSISDN>admin_msisdn</AdminMSISDN>
					         <AdminPwd>admin_pwd</AdminPwd>
					         <CUGTypeID>cug_type</CUGTypeID>
					          <PricePlanCode>ipp_code</PricePlanCode>
					         <MaxMemberAmount>member_amount</MaxMemberAmount>
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

	xml = xml.replace("cug_name", str(cug_name))
	xml = xml.replace("admin_msisdn", str(admin_msisdn))
	xml = xml.replace("admin_pwd", str(admin_pwd))
	xml = xml.replace("cug_type", str(cug_type))
	xml = xml.replace("ipp_code", str(ipp_code))
	xml = xml.replace("member_amount", str(member_amount))

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

	cug_id = 0
	if return_msg == 'Successful':
		print('AddCUG request has been executed successfully !')
		cug_id = root.xpath('//zsmart/Data/body/CUGID')[0].text
	else:
		raise Exception('AddCUG: ' + return_msg)
	
	return cug_id
