

def normalize_phone_number(phone):
    phone = phone.strip().replace(' ', '').replace('-', '')
    if phone.startswith('+98'):
        phone = '0' + phone[3:]
    return phone
