resource "google_service_account" "vidscribe_sa" {
    account_id   = "vidscribe-sa"
    display_name = "VidScribe Service Account"
}

resource "google_project_iam_member" "vidscribe_sa_storage" {
    project = var.project_id
    role    = "roles/storage.objectAdmin"
    member  = "serviceAccount:${google_service_account.vidscribe_sa.email}"
}

resource "google_project_iam_member" "vidscribe_sa_pubsub_subscriber" {
    project = var.project_id
    role    = "roles/pubsub.subscriber"
    member  = "serviceAccount:${google_service_account.vidscribe_sa.email}"
}

resource "google_project_iam_member" "vidscribe_sa_pubsub_publisher" {
    project = var.project_id
    role    = "roles/pubsub.publisher"
    member  = "serviceAccount:${google_service_account.vidscribe_sa.email}"
}

resource "google_project_iam_member" "vidscribe_sa_cloudsql" {
    project = var.project_id
    role    = "roles/cloudsql.client"
    member  = "serviceAccount:${google_service_account.vidscribe_sa.email}"
}

resource "google_project_iam_member" "vidscribe_sa_aiplatform" {
    project = var.project_id
    role    = "roles/aiplatform.user"
    member  = "serviceAccount:${google_service_account.vidscribe_sa.email}"
}

# Workload identity binding — allows the Kubernetes SA to act as this GCP SA
resource "google_service_account_iam_member" "vidscribe_workload_identity" {
    service_account_id = google_service_account.vidscribe_sa.name
    role               = "roles/iam.workloadIdentityUser"
    member             = "serviceAccount:${var.project_id}.svc.id.goog[default/vidscribe-ksa]"
}
