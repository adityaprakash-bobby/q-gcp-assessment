# GCP Day 2 - VPC Networking and Cloud Scheduler

1. Create a instance in default VPC

Use the following REST equivalent of the instance to create a VM in the default VPC with an external IP.

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