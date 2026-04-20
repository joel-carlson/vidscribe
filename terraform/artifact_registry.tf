resource "google_artifact_registry_repository" "vidscribe_repo" {
    location      = var.region
    repository_id = "vidscribe"
    format        = "DOCKER"
}
