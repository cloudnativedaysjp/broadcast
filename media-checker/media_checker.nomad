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
      args = ["/opt/broadcast/media_checker/media_checker.py", "put", "--upper_limit", "42", "--lower_limit", "0", "--csv", "/home/ubuntu/nextcloud/cfp.csv"]
    }

    env {
      ENV_FILE = "/opt/broadcast/media_checker/media_checker_env.json"
    }

    artifact {
      source = "/opt/broadcast/media_checker"
      destination = "/opt/broadcast/media_checker"
    }
  }
}
