# File for defining variables
variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

variable "region" {
  description = "The region of the Google Cloud project"
  type        = string
  default     = "us-central1"
}

variable "gke_num_nodes" {
    description = "num of nodes for GKE to create"
    type = number
    default = 1
}
