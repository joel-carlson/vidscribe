resource "google_compute_global_address" "vidscribe_sql_ip"{
    name = "vidscribe-sql-ip"
    purpose = "VPC_PEERING"
    address_type = "INTERNAL"
    prefix_length = 16
    network = google_compute_network.vpc_network.id
}

resource "google_service_networking_connection" "vidscribe_sql_connection" {
    network = google_compute_network.vpc_network.id
    service = "servicenetworking.googleapis.com"
    reserved_peering_ranges = [google_compute_global_address.vidscribe_sql_ip.name]
}

resource "google_sql_database_instance" "vidscribe_sql_instance" {
    name = "vidscribe-sql-instance"
    database_version = "POSTGRES_15"
    region = var.region
    settings {
        tier = "db-f1-micro"
        ip_configuration {
            ipv4_enabled = false
            private_network = google_compute_network.vpc_network.id
            enable_private_path_for_google_cloud_services = true
        }
    }
    depends_on = [google_service_networking_connection.vidscribe_sql_connection]
}

resource "google_sql_user" "vidscribe_sql_user" {
    name = "vidscribe-user"
    instance = google_sql_database_instance.vidscribe_sql_instance.name
    password = var.sql_password
}