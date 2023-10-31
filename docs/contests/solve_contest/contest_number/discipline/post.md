# Save solve

**URL** : `/api/contests/solve_contest/<int:contest_number>/<str:discipline>/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : YES

**Data to send**

```json
{
    "dnf": true
}
```

or

```json
{
    "reconstruction": "B2 L2 R2",
    "time_ms": "1913"
}
```

can be combined if needed

```json
{
    "reconstruction": "B2 L2 R2",
    "time_ms": "1913",
    "dnf": false
}
```

or if dnf

```json
{
    "reconstruction": null,
    "time_ms": null,
    "dnf": true
}
```


## Success Responses

**Code** : `200 OK`


```json
{"solve_id":79}
```
