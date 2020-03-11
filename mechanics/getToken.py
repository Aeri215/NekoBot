import yaml


class GetToken(object):

    @staticmethod
    def get_token():
        with open("Static/token.yaml", 'r') as stream:
            token_obj = yaml.load(stream, Loader=yaml.FullLoader)
            token = token_obj["token"]
        return token
