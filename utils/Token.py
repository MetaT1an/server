from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


def check_token(token):
    s = Serializer("secrete")
    try:
        data = s.loads(token)  # decrypt from token str
    except (SignatureExpired, BadSignature):
        return None

    return data['id']  # get user id


def gen_token(user_id):
    s = Serializer("secrete", expires_in=3600)
    return s.dumps({'id': user_id}).decode("ascii")  # decode to plain str
