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
                "scramble": {
                    "position": "1"
                }
            },
            {
                "id": 46,
                "time_ms": 2203,
                "dnf": false,
                "state": "changed_to_extra",
                "scramble": {
                    "position": "2"
                }
            },
            {
                "id": 47,
                "time_ms": 5924,
                "dnf": false,
                "state": "submitted",
                "scramble": {
                    "position": "E1"
                }
            },
            {
                "id": 48,
                "time_ms": 6112,
                "dnf": false,
                "state": "submitted",
                "scramble": {
                    "position": "3"
                }
            },
            {
                "id": 49,
                "time_ms": 984,
                "dnf": false,
                "state": "changed_to_extra",
                "scramble": {
                    "position": "4"
                }
            },
            {
                "id": 50,
                "time_ms": 708,
                "dnf": false,
                "state": "submitted",
                "scramble": {
                    "position": "E2"
                }
            },
            {
                "id": 51,
                "time_ms": 2128,
                "dnf": false,
                "state": "submitted",
                "scramble": {
                    "position": "5"
                }
            }
        ]
    },
    {
        "id": 5,
        "avg_ms": null,
        "discipline": {
            "name": "3by3"
        },
        "solve_set": [
          
        ]
    }
]
```
