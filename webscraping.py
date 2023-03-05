from __future__ import print_function
import time
import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException
from pprint import pprint


def main(barcode_value):
    # Configure API key authorization: Apikey
    configuration = cloudmersive_barcode_api_client.Configuration()
    configuration.api_key['Apikey'] = '015101df-59d7-47a2-80f5-c445ca6942bd'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['Apikey'] = 'Bearer'
    # create an instance of the API class
    api_instance = \
        cloudmersive_barcode_api_client.BarcodeLookupApi(cloudmersive_barcode_api_client.ApiClient(configuration))

    value = barcode_value  # str | Barcode value

    try:
        # Lookup a barcode value and return product data
        api_response = api_instance.barcode_lookup_ean_lookup(value)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BarcodeLookupApi->barcode_lookup_ean_lookup: %s\n" % e)

