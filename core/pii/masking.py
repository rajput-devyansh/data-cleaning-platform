def mask_email(col):
    return f"REGEXP_REPLACE({col}, '(^.).*(@.*$)', '\\1****\\2')"

def mask_phone(col):
    return f"REGEXP_REPLACE({col}, '(\\d{{2}})\\d+(\\d{{2}})', '\\1****\\2')"