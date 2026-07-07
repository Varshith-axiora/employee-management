Invoke-RestMethod `
-Uri http://127.0.0.1:55124/api/employees `
-Method POST `
-ContentType "application/json" `
-Body '{
    "name":"John",
    "email":"john@gmail.com",
    "department":"DevOps",
    "salary":85000
}'