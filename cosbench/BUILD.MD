# Below are steps to build Cocbench from source code using Eclipse SDK:

* Download Eclipse SDK from [here](https://www.eclipse.org/downloads/)
* Download Source code from github repo or from releases:
  * Clone the source code from Cosbench [github repo](https://github.com/intel-cloud/cosbench).  
     ```
     git clone https://github.com/intel-cloud/cosbench.git
     git checkout -b v0.4.2
     git checkout remotes/origin/0.4.2.0
     git branch -vv
     ```
  * Download the source code from [releases](https://github.com/intel-cloud/cosbench/releases)
     ``` 
     wget https://github.com/intel-cloud/cosbench/archive/v0.4.2.tar.gz
     tar -xvzf v0.4.2.tar.gz
     ```
* Open Eclipse SDK
  * Select "File -> Import -> General -> Existeing Projects into Workspace"
  * Select the root directory to the "dev" folder in cosbench and click "Finish".
  * Eclipse imports all projects and there will be error signs on projects.   

* Resolving error signs on projects
  * Select "Eclipse -> Preferences -> Plug-in Development -> Target Platform",
  * Select "Running Platform (Active) " and click "Edit" button to add required plugins.
  * Select the 3 folders located under "cosbench/dist" directory
    * main 
    * osgi
    * osgi\libs
  * After added those folders, then apply changes.
  * Go to "cosbench/dev/cosbench-openio" folder and create "test" folder and Refresh the project.
  
* Those error signs should disappear, then the development environment is ready.

# Modification of for the v0.4.2 (Optional)

* Currently released version (0.4.2) has a problem that can not be used. I follow the following code modification to resolve the problem.
https://github.com/intel-cloud/cosbench/pull/373
 * [Correct the wrong library path](https://github.com/intel-cloud/cosbench/pull/373/commits/0d263f171091539de834aec726b7809b13241232)
 * [Remove unnecessary metadata of cosbench-ecs](https://github.com/intel-cloud/cosbench/pull/373/commits/44a51247d7600c868f829883c9140d483caa9f95)
 * [Add a default configuration for importing cosbench-ecs project](https://github.com/intel-cloud/cosbench/pull/373/commits/3807991edb05a9f81c9ecfc65d45cab9f0382039)
 * [Modify the version(0.4.1) of the MANIFEST.MF files to be the same as the version(0.4.2) recorded in the VERSION file for linux users.](https://github.com/intel-cloud/cosbench/pull/373/commits/8958eef1e6cded294fc11d1e79f2eaf7414a13f3)

* Cosbench changing system clock [issue](https://github.com/intel-cloud/cosbench/issues/340) which is causing error on pbench. To resolve the problem
 * Open "cosbench/dev/cosbench-driver-web/src/com/intel/cosbench/driver/handler/PingHandler.java" and remove the line
   ```setSysTime(getControllerTime(scanner));```

# Compile and build the source code
* Select all projects and right click and select "Export -> Plug-in Development -> Deployable plugins and fragments"
* Set the "Directory" to "dist\osgi" folder. Then the plugins library will be placed at "dist\osgi\plugins" folder.
* Run  ```pack.sh <version number>``` from cosbench directory.

# Minor Fix
* If you are using centos/Rhel please edit "cosbench-start.sh" file
 ```TOOL_PARAMS=""```
