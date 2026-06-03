import re


PHONE_RE = re.compile(r"^(?:8|\+7)\d{10}$")


def clean_phone_string(value):
    if not value:
        return ""
    return value.strip().replace(" ", "").replace("-", "")


def normalize_phone(value):
    phone = clean_phone_string(value)
    if not phone:
        return None

    if phone.startswith("8"):
        return "+7" + phone[1:]
    return phone


def is_valid_phone(value):
    return bool(PHONE_RE.match(clean_phone_string(value)))
