resource "google_container_cluster" "vidscribe_gke" {
    name = "vidscribe-cluster"
    location = var.region
    #removing default node pool to create custom one
    remove_default_node_pool = true
    initial_node_count = 1
    network = google_compute_network.vpc_network.name
    subnetwork = google_compute_subnetwork.vpc_subnetwork.name
    networking_mode = "VPC_NATIVE"
    ip_allocation_policy {}
    workload_identity_config {
        workload_pool = "${var.project_id}.svc.id.goog"
    }
    deletion_protection = false
}
resource "google_container_node_pool" "primary_nodes" {
	name = "vidscribe-node-pool"
	location = var.region
    cluster =  google_container_cluster.vidscribe_gke.name
    node_count = var.gke_num_nodes 
    autoscaling {
        min_node_count = 1 
        max_node_count = 3
    }
    
    management { 
        auto_repair  = true 
        auto_upgrade = true
    }
    node_config {
        machine_type = "e2-standard-2"
        disk_size_gb = 50
        oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    }
}
