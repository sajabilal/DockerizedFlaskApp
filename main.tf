terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.1"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Pulls the image
resource "docker_image" "flaskapp_image" {
  name = "flaskapp:v1"
}

resource "docker_network" "private_network" {
  name = "test"
  labels {
    label = "label"
    value = "test"
  }
}

# Create a container
resource "docker_container" "flaskapp_container" {
  image = docker_image.flaskapp_image.name
  name  = "docker_container"
#  network_mode = "custom"
  networks_advanced {
    name = "test"
  }
  ports {
    external = 8080
    internal = 8080
  }
}