import re


class Utils (object):
    async def clean_number(str) :
        return re.sub("[^0-9][+\-*/]", "", str)
