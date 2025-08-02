
_logins = []

def store_login(user_id, login_date, loc_score, dev_score, ip):
    _logins.append((user_id, login_date, loc_score, dev_score, ip))

def get_all_logins():
    return _logins
