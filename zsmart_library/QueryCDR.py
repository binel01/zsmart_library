import requests
from datetime import datetime, date
from lxml import etree


def QueryCDR(phone_number, billing_cycle, cdr_type=1):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
		<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://com.ztesoft.zsmart/xsd">
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
								<ACTION_ID>QueryCDR</ACTION_ID>
								<REQUEST_ID>00320180529092105</REQUEST_ID>
							</header>
							<body>
					         <MSISDN>phone_number</MSISDN>
					         <BillingCycle>billing_cycle</BillingCycle>
					         <CDRType>cdr_type</CDRType>
					         <PageIndex></PageIndex>
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
    xml = xml.replace("billing_cycle", str(billing_cycle))
    xml = xml.replace("cdr_type", str(cdr_type))

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
        print('QueryCDR request has been executed successfully !')
    else:
        raise Exception('QueryCDR: ' + return_msg)

    return return_msg


def get_last_cdr(phone_number, date_time, cdr_type):
    """
    Gets the last CDR of a phone number
    """
    cdr_type = str.casefold(cdr_type)
    today = date.today()
    billing_cycle = today.strftime("%Y%m")

    new_date = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    res = ""
    if cdr_type == 'voice' or cdr_type == 'sms':
        res = QueryCDR(phone_number, billing_cycle, '1')
    else:
        res = QueryCDR(phone_number, billing_cycle, '2')

        root = etree.fromstring(res)
        res_state = root.xpath('//zsmart/Data/header/returnMsg')[0].text

        event = root.xpath('//zsmart/Data/body/CDRDtoList/CDRDto/Event')
        begin_time = root.xpath(
            '//zsmart/Data/body/CDRDtoList/CDRDto/EventBeginTime')
        duration = root.xpath('//zsmart/Data/body/CDRDtoList/CDRDto/Duration')
        charge_1 = root.xpath('//zsmart/Data/body/CDRDtoList/CDRDto/Charge1')
        acc_name_1 = root.xpath(
            '//zsmart/Data/body/CDRDtoList/CDRDto/AcctResName1')

        response = [0]
        if (res_state == 'Successful'):
            print('The request has been executed successfully !')
            for i in range(0, len(event)):
                begin_time_2 = datetime.strptime(
                    begin_time[i].text, '%Y-%m-%d %H:%M:%S')
                if begin_time_2 >= new_date:
                    response = [event[i].text, begin_time[i].text,
                                duration[i].text, charge_1[i].text, acc_name_1[i].text]
                    break
        else:
            print('The request has failed !')

        return response
