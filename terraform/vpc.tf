resource "google_compute_network" "vpc_network" {
      name = "vidscribe-vpc"
      auto_create_subnetworks = false
}


resource "google_compute_subnetwork" "vpc_subnetwork" {
    name = "vidscribe-subnet"
    ip_cidr_range = "10.0.0.0/18"
    region = var.region
    network = google_compute_network.vpc_network.id
    secondary_ip_range {
        range_name = "pods"
        ip_cidr_range = "10.48.0.0/14"
    }
    secondary_ip_range {
        range_name = "services"
        ip_cidr_range = "10.52.0.0/20"
    }
    lifecycle {
        ignore_changes = [secondary_ip_range]
    }
}
