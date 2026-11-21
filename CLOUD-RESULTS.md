# Railway cloud validation — 2026-11-21

These checks used isolated projects. Credentials were kept in memory. Test addresses are temporary.

## openttd-cloud

```json
{
  "testedAt": "2026-11-21T12:19:11.307015+00:00",
  "projectId": "7b1c98dc-7c0e-4f72-a194-27b5be333efb",
  "endpoint": "metro.proxy.rlwy.net:22428",
  "checks": {
    "initial_deployment": {
      "id": "4327ff28-47d1-4392-8aa4-5ead687c2093",
      "status": "SUCCESS"
    },
    "initial_public_game_info": {
      "ticks": 1280,
      "date": 712223,
      "companies": 0
    },
    "wrong_password_rejected": true,
    "correct_public_client_join": {
      "encrypted": true,
      "map_complete": true,
      "active": true,
      "frame_ack": true
    },
    "company_created_before_redeploy": {
      "ticks": 1299,
      "date": 712223,
      "companies": 1
    },
    "latest_commit_redeploy_requested": true,
    "redeployment": {
      "id": "97240763-ca01-4852-be93-4034d96ff122",
      "status": "SUCCESS"
    },
    "persisted_public_world_after_redeploy": {
      "ticks": 1299,
      "date": 712223,
      "companies": 1
    },
    "real_client_rejoined_after_redeploy": {
      "active": true,
      "map_complete": true,
      "frame_ack": true
    },
    "result": "PASS"
  },
  "clientContainersRemoved": true
}
```

## openttd-postpublished

```json
{
  "testedAt": "2026-11-21T12:24:05.290785+00:00",
  "projectId": "482c5f94-f1dd-47d7-aa42-f0b55e3d2a5a",
  "endpoint": "shuttle.proxy.rlwy.net:54516",
  "publishedTemplateId": "15932cc4-20a1-48a4-9c42-23c28911e071",
  "templateCode": "openttd",
  "checks": {
    "initial_deployment": {
      "id": "83e47ac1-c341-4fdb-ba58-1f3a452f8bc8",
      "status": "SUCCESS"
    },
    "initial_public_game_info": {
      "ticks": 1280,
      "date": 712223,
      "companies": 0
    },
    "wrong_password_rejected": true,
    "correct_public_client_join": {
      "encrypted": true,
      "map_complete": true,
      "active": true,
      "frame_ack": true
    },
    "result": "PASS",
    "company_created": {
      "ticks": 1316,
      "date": 712223,
      "companies": 1
    }
  },
  "clientContainersRemoved": true,
  "infrastructure_mutations": false,
  "redeployed": false,
  "project_deleted": false
}
```

