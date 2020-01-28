# Day 3 GCP - Cloud Functions, StackDriver, Pub/Sub

#### 1. Steps to export all the logs related to firewall rules to BigQuery for further analysis. Use console.

##### Enable Logging for the firewall rules you want to get logs from.
  - Go to the **Firewall rules** page in the Google Cloud Console.
  - Select the firewall rule that you want to update.
  - Click **Edit**.
  - For the Logs setting, select **On**.
  - Click **Save**.

##### Create Sinks
  - Go to the **StackDriver Logs Viewer** page in console.
  - Click on **Create Sink**, and fill in the **Edit Export** panel as follows.
    - Set a **filter** to show all logs related to firewall rules.
      ```
      resource.type="gce_subnetwork" AND
      log_name="projects/pe-training/logs/compute.googleapis.com%2Ffirewall"
      ```
    - Set the **Sink name**.
    - Select **Sink Service** as **Bigquery**.
    - In **Sink Destination**, **create a new dataset** and give it a suitable name.
    - Click **Create Sink**
  - Go to **Logs Router** page to check that the log exporter is created.

#### 2. Configure Apache2 HTTP server on a GCE VM instance and setup an email alert notification which triggers when the health check of the instance fails. Use console. 

##### Create an instance from the given REST equivalent, with a custom generated **ssh** key-pair
```json
{
  "canIpForward": false,
  "cpuPlatform": "Unknown CPU Platform",
  "creationTimestamp": "2020-01-27T05:23:21.997-08:00",
  "deletionProtection": false,
  "description": "",
  "disks": [
    {
      "autoDelete": true,
      "boot": true,
      "deviceName": "alert-instance",
      "diskSizeGb": "10",
      "guestOsFeatures": [
        {
          "type": "VIRTIO_SCSI_MULTIQUEUE"
        }
      ],
      "index": 0,
      "interface": "SCSI",
      "kind": "compute#attachedDisk",
      "licenses": [
        "projects/debian-cloud/global/licenses/debian-9-stretch"
      ],
      "mode": "READ_WRITE",
      "source": "projects/pe-training/zones/us-central1-a/disks/alert-instance",
      "type": "PERSISTENT"
    }
  ],
  "displayDevice": {
    "enableDisplay": false
  },
  "id": "740139428374338214",
  "kind": "compute#instance",
  "labelFingerprint": "42WmSpB8rSM=",
  "machineType": "projects/pe-training/zones/us-central1-a/machineTypes/f1-micro",
  "metadata": {
    "fingerprint": "ooekqljsH_Y=",
    "items": [
      {
        "key": "startup-script",
        "value": "#!/bin/bash\napt-get update\napt-get install -y apache2\necho '<h1>Hello World</h1>' > /var/www/html/index.html"
      },
      {
        "key": "ssh-keys",
        "value": "aditya:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7FMqxO7eYDTeYOdpKivWdcEeWicWwhyYQ90vREzUDrE1/MpETRuoYMyKNjMjx9juMTRvn2ckVYW0r9y7VisEvqu0rLqaGBMDEQRc8dmiRUr8IDvVz/0ge/36hWgbC/IJzc0hq4Vd3W9C48c1Nh1wtmQr3Ik3qkSbWwAs6aXPx5iy/msanxnanmvTBZns6sNK7o0LctXsaHLBgs+OVpcrSBRN/tdSZK1RJzHt/qSVbJqEPBcACUwoP23pOvMcGbxHmaI0zxe/9Ytp9vmZlhlQEe+20GCcR5YEs9vlxdaioV+sLpJFppwATEQMnFesj0BA/uZ/fhuEvqtHVGzzCvtdxlZUL185+0VLMyB6cYF3C6s/FGuGzvUXEztZbls9CESnYmbpXdI3wCJKxdYLw92rbDGyp7SwBQWlaF0ABl952YX/IFtA2TOX36YzpKS1Q29/Rxdtsv0p9NnhNS0ZJnfv1icdiBGBAr+ZrBsMk6D0d3rurqL7wZyzzfDWS4iitD4c= aditya@fedora"
      }
    ],
    "kind": "compute#metadata"
  },
  "name": "alert-instance",
  "networkInterfaces": [
    {
      "accessConfigs": [
        {
          "kind": "compute#accessConfig",
          "name": "External NAT",
          "networkTier": "PREMIUM",
          "type": "ONE_TO_ONE_NAT"
        }
      ],
      "fingerprint": "vfgFqAcj8eI=",
      "kind": "compute#networkInterface",
      "name": "nic0",
      "network": "projects/pe-training/global/networks/default",
      "networkIP": "10.128.0.71",
      "subnetwork": "projects/pe-training/regions/us-central1/subnetworks/default"
    }
  ],
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
  },
  "scheduling": {
    "automaticRestart": true,
    "onHostMaintenance": "MIGRATE",
    "preemptible": false
  },
  "selfLink": "projects/pe-training/zones/us-central1-a/instances/alert-instance",
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
  "startRestricted": false,
  "status": "PROVISIONING",
  "tags": {
    "fingerprint": "FYLDgkTKlA4=",
    "items": [
      "http-server"
    ]
  },
  "zone": "projects/pe-training/zones/us-central1-a"
}
```

##### SSH into the instance and run the following commands to install the monitoring and logging agent in the instance

```bash
ssh -i id_rsa.pub <user-name>@<public-ip-of-instance>

<user-name>@<instance-host-name>$curl -sSO https://dl.google.com/cloudagents/install-monitoring-agent.sh
<user-name>@<instance-host-name>$sudo bash install-monitoring-agent.sh

<user-name>@<instance-host-name>$curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
<user-name>@<instance-host-name>$sudo bash install-logging-agent.sh --structured
```
##### Create Uptime Health Check and Alerting policy

- Go to the [Monitoring Overview](https://console.cloud.google.com/monitoring).
- Under **Create uptime check**, select **CREATE CHECK** and fill the details for the instance as shown below.

![create_uptime_hc](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/uptime_health_check.png)

- After hitting the **Save** button, you will be prompted to create a Alerting Policy for it. Go ahead and fill the details as follow:

![create_alert_policy](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/alerting_policy.png)

- Hit **Save**, click on **ADD CONDITION** and fill in the details for the CPU utilization condition.

![create_cpu_condtion](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/cpu_utilisation_condition.png)

- **ADD** and next click on **ADD NOTIFICATION CHANNEL**, select **email** from the dropdown menu and provide your email address to recieve the alerts.

- After the above the alert should look something like the following in the console:

![pol_1](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/policy_1.png)

![pol_2](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/policy_2.png)


##### Alert message for failing uptime health check:

![alert_uptime](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/alert_uptime.png)

##### Alert message for crossing CPU utilization:

![alert_cpu](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/alert_cpu_util.png)

**The following was the CPU utilization while a spike in CPU was caused.**

![cpu_spike](https://raw.githubusercontent.com/adityaprakash-bobby/q-gcp-assessment/master/assets/cpu_spike.png)

#### 3. Create a Cloud Function to convert the pub/sub message to json file and store it in GCS bucket

The solution for the cloud functions is provided in the following `store_gcs.py` and `requirements.txt` file.
 - [store_gcs.py](https://github.com/adityaprakash-bobby/q-gcp-assessment/blob/master/Cloud-Functions-PubSub-SD/store_gcs.py) with function to execute as `store_pubsub`.
 - [requirements.txt](https://github.com/adityaprakash-bobby/q-gcp-assessment/blob/master/Cloud-Functions-PubSub-SD/requirements.txt)