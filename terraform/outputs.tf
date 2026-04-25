output "GKE_CLUSTER_NAME" {
 description = "Name of the GKE cluster"
  value = google_container_cluster.vidscribe_gke.name
    sensitive = false
}

output "GKE_CLUSTER_ENDPOINT" {
 description = "Endpoint of the GKE cluster"
  value = google_container_cluster.vidscribe_gke.endpoint
  sensitive = true
}

output "REDIS_HOST" {
 description = "Host of the Redis instance"
  value = google_redis_instance.vidscribe_redis.host
    sensitive = true
}

output "CSQL_CONNECTION_NAME" {
 description = "Connection name for Cloud SQL instance"
  value = google_sql_database_instance.vidscribe_sql_instance.connection_name
  sensitive = true
}

output "GCS_BUCKET_NAME" {
 description = "Name of the GCS bucket"
  value = google_storage_bucket.vidscribe_bucket.name
  sensitive = false
}