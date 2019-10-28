
# free proxy spider

## mongodb

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
