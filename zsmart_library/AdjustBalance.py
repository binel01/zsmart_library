import requests
from lxml import etree


def AdjustBalance(phone_number, tx_seq_num, acc_res_code='1', balance='-80000000', add_days='30'):
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
					      <ACTION_ID>AdjustBalance</ACTION_ID>
					      <REQUEST_ID>003201283930045  </REQUEST_ID>
					    </header>
					    <body>
					         <Channel_ID></Channel_ID>
					         <MSISDN>phone_number</MSISDN>
					         <AccountCode></AccountCode>
					         <AcctResCode>acc_res_code</AcctResCode>
					         <AddBalance>balance</AddBalance>
					         <AddDays>add_days</AddDays>
					         <OperationStaff></OperationStaff>
					         <TransactionSN>tx_seq_num</TransactionSN>
					         <TransactionDesc></TransactionDesc>
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
    xml = xml.replace("acc_res_code", str(acc_res_code))
    xml = xml.replace("balance", str(balance))
    xml = xml.replace("add_days", str(add_days))
    xml = xml.replace("tx_seq_num", str(tx_seq_num))

    # send the request
    result = requests.post(end_point, data=xml, headers=headers)

    # clean the result
    new_xml = result.text.replace('&lt;', '<')
    new_xml = new_xml.replace('&gt;', '>')
    new_xml = new_xml.replace(
        """<?xml version='1.0' encoding='UTF-8'?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><doServiceResponse xmlns="http://ocs.ztesoft.com"><doServiceReturn><?xml version="1.0" encoding="UTF-8"?>""", '')
    new_xml = new_xml.replace(
        """</doServiceReturn></doServiceResponse></soapenv:Body></soapenv:Envelope>""", '')

# We get the CUG
    root = etree.fromstring(new_xml)
    return_msg = root.xpath('//zsmart/Data/header/returnMsg')[0].text

    if return_msg == 'Successful':
        print('AdjustBalance request has been executed successfully !')
    else:
        raise Exception('AdjustBalance: ' + return_msg)

    return return_msg
