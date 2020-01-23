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

- Instance Template

```json
{
  "creationTimestamp": "2020-01-23T10:34:06.295-08:00",
  "description": "",
  "id": "8682670952485771761",
  "kind": "compute#instanceTemplate",
  "name": "lb-ig",
  "properties": {
    "scheduling": {
      "onHostMaintenance": "MIGRATE",
      "automaticRestart": true,
      "preemptible": false
    },
    "tags": {
      "items": [
        "http-server"
      ]
    },
    "disks": [
      {
        "type": "PERSISTENT",
        "deviceName": "lb-ig",
        "autoDelete": true,
        "index": 0.0,
        "boot": true,
        "kind": "compute#attachedDisk",
        "mode": "READ_WRITE",
        "initializeParams": {
          "sourceImage": "projects/debian-cloud/global/images/debian-9-stretch-v20191210",
          "diskType": "pd-standard",
          "diskSizeGb": "10"
        }
      }
    ],
    "networkInterfaces": [
      {
        "network": "projects/pe-training/global/networks/default",
        "accessConfigs": [
          {
            "name": "External NAT",
            "type": "ONE_TO_ONE_NAT",
            "kind": "compute#accessConfig",
            "networkTier": "PREMIUM"
          }
        ],
        "kind": "compute#networkInterface"
      }
    ],
    "reservationAffinity": {
      "consumeReservationType": "ANY_RESERVATION"
    },
    "canIpForward": false,
    "machineType": "f1-micro",
    "metadata": {
      "fingerprint": "IN4LBIix3Eo=",
      "kind": "compute#metadata",
      "items": [
        {
          "value": "#!/bin/bash\napt-get update\napt-get install -y apache2\necho \"<h1>Hello! This is $(date | md5sum)</h1>\" > /var/www/html/index.html\nsystemctl start apache2\nsystemctl enable apache2",
          "key": "startup-script"
        }
      ]
    },
    "serviceAccounts": [
      {
        "email": "912623308461-compute@developer.gserviceaccount.com",
        "scopes": [
          "https://www.googleapis.com/auth/devstorage.read_only",
          "https://www.googleapis.com/auth/logging.write",
          "https://www.googleapis.com/auth/monitoring.write",
          "https://www.googleapis.com/auth/servicecontrol",
          "https://www.googleapis.com/auth/service.management.readonly",
          "https://www.googleapis.com/auth/trace.append"
        ]
      }
    ],
    "displayDevice": {
      "enableDisplay": false
    }
  },
  "selfLink": "projects/pe-training/global/instanceTemplates/lb-ig"
}
```

- Instancee group config

```json
POST https://www.googleapis.com/compute/v1/projects/pe-training/global/healthChecks
{
  "kind": "compute#healthCheck",
  "name": "lb-ig-healthcheck",
  "description": "",
  "checkIntervalSec": 5,
  "timeoutSec": 5,
  "unhealthyThreshold": 3,
  "healthyThreshold": 2,
  "selfLink": "projects/pe-training/global/healthChecks/lb-ig-healthcheck",
  "type": "HTTP",
  "httpHealthCheck": {
    "port": 80,
    "host": "",
    "requestPath": "/",
    "response": null,
    "proxyHeader": "NONE"
  },
  "httpsHealthCheck": null,
  "http2HealthCheck": null,
  "tcpHealthCheck": null,
  "sslHealthCheck": null,
  "udpHealthCheck": null
}

POST https://www.googleapis.com/compute/beta/projects/pe-training/regions/us-central1/instanceGroupManagers
{
  "name": "lb-ig-instance-grp",
  "instanceTemplate": "projects/pe-training/global/instanceTemplates/lb-ig",
  "baseInstanceName": "lb-ig-int-gw",
  "targetSize": 1,
  "autoHealingPolicies": [
    {
      "initialDelaySec": 300,
      "healthCheck": "projects/pe-training/global/healthChecks/lb-ig-healthcheck"
    }
  ],
  "distributionPolicy": {
    "zones": [
      {
        "zone": "projects/pe-training/zones/us-central1-b"
      },
      {
        "zone": "projects/pe-training/zones/us-central1-c"
      },
      {
        "zone": "projects/pe-training/zones/us-central1-f"
      }
    ]
  }
}

POST https://www.googleapis.com/compute/beta/projects/pe-training/regions/us-central1/autoscalers
{
  "name": "lb-ig-int-gw",
  "target": "projects/pe-training/regions/us-central1/instanceGroupManagers/lb-ig-int-gw",
  "region": "us-central1",
  "kind": "compute#autoscaler",
  "autoscalingPolicy": {
    "cpuUtilization": {
      "utilizationTarget": 0.1
    },
    "mode": "ON",
    "coolDownPeriodSec": 60,
    "minNumReplicas": 1,
    "maxNumReplicas": 3
  }
}
```
![mig](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/mig.png)

- LoadBalancer

![lb](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/loadbalancer.png)

- Outputs on hitting the load-balancer

![op_1](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/op_1.png)
![op_2](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/op_2.png)
![op_3](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/op_3.png)





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
