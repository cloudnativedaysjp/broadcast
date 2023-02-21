job "media_checker" {
  datacenters = ["dc1"]
  type = "batch"

  periodic {
    cron         = "*/10 * * * *"
    prohibit_overlap = true
  }

  task "media_checker" {
    driver = "exec"

    config {
      command = "/usr/bin/python3"
      args = ["/opt/media_checker/media_checker.py", "put", "--upper_limit", "42", "--lower_limit", "0", "--csv", "/home/ubuntu/nextcloud/cfp.csv"]
    }

    env {
      ENV_FILE = "/opt/media_checker/env.json"
    }

    artifact {
      source = "/opt/media_checker"
      destination = "/opt/media_checker"
    }
  }
}
