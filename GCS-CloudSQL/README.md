# Day 4 GCP - GCS and Cloud SQL

#### 1. Host a static website using GCS bucket.

- Create a bucket 
- Add a file named `index.html` in it from the local system
- Make the above file public or make a group of files public that are to be serverd by the statuc site
```bash
gsutil acl ch -u AllUsers:R gs://gcsrandomname/index.html
```
- Access the file link from the console to get the following output.

#### 2. Create a folder structure in the bucket as follows (manually). Download the entire folder (folder1) on the local (cloud shell or vm) using python3 with standard library: 
 	
    ```
     folder1/
        ├── file1.txt
        └── folder2
            └── file2.txt
    ```

Follow the script for the above task. 
    - [script_download.py](https://github.com/adityaprakash-bobby/q-gcp-assessment/blob/master/GCS-CloudSQL/script_download.py)