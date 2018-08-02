
import yaml


class Prefix(object):

    async def getPrefix(self):
        with open("prefix_conf.yaml", 'r') as stream:
            try:
                prefix_obj = yaml.load(stream)
                prefix = prefix_obj['prefix']
            except yaml.YAMLError as exc:
                print(exc)
            return prefix

    async def setPrefix(self, msg):
        newprefix = dict(
            prefix=msg,
        )
        with open('prefix_conf.yaml', 'w') as outfile:
            yaml.dump(newprefix, outfile, default_flow_style=False)
        prefix = await self.getPrefix()
        return prefix
