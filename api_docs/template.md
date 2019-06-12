#### Overview of the api's endpoints:

- [account](#account-apiv1account)
- [authentication](#authentication-apiv1auth)
- [resources](#resources-resources)
- [jobs](#jobs-jobs)
- [pricing](#pricing-pricing)

#### Requests 

All endpoint requests should be extended from `/api/v1`. For instance an authentication request should be made to `/api/v1/auth/`.

Each endpoint supports the four basic basic HTTP verbs:

| Verb   | Action |
| ------ | ------------------------------------ |
| GET    | Retrieves data from an endpoint      |
| POST   | Submits new data to an endpoint      |
| PUT    | Updates existing data at an endpoint |
| DELETE | Removes data from an endpoint        |

#### Responses:

The api returns all responses as JSON data with at minimum the following fields.

| Field          | Description                                                      |
|----------------|------------------------------------------------------------------|
| success        | Boolean value based on whether the call was successful.          |
| error          | Null if success is true; otherwise an appropriate error message. |
| message        | Human friendly message describing the interaction with the api.  |

Note: Some responses will contain more fields than laid out here. For instance a successful authentication request will return a [json web token](https://jwt.io/).

#### Response Codes:
Where possible the api attempts to stick to return the most appropriate status code based on the list of [http status codes](https://www.restapitutorial.com/httpstatuscodes.html).

###### The following endpoints are laid out in the following format:
| Column Header  | Description                                                   |
|----------------|---------------------------------------------------------------|
| Method         | The HTTP method by which to interact with the endpoint.       |
| endpoint       | The endpoint to interact with.                                |
| parameters     | The request body sent to the server.                          |
| requires token | The endpoint requires a jwt token for successful interaction. |

***

### Account (`/api/v1/account`)

##### Get account information

###### Request

`GET https://api.deepmarket.cs.pdx.edu/api/v1/account/`

Using `curl`
```bash
$ curl --request GET --header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVjZGI2YTBmMzY2NmY0MzM0ZjZlOTczMyIsImlhdCI6MTU1Nzg4NDAwMn0.ErlyRuWi5U7Qyg3_C9QtMLWMGxkTsUgtSuCmlI9YzKU' https://api.deepmarket.cs.pdx.edu/api/v1/account/
```

###### Response
```bash
{
    "success": true,
    "error": null,
    "message": "Successfully fetched customer information.",
    "customer": {
        "credits": 20,
        "_id": "5c84a6d58eaea68613cb7e0e",
        "firstname": "Barbara",
        "lastname": "Streisand",
        "email": "barbara@email.com",
        "password": "$2b$10$xIv9Y9VEWuZUpFAk1suGw.B/TsVt2b2vuyh7tCZqhQWzUOvTYsAZu",
        "status": "Active",
        "createdOn": "2019-03-10T05:55:33.801Z",
        "updatedOn": "2019-03-10T05:55:33.801Z",
        "__v": 0
    }
}
```

***

##### Create a new account

###### Request 

`POST https://api.deepmarket.cs.pdx.edu/api/v1/account/`

Using `curl`
```bash
$ curl --request POST --header 'Content-Type: application/json' --data '{"firstname": "Barabara", "lastname": "Streisand", "email": "barbara@email.com", "password": "password"}' https://api.deepmarket.cs.pdx.edu/api/v1/account/
```

###### Response

```bash
{
  "success": true,
  "error": null,
  "message": "Successfully created account.",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVjZGI2YTBmMzY2NmY0MzM0ZjZlOTczMyIsImlhdCI6MTU1Nzg4MzQwNywiZXhwIjoxNTU3OTY5ODA3fQ.-r9ae05XnaUdtIISLBsbujLwtqDkUolo9kI0ERG-XfE",
  "user": {
    "credits": 20,
    "_id": "5cdb6a0f3666f4334f6e9733",
    "firstname": "Barabara",
    "lastname": "Streisand",
    "email": "barbara@email.com",
    "password": "$2b$10$QBGD5ijWWeUIIWijPDu4pOMQPfPFZrke6cTJ3WT4Usau9JRp8i3lO",
    "status": "Active",
    "createdOn": "2019-05-15T01:23:27.531Z",
    "updatedOn": "2019-05-15T01:23:27.531Z",
    "__v": 0
  }
}
```

An overview of the account endpoint functionality:

| method | endpoint | parameters | requires token |
|--------|----------|------------|----------------|
| GET    | `/account/`      | `{}` | Yes |
| POST   | `/account/`      | `{firstname, lastname, email, password}` | No  |
| PUT    | `/account/`      | Not Implemented                          | Yes |
| DELETE | `/account/`      | `{}`                                     |Yes |

### Authentication (`/api/v1/auth`)

##### Login to the application (i.e. generate an auth token)

###### Request 
`POST https://api.deepmarket.cs.pdx.edu/api/v1/auth/login/`

Using `curl`
```curl
curl --request POST --header 'Content-Type: application/json' --data '{"email": "barbara@email.com", "password": "password"}' https://api.deepmarket.cs.pdx.edu/api/v1/auth/login/
```

###### Response

```bash
{
    "success": true,
    "error": null,
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVjZGI2YTBmMzY2NmY0MzM0ZjZlOTczMyIsImlhdCI6MTU1Nzg4NDAwMn0.ErlyRuWi5U7Qyg3_C9QtMLWMGxkTsUgtSuCmlI9YzKU",
    "auth": true
}
```

***

##### Logout from the application (i.e. invalidate given auth tokens)

###### Request
`POST https://api.deepmarket.cs.pdx.edu/api/v1/auth/login/`

Using `curl`
```bash
curl --request POST --header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVjZGI2YTBmMzY2NmY0MzM0ZjZlOTczMyIsImlhdCI6MTU1Nzg4NDAwMn0.ErlyRuWi5U7Qyg3_C9QtMLWMGxkTsUgtSuCmlI9YzKU'
```

###### Response 

```bash
{
  "success": true,
  "error": null,
  "message": "Successfully logged out.",
  "token": null,
  "auth": false
}
```

An overview of the authentication endpoint functionality:

| method | endpoint              | parameters          | requires token |  
|--------|-----------------------|---------------------|----------------|
| POST   | `/auth/login`         | `{email, password}` | No             |
| POST   | `/auth/logout`        | `{}`                | Yes            |

### Resources (`/resources`)
| method | endpoint | parameters | requires token | Description                                  |
|--------|----------|------------|----------------|----------------------------------------------|
| GET    | `/resouces/`      | `{}`       | Yes            | Gets all the resources for the current user. |
| POST   | `/resouces/`      | `{ip_address, ram, cores, cpus, gpus, price, machine_name}`| Yes | Adds a resource to the current users profile |
| PUT    | `/resouces/{resource_id}`      | `{}`       | Yes            | *NOT IMPLEMENTED*                            |
| DELETE | `/`      | `{resource_id}` | Yes       | **DEPRECATED**: Use `/{resource_id}` instead.|
| DELETE | `/resouces/{resource_id}` | `{}` | Yes          | Deletes resources with `resource_id`         |

### Jobs (`/jobs`)
| method | endpoint    | parameters | requires token | Description                             |
|--------|-------------|------------|----------------|-----------------------------------------|
| GET    | `/jobs/`         | `{}`       | Yes            | Gets all the jobs for the current user. |
| GET    | `/jobs/{job_id}` | `{}`       | Yes            | Gets job <job_id> for the current user. |
| POST   | `/jobs/`         | `{workers, cores, memory, timeslot_id, price, source_files, input_files}` | Yes | Adds a job to be run. | 
| PUT    | `/jobs/{job_id}` | `{}`       | Yes            | *NOT IMPLEMENTED*                       |
| DELETE | `jobs/{job_id}`  | `{}`       | Yes            | Deletes job with `job_id`               |

### Pricing (`/pricing`)
| method | endpoint    | parameters | requires token | Description                             |
|--------|-------------|------------|----------------|-----------------------------------------|
| GET    | `/pricing/` | `{}`       | No             | Returns pricing data for the next 24hrs.|
| POST   | `/pricing/` | `TBD`      | yes            | Inserts price data to the database      |
