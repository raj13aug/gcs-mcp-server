resource "google_project_service" "cloud_run_api" {
  service = "run.googleapis.com"
}


resource "google_service_account" "gcs_admin_sa" {
  account_id   = "gcs-mcp-admin-sa"
  display_name = "GCS Bucket Admin Service Account"
}


resource "google_project_iam_member" "gcs_admin_role" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.gcs_admin_sa.email}"
}

resource "google_cloud_run_v2_service" "cloud_run_teraform" {
  name     = var.cloudrun_name
  location = var.region
  ingress  = var.cloudrun_ingress
  project  = var.project_id

  template {
    service_account = google_service_account.gcs_admin_sa.email

    containers {
      image = var.cloudrun_image
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
    }
  }
  depends_on = [
    google_project_service.cloud_run_api,
    google_project_iam_member.gcs_admin_role
  ]
}


data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_v2_service.cloud_run_teraform.location
  project     = google_cloud_run_v2_service.cloud_run_teraform.project
  service     = google_cloud_run_v2_service.cloud_run_teraform.name
  policy_data = data.google_iam_policy.noauth.policy_data
}

output "url" {
  value = google_cloud_run_v2_service.cloud_run_teraform.uri
}