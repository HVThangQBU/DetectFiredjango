import yaml
path = 'canhbao.config.yml'
with open(path) as f:
  config = yaml.load(f, Loader=yaml.FullLoader)
args = config
