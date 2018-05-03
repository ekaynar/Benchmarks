# RGW Installation
Make sure you have the admin keyrings and ceph.conf file
```
yum -y install ceph-deploy
yum -y install ceph-radosgw
ceph-deploy install --rgw <rgw_name>
ceph-deploy admin <rgw_name>
ceph-deploy rgw create <rgw_name>
````


# Delete Exising Pools
```
systemctl stop ceph-radosgw@rgw.<rgw_name>
for i in `ceph df|grep rgw|awk '{print $1}'`;do ceph osd pool set $i nodelete 0 ;done
for i in `ceph df|grep rgw|awk '{print $1}'`;do rados rmpool $i $i --yes-i-really-really-mean-it ;done
```

# Multi-Side Installation
We will have two RGWs, each poiting to different set of pools. 
We create unique "realm", "zonegroup" and "zone" per RGW. 
RGWs will share the same Ceph cluster.

* Setup First RGW
  * Create a Realm 
  ```
  radosgw-admin realm create --rgw-realm=realm1
  ```
   * Create a Zonegroup
  ```
  radosgw-admin zonegroup create --rgw-zonegroup=production --endpoints=http://<rgw_name>:80 --rgw-realm=realm1 --master --default
  ```
  * Create a Zone
  ``` 
  radosgw-admin zone create --rgw-zonegroup=production --rgw-zone=production_zone --access-key=$SYSTEM_ACCESS_KEY --secret=$SYSTEM_SECRET_KEY --rgw-realm=realm1 --master --endpoints=http://<rgw_name>:80
  ```
  * Delete the "default" pools in your Ceph storage cluster if they exist.
  ```
  radosgw-admin zonegroup remove --rgw-zonegroup=default --rgw-zone=default
  radosgw-admin zone delete --rgw-zone=default
  radosgw-admin zonegroup delete --rgw-zonegroup=default  
  ```
  * Update the period
  ```
  radosgw-admin period update --commit --rgw-realm=realm1
  ```
 
 * Setup Second RGW
   * Create a Realm 
    ```
    radosgw-admin realm create --rgw-realm=realm2
    ```
   * Create a Zonegroup
    ```
    radosgw-admin zonegroup create --rgw-zonegroup=experiment --endpoints=http://<rgw_name>:80 --rgw-realm=realm2 --master --default
    ```
   * Create a Zone
    ```
    radosgw-admin zone create --rgw-zonegroup=experiment --rgw-zone=experiment_zone --access-key=$SYSTEM_ACCESS_KEY --secret=$SYSTEM_SECRET_KEY --rgw-realm=realm2 --master --endpoints=http://<rgw_name>:80
    ```
   * Delete the "default" pools in your Ceph storage cluster if they exist.
    ```
    radosgw-admin zonegroup remove --rgw-zonegroup=default --rgw-zone=default
    radosgw-admin zone delete --rgw-zone=default
    radosgw-admin zonegroup delete --rgw-zonegroup=default  
    ```
    * Update the period
   ```
   radosgw-admin period update --commit --rgw-realm=realm2
   ```
  
 # Edit RGW Configurations
 Add the following lines into /etc/ceph/ceph.conf on both RGW hosts.
  * RGW 1
   ```
   [client.rgw.<rgw1_name>]
   rgw_zonegroup = production
   rgw_zone = production_zone
   rgw_realm = realm1
   rgw_frontends = "civetweb port=80"
   ```
 * RGW 2
   ```
   [client.rgw.<rgw2_name>]
   rgw_zonegroup = experiment
   rgw_zone = experiment_zone
   rgw_realm = realm2
   rgw_frontends = "civetweb port=80"
   ```
 
 # Restart RGW
 ```
 systemctl start ceph-radosgw@rgw.`hostname -s`
 ```
 
 # Check Created Pools
 run the "ceph df" command. You should see seperate set of pools
 ```
    .rgw.root                  232      11517         0        29864G          36
    production_zone.rgw.control           233          0         0        29864G           8
    production_zone.rgw.meta              234       1432         0        29864G           9
    production_zone.rgw.log               235         63         0        29864G         178
    production_zone.rgw.buckets.index     239          0         0        29864G           2
    production_zone.rgw.buckets.data      240        879         0        29864G           2
    experiment_zone.rgw.control           236          0         0        29864G           8
    experiment_zone.rgw.meta              237       1416         0        29864G           9
    experiment_zone.rgw.log               238         89         0        29864G         178
    experiment_zone.rgw.buckets.data      241      30400         0        29864G           3
    experiment_zone.rgw.buckets.index     242          0         0        29864G           2
 ``` 
# Create RGW Users
    * Create User for First RGW
      ```
      radosgw-admin user create --uid=ugur --display-name="ugur" --email=ugur@example.com --rgw-zonegroup=experiment --rgw-zone=experiment_zone
      adosgw-admin subuser create --uid=ugur --subuser=ugur:swift --access=full --rgw-zonegroup=experiment --rgw-zone=experiment_zone
      ```
      
    * Create User for Second RGW
      ```
      radosgw-admin user create --uid=orran --display-name="orran" --email=orran@example.com --rgw-zonegroup=production --rgw-zone=production_zone
      adosgw-admin subuser create --uid=orran --subuser=orran:swift --access=full --rgw-zonegroup=production --rgw-zone=production_zone
      ```
   
   
   
   
   
