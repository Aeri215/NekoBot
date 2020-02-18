import yaml


class Prefix(object):

    async def getPrefix(self):
        with open("Static/Prefix/prefix.yaml", 'r') as stream:
            try:
                prefix_obj = yaml.load(stream, Loader=yaml.FullLoader)
                prefix = prefix_obj['prefix']
            except yaml.YAMLError as exc:
                print(exc)
            return prefix

    async def setPrefix(self, msg):
        msg = str(msg)
        newprefix = dict(
            prefix=msg,
        )
        with open('Static/Prefix/prefix.yaml', 'w') as outfile:
            yaml.dump(newprefix, outfile, default_flow_style=False)
        prefix = await self.getPrefix()
        return prefix
