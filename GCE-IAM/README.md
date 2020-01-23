# Assessment Day 4 - IAM and GCE

### Configure a vm with 10 GB disk. Once launched, increase the disk size to 50GB. Verify it on system. Use CLI only.

```bash
# Provision an instance with 10GB boot disk
gcloud compute instances create gcp-aditya \
    --machine-type f1-micro \
    --image-family ubuntu-1604-lts \
    --image-project ubuntu-os-cloud \
    --boot-disk-size 10GB  \
    --zone us-east1-b
```
![create_vm](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/vm_create.png)

```bash
# Provision the disk attached to the VM for 50GB
gcloud compute disks resize gcp-aditya --zone=us-east1-b --size 50

# Restart the instance to make the changes affect inside the VM
gcloud compute instances stop gcp-aditya --zone=us-east1-b
gcloud compute instances start gcp-aditya --zone=us-east1-b
```
![vm_resize_disk](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/vm_resize.png)


### Configure HTTPS load balancer with  2 instances in MIG. install apache and a sample index page. Your load should be balanced on all 2 VMs.


### Create a bucket. Do the following operations with CLI.
   
```bash
# Create a bucket
gsutil mb gs://gcpbucketaditya/

# Create second bucket for later operations
gsutil mb gs://gcpbucketaditya2/

# Create files for transfer operations
echo 'this is a test file.' > testfile.txt
echo 'this is another test file' > testfile2.txt
```

```bash
# Transfer a local file from PC to the bucket
gsutil cp testfile.txt gs://gcpbucketaditya/

# Transfer another file to the same bucket as above for other operations
gsutil cp testfile2.txt gs://gcpbucketaditya/

# Remove the local 'testfile2.txt' in your PC
rm testfile2.txt
```
![file_cp](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/bucket_cp_file.png)


```bash
# Transfer file from one bucket to another
gsutil cp gs://gcpbucketaditya/testfile.txt gs://gcpbucketaditya2/
```
![file_transfer](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/bucket_transfer.png)

```bash
# Download a file from bucket to the local PC
gsutil cp -m gs://gcpbucketaditya/testfile2.txt .
```
![file_download](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/bucket_file_download.png)


```bash
# List all the objects within a bucket
gsutil ls -r gs://gcpbucketaditya/**
```
![bucket_ls](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/bucket_ls.png)

```bash
# Delete all objects in a bucket, not the bucket
gsutil rm gs://gcpbucketaditya/**
```
![file_rm](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/bucket_rm.png)
