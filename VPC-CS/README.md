# GCP Day 2 - VPC Networking and Cloud Scheduler

1. Create an instance A in default VPC.

Use the following REST equivalent of the instance to create a VM in the default VPC with an external IP. 

**Note:** We are using same custom key-pair generated using **ssh-keygen** tool for logging into both the instances A and B. Hence, the public key needs to be mentioned in the configuration of both instances. Check step 4 for key-pair generation.

```json
POST https://www.googleapis.com/compute/v1/projects/pe-training/zones/us-central1-a/instances
{
  "kind": "compute#instance",
  "name": "instance-a",
  "zone": "projects/pe-training/zones/us-central1-a",
  "machineType": "projects/pe-training/zones/us-central1-a/machineTypes/f1-micro",
  "displayDevice": {
    "enableDisplay": false
  },
  "metadata": {
    "kind": "compute#metadata",
    "items": [
      {
        "key": "ssh-keys",
        "value": "aditya:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7FMqxO7eYDTeYOdpKivWdcEeWicWwhyYQ90vREzUDrE1/MpETRuoYMyKNjMjx9juMTRvn2ckVYW0r9y7VisEvqu0rLqaGBMDEQRc8dmiRUr8IDvVz/0ge/36hWgbC/IJzc0hq4Vd3W9C48c1Nh1wtmQr3Ik3qkSbWwAs6aXPx5iy/msanxnanmvTBZns6sNK7o0LctXsaHLBgs+OVpcrSBRN/tdSZK1RJzHt/qSVbJqEPBcACUwoP23pOvMcGbxHmaI0zxe/9Ytp9vmZlhlQEe+20GCcR5YEs9vlxdaioV+sLpJFppwATEQMnFesj0BA/uZ/fhuEvqtHVGzzCvtdxlZUL185+0VLMyB6cYF3C6s/FGuGzvUXEztZbls9CESnYmbpXdI3wCJKxdYLw92rbDGyp7SwBQWlaF0ABl952YX/IFtA2TOX36YzpKS1Q29/Rxdtsv0p9NnhNS0ZJnfv1icdiBGBAr+ZrBsMk6D0d3rurqL7wZyzzfDWS4iitD4c= aditya@fedora"
      }
    ]
  },
  "tags": {
    "items": []
  },
  "disks": [
    {
      "kind": "compute#attachedDisk",
      "type": "PERSISTENT",
      "boot": true,
      "mode": "READ_WRITE",
      "autoDelete": true,
      "deviceName": "instance-a",
      "initializeParams": {
        "sourceImage": "projects/debian-cloud/global/images/debian-9-stretch-v20191210",
        "diskType": "projects/pe-training/zones/us-central1-a/diskTypes/pd-standard",
        "diskSizeGb": "10"
      },
      "diskEncryptionKey": {}
    }
  ],
  "canIpForward": false,
  "networkInterfaces": [
    {
      "kind": "compute#networkInterface",
      "subnetwork": "projects/pe-training/regions/us-central1/subnetworks/default",
      "accessConfigs": [
        {
          "kind": "compute#accessConfig",
          "name": "External NAT",
          "type": "ONE_TO_ONE_NAT",
          "networkTier": "PREMIUM"
        }
      ],
      "aliasIpRanges": []
    }
  ],
  "description": "",
  "labels": {},
  "scheduling": {
    "preemptible": false,
    "onHostMaintenance": "MIGRATE",
    "automaticRestart": true,
    "nodeAffinities": []
  },
  "deletionProtection": false,
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
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
  ]
}
```

2. Create an instance B in another zone with private IP only, in the same VPC

Use the following REST equivalent to create the other instance.

```json
POST https://www.googleapis.com/compute/v1/projects/pe-training/zones/us-central1-f/instances
{
  "kind": "compute#instance",
  "name": "instance-b",
  "zone": "projects/pe-training/zones/us-central1-f",
  "machineType": "projects/pe-training/zones/us-central1-f/machineTypes/f1-micro",
  "displayDevice": {
    "enableDisplay": false
  },
  "metadata": {
    "kind": "compute#metadata",
    "items": [
      {
        "key": "ssh-keys",
        "value": "aditya:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7FMqxO7eYDTeYOdpKivWdcEeWicWwhyYQ90vREzUDrE1/MpETRuoYMyKNjMjx9juMTRvn2ckVYW0r9y7VisEvqu0rLqaGBMDEQRc8dmiRUr8IDvVz/0ge/36hWgbC/IJzc0hq4Vd3W9C48c1Nh1wtmQr3Ik3qkSbWwAs6aXPx5iy/msanxnanmvTBZns6sNK7o0LctXsaHLBgs+OVpcrSBRN/tdSZK1RJzHt/qSVbJqEPBcACUwoP23pOvMcGbxHmaI0zxe/9Ytp9vmZlhlQEe+20GCcR5YEs9vlxdaioV+sLpJFppwATEQMnFesj0BA/uZ/fhuEvqtHVGzzCvtdxlZUL185+0VLMyB6cYF3C6s/FGuGzvUXEztZbls9CESnYmbpXdI3wCJKxdYLw92rbDGyp7SwBQWlaF0ABl952YX/IFtA2TOX36YzpKS1Q29/Rxdtsv0p9NnhNS0ZJnfv1icdiBGBAr+ZrBsMk6D0d3rurqL7wZyzzfDWS4iitD4c= aditya@fedora"
      }
    ]
  },
  "tags": {
    "items": []
  },
  "disks": [
    {
      "kind": "compute#attachedDisk",
      "type": "PERSISTENT",
      "boot": true,
      "mode": "READ_WRITE",
      "autoDelete": true,
      "deviceName": "instance-b",
      "initializeParams": {
        "sourceImage": "projects/debian-cloud/global/images/debian-9-stretch-v20191210",
        "diskType": "projects/pe-training/zones/us-central1-f/diskTypes/pd-standard",
        "diskSizeGb": "10"
      },
      "diskEncryptionKey": {}
    }
  ],
  "canIpForward": false,
  "networkInterfaces": [
    {
      "kind": "compute#networkInterface",
      "subnetwork": "projects/pe-training/regions/us-central1/subnetworks/default",
      "aliasIpRanges": []
    }
  ],
  "description": "",
  "labels": {},
  "scheduling": {
    "preemptible": false,
    "onHostMaintenance": "MIGRATE",
    "automaticRestart": true,
    "nodeAffinities": []
  },
  "deletionProtection": false,
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
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
  ]
}
```

3. Configure NAT so instance B can access Internet

Use the `gcloud` CLI in the cloud shell or the console for the purpose of creating a Cloud NAT.

```bash
# create a cloud router for the NAT
gcloud compute routers create nat-cloud-router \
  --network a2q2vpc \
  --region us-central1

# create a NAT for the subnet in the given region
gcloud compute routers nats create nat-config \
  --router-region us-central1 \
  --router nat-cloud-router \
  --nat-all-subnet-ip-ranges \
  --auto-allocate-nat-external-ips
# since, there is only one subnet in the given region, we assign NAT to all 
# subnets in the region
```

4. SSH into instance B using instance A and try to install nginx

Use **ssh-keygen** in your local machine or the Cloud Shell to generate a key-pair. By default, the key files are stored in `$HOME/.ssh/` folder with the names as `id_rsa` for the private key and `id_rsa.pub` for the public key. Then add the public key to the SSH forwarding agent using the **ssh-add** tool. Use this public key while you are creating the above instances. Here, I am using a single key-pair for both the instances (better to use different key-pairs for both of the instances, due to security reasons). There after you can `ssh` into the machines.

```bash
# generate key-pair
ssh-keygen
# generates $HOME/.ssh/id_rsa and $HOME/.ssh/id_rsa.pub if you don't specify the path

# add private key to the ssh forwarding agent
ssh-add -k $HOME/.ssh/id_rsa

# SSH into instance A with ssh forwarding agent
ssh -A <username>@<public-ip-of-instance-a>

# SSH into instance B for instance A
<username>@instance-a$ ssh <username>@<private-ip-of-instance-b>

# install nginx in instance B
<username>@instance-b$ sudo apt-get install nginx
```