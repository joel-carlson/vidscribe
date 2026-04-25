resource "google_redis_instance" "vidscribe_redis" {
    name           = "vidscribe-redis"
    region           = var.region
    tier           = "BASIC"
    memory_size_gb = 1
    redis_version     = "REDIS_7_2"
    authorized_network = google_compute_network.vpc_network.id
}