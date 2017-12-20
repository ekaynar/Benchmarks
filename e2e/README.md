# Create Traces and Upload Files into CEPH

## Create Traces 

```
./create_jobs.py <FILE_NAME>
./create_jobs.py sample.input
```

sample.input file has 3 column
```<Date> <Time> <FileNamewithLenght> ```

**create_jobs.py** parses the input file and creates two files called **sample.jobs** and **sample.jobfiles**
sample.jobfiles contains unique files in the traces and their size.

## Upload Traces 
```
./upload.py <FILE_NAME>
./upload.py sample.jobfiles
```
User can set number of threads, swift credentials, bucket and filenames.

