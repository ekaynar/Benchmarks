# Below are steps to build Cosbench from source code using Eclipse SDK:
## Download Source Code
* Download Cosbench source code either from github repo or from releases:
  * To download it from [github repo](https://github.com/intel-cloud/cosbench).  
     ```
     git clone https://github.com/intel-cloud/cosbench.git
     git checkout -b v0.4.2
     git checkout remotes/origin/0.4.2.0
     git branch -vv
     ```
  * To download it from [releases](https://github.com/intel-cloud/cosbench/releases)
     ``` 
     wget https://github.com/intel-cloud/cosbench/archive/v0.4.2.tar.gz
     tar -xvzf v0.4.2.tar.gz
     ```
## Download Eclipse SDK
* Download **Eclipse SDK** from [here](https://www.eclipse.org/downloads/)

## Import Cosbench source code into Eclipse SDK
* Open Eclipse SDK
  * Select "File -> Import -> General -> Existeing Projects into Workspace"
  * Select the "dev" folder in cosbench as a root directory and click "Finish" button.
  * Eclipse imports all projects in workspace. After the code is imported, there will be error signs on multiple projects.   

## Resolving error signs on projects
* Import existing Cosbench plug-ins into target platform
  * Select "Eclipse -> Preferences -> Plug-in Development -> Target Platform",
  * Select "Running Platform (Active) " and click "Edit" button to add required plugins.
  * Select the 3 folders located under "cosbench/dist" directory
      * main 
      * osgi
      * osgi\libs
  * After added those folders, then apply changes.
 
* Cosbench-openio shows an error says "test/ is missing from source"
  ```
  cd CosbenchHOME$/dev/cosbench-openio
  mkdir test
  ```
 
* If you want to run Cosbench with Pbench
    * Cosbench changing system clock [issue](https://github.com/intel-cloud/cosbench/issues/340) which is causing error on pbench. To resolve the problem, open "cosbench/dev/cosbench-driver-web/src/com/intel/cosbench/driver/handler/PingHandler.java" and remove the line
      ```
      ///setSysTime(getControllerTime(scanner));
      ```
 * **(For released version only) Modification for the v0.4.2**
     * Currently released version (0.4.2) has a problem that can not be used. I follow the following code modification to resolve the problem. https://github.com/intel-cloud/cosbench/pull/373
     * [Correct the wrong library path](https://github.com/intel-cloud/cosbench/pull/373/commits/0d263f171091539de834aec726b7809b13241232)
     * [Remove unnecessary metadata of cosbench-ecs](https://github.com/intel-cloud/cosbench/pull/373/commits/44a51247d7600c868f829883c9140d483caa9f95)
     * [Add a default configuration for importing cosbench-ecs project](https://github.com/intel-cloud/cosbench/pull/373/commits/3807991edb05a9f81c9ecfc65d45cab9f0382039)
     * [Modify the version(0.4.1) of the MANIFEST.MF files to be the same as the version(0.4.2) recorded in the VERSION file for linux users.](https://github.com/intel-cloud/cosbench/pull/373/commits/8958eef1e6cded294fc11d1e79f2eaf7414a13f3)

 * All error signs should disappear, then the development environment is ready.

# Compile and build the source code
* Select all projects and right click and select "Export -> Plug-in Development -> Deployable plugins and fragments"
* Set the "Directory" to "dist\osgi" folder. Then the plugins library will be placed at "dist\osgi\plugins" folder.
* Run  ```pack.sh <version number>``` from cosbench directory.

# Minor Fix when you run Cosbench on CentOS/Rhel System
* If you are using centos/Rhel please edit "cosbench-start.sh" file
 ```
 cd CosbenchHOME$/<version number>
 vim cosbench-start.sh
 ```
 * Edit the TOOL_PARAMS parameter
 ```
 TOOL_PARAMS=""
 ```
