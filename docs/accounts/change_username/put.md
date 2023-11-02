# Show Contest

Show all solve of this contest

**URL** : `/accounts/change_username/`

**Method** : `GET`

**Auth required** : YES 

**Permissions required** : User is not verified

**Data to send**

```json
{
    "username": "justHoma"
}
```

## Success Responses

**Code** : `200 OK`


```json
{
    "id": 2,
    "username": "justHoma"
}
```

## Error Responses

**Code** : `400 OK`

```json
{
    "username": [
        "Username must be alphanumeric"
    ]
}
```

```json
{
    "username": [
        "Ensure this field has at least 3 characters."
    ]
}
```

```json
{
    "username": [
        "Ensure this field has no more than 20 characters."
    ]
}
```

**Code** : `403 OK`

If user already changed nickname

```json
{
    "detail": "you dont have permission"
}
```