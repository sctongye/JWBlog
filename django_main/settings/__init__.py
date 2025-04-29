__author__ = '@SCTongYe'


import os

# print(os.environ.get('MYSITE_CONFIG'))

if os.environ.get('MYSITE_CONFIG') == "server":
    from .production import *
if os.environ.get('MYSITE_CONFIG') == "pc":
    print("本地 Windows PC 上运行中")
    from .local import *
elif os.environ.get('MYSITE_CONFIG') == "ubuntu_p73":
    print("本地 Linux Ubuntu P73 上运行中")
    from .local import *
else:
    from .production import *