# Show Contest

Show all solve of this contest

**URL** : `/contests/contest/<int:contest_number>/<str:discipline>/`

**Method** : `GET`

**Auth required** : if contest is ongoing YES, elso NO 

**Permissions required** : if contest is ongoing YES, elso NONE

## Success Responses

**Code** : `200 OK`


```json
[
    {
        "id": 11,
        "avg_ms": 17000,
        "discipline": {
            "name": "3by3"
        },
        "user": {
            "username": "antonsav2005"
        },
        "solve_set": [
            {
                "id": 45,
                "time_ms": 5391,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 46,
                "time_ms": 2203,
                "dnf": false,
                "state": "changed_to_extra",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 47,
                "time_ms": 5924,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 48,
                "time_ms": 6112,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 49,
                "time_ms": 984,
                "dnf": false,
                "state": "changed_to_extra",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 50,
                "time_ms": 708,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 51,
                "time_ms": 2128,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            }
        ]
    },
    {
        "id": 12,
        "avg_ms": 17000,
        "discipline": {
            "name": "3by3"
        },
        "user": {
            "username": "savytskyi.work"
        },
        "solve_set": [
            {
                "id": 52,
                "time_ms": 3479,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 53,
                "time_ms": 1772,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 54,
                "time_ms": 7660,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 60,
                "time_ms": 1280,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 61,
                "time_ms": 4397,
                "dnf": false,
                "state": "changed_to_extra",
                "created": "2023-11-01T00:47:33.644764Z"
            },
            {
                "id": 62,
                "time_ms": 13791,
                "dnf": false,
                "state": "submitted",
                "created": "2023-11-01T00:47:33.644764Z"
            }
        ]
    }
]
```
