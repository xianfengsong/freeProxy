
# free proxy spider


## mongodb
MONGO_URI = 'mongodb://proxy:proxy@127.0.0.1:9000,127.0.0.1:9001,127.0.0.1:9002/free_proxy'

MONGO_DATABASE = 'free_proxy'

```shell
 use free_proxy;
 db.createUser(
   {
     user: "proxy",
     pwd: "proxy",
     roles: [{role:"readWrite",db:"free_proxy"}]
   }
 )
```
## crontab 

```
*/10 * * * * cd your_path/freeProxy/freeProxy && scrapy crawl free-proxy-list
*/5 * * * *  cd your_path/freeProxy/freeProxy && scrapy crawl check

```