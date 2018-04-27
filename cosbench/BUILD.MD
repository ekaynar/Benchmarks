# Below are steps to build Cocbench from source code using Eclipse:

* Download Eclipse SDK from [here](https://www.eclipse.org/downloads/)
* Clone the source code from Cosbench [repo](https://github.com/intel-cloud/cosbench) or download the source code from [releases](https://github.com/intel-cloud/cosbench/releases)
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
* Cosbench changing system clock [issue](https://github.com/intel-cloud/cosbench/issues/340) which is causing error on pbench. To resolve the problem
Open "cosbench/dev/cosbench-driver-web/src/com/intel/cosbench/driver/handler/PingHandler.java" and remove the line
  ```setSysTime(getControllerTime(scanner));```

# Compile and build the source code
* Select all projects and right click and select "Export -> Plug-in Development -> Deployable plugins and fragments"
* Set the "Directory" to "dist\osgi" folder. Then the plugins library will be placed at "dist\osgi\plugins" folder.
* Run  ```pack.sh <version number>``` from cosbench directory.
