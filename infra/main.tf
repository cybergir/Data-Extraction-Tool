# infra/main.tf
resource "kubernetes_cron_job" "extractor" {
  metadata {
    name = "system-data-extractor"
  }
  spec {
    schedule = "0 2 * * *" # 2AM daily
    job_template {
      spec {
        template {
          spec {
            container {
              name    = "extractor"
              image   = "yourrepo/system-extractor:latest"
              command = ["--source", "all"]
              resources {
                limits = {
                  cpu    = "500m"
                  memory = "512Mi"
                }
              }
            }
          }
        }
      }
    }
  }
}