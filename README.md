# DockerizedFlaskApp
a dockerized flask app serving the requests on port 8080 using REST in Python that implements several endpoints, which is run using Terraform
the served endpoints are: 
/healthcheck
This endpoint must return the health status of the service.
/stats
This endpoint returns the stats on the number of requests blocked, the number of requests accepted, and the number of CIDRs currently being blocked. 
/block
This endpoint requires authentication (returns 401, if unauthenticated). It only accepts POST requests and must accept the following payload:
{
  "cidr": "172.10.10.0/24",
  "ttl": 86400,
}

