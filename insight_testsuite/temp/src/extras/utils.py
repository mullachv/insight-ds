import datetime
def is_valid_zip(zip_code):
    if zip_code is None:
        return False

    if len(zip_code.strip()) < 5:
        return False

    return True

def cleansed_zip(zip_code):
    return zip_code.strip()[0:5]

def is_valid_date(dt):
    try:
        datetime.datetime.strptime(dt, '%m%d%Y')
        return True
    except ValueError:
        return False

