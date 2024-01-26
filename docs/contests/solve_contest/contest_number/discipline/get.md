# Show data to solve ongoing contest

**URL** : `/api/contests/solve_contest/<int:contest_number>/<str:discipline>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : Did not solve this contest

## Success Responses

**Code** : `200 OK`


```json
{
    "submitted_solves": [
        {
            "id": 73,
            "time_ms": 2541,
            "dnf": false,
            "scramble": {
                "scramble": "B2 R' U",
                "extra": false,
                "id": 15,
                "position": "1"
            }
        },
        {
            "id": 75,
            "time_ms": 4556,
            "dnf": false,
            "scramble": {
                "scramble": "R2 U F",
                "extra": true,
                "id": 20,
                "position": "E1"
            }
        },
        {
            "id": 76,
            "time_ms": 1364,
            "dnf": false,
            "scramble": {
                "scramble": "R2 F' B2",
                "extra": false,
                "id": 17,
                "position": "3"
            }
        }
    ],
    "current_solve": {
        "scramble": {
            "id": 23,
            "scramble": "B2 D' B'",
            "extra": false,
            "position": "2"
        },
        "solve": {
            "id": null,
            "time_ms": null,
            "dnf": false
        },
        "can_change_to_extra": true
    }
}
     
```
