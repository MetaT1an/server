auth_fail_msg = {'status': False, 'msg': "authorization failed"}

token_invalid_msg = {'status': False, 'msg': "token expired, please login again"}

success_msg = {'status': True, 'data': ""}

no_resource_msg = {'status': False, 'msg': "resource missing"}

invalid_data_msg = {'status': False, 'msg': "invalid data"}

deny_msg = {'status': False, 'msg': "permission deny"}


def error_msg(error_info):
    return {'status': False, 'msg': error_info}
