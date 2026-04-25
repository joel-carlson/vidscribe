resource "google_pubsub_topic" "vidscribe_topic" {
  name = "vidscribe-topic"
}
resource "google_pubsub_subscription" "vidscribe_subscription" {
  name  = "vidscribe-subscription"
  topic = google_pubsub_topic.vidscribe_topic.name
  ack_deadline_seconds = 600
}