
项目描述:
分布式爬虫爬取免费代理服务器ip地址,获取数据后将其存储在mongodb中,通过web界面展示获取到的数据,并能够在web界面上对相应字段进行查询


分布式实现:
redis

存储:
mongodb

爬虫状态显示:
graphite

TODO
web界面展示部分(待做):
flask

python库依赖问题
解决思路
virtualenv virtualenvwrapper管理python 库依赖问题

TODO
部署方式
docker

mongodb存储字段
database:proxyip_data
collection:proxyip_collection

存储内容包括
ip  端口  类型  所在地区

