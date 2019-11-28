import requests
from lxml import etree


def NewConnection(phone_number, brand_index=985, start_state='G'):
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
						      <ACTION_ID>NewConnection</ACTION_ID>
						      <REQUEST_ID>027210914126658</REQUEST_ID>
						    </header>
						    <body>
								<ProviderID>0</ProviderID>
								<MSISDN>phone_number</MSISDN>
								<BrandIndex>brand_index</BrandIndex>
								<InitState>start_state</InitState>
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
    xml = xml.replace('phone_number', str(phone_number))
    xml = xml.replace('brand_index', str(brand_index))
    xml = xml.replace('start_state', start_state)

    # send the request
    result = requests.post(end_point, data=xml, headers=headers)

    # clean the result
    new_xml = result.text.replace('&lt;', '<')
    new_xml = new_xml.replace("&gt;", '>')
    new_xml = new_xml.replace(
        """<?xml version='1.0' encoding='UTF-8'?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><doServiceResponse xmlns="http://ocs.ztesoft.com"><doServiceReturn><?xml version="1.0" encoding="UTF-8"?>""", '')
    new_xml = new_xml.replace(
        """</doServiceReturn></doServiceResponse></soapenv:Body></soapenv:Envelope>""", '')

    # We get the CUG
    root = etree.fromstring(new_xml)
    return_msg = root.xpath('//zsmart/Data/header/returnMsg')[0].text

    if return_msg == 'Successful':
        print('NewConnection request has been executed successfully !')
    else:
        raise Exception('NewConnection: ' + return_msg)

    return return_msg
