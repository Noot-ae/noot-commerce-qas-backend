from rest_framework.views import exception_handler


def extract_buried_list(key, data):
    if isinstance(data, dict):            
        for key, value in data.items():
            return {key: extract_buried_list(key, value)}            

    elif isinstance(data, list) :                
        if isinstance(data[0], str):
            return {key : data[0]}
        elif isinstance(data[0], dict):
            for key, value in data[0].items():                    
                return extract_buried_list(key, value)

    return {key : data}

def api_handler(exc, context):
    # Call the default DRF exception handler
    response = exception_handler(exc, context)    
    
    if response is None:
        return 
    # Get the translated error message for the exception
    data = response.data

    if hasattr(exc, 'get_codes'):
        codes = exc.get_codes()
        if isinstance(codes, dict):
            response.data = [extract_buried_list(key, value) for key, value in codes.items()]
        else:
            response.data = [{"code" : codes}]
    return response

    # Get the translated error message for the exception
    data = response.data
    if not type(data) == list:
        response.data = [data]
    return response
