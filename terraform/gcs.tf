resource "google_storage_bucket" "vidscribe_bucket" {
    name     = "vidscribe-${var.project_id}"
    location = var.region
    force_destroy = true
    uniform_bucket_level_access = true
    lifecycle_rule {
        action {
            type = "Delete"
        }
        condition {
            age = 30
        }
    }
} 