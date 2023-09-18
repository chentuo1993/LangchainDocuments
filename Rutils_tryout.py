import rutils
rutils.memento()  # use memento to authenticate if it exists
host = "cmedge003.usmsc18.pie.apple.com"
conn = rutils.RemoteFSHook(host)