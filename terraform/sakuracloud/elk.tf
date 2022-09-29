resource "sakuracloud_disk" "elk" {
	name              = "elk"
  source_archive_id = data.sakuracloud_archive.ubuntu.id
  plan              = "ssd"
  connector         = "virtio"
  size              = 512000

  lifecycle {
    ignore_changes = [
      source_archive_id,
    ]
  }
}

resource "sakuracloud_server" "elk" {
  name = "elk"
  disks = [
    sakuracloud_disk.elk.id,
  ]
  core        = 4
  memory      = 8
  description = "ELK Stack"
  tags        = ["app=elk", "stage=production", "starred"]

  network_interface {
    upstream = "shared"
    packet_filter_id = sakuracloud_packet_filter.nextcloud.id
  }

  network_interface {
    upstream = data.sakuracloud_switch.switcher.id
  }

  user_data = templatefile("./template/cloud-init.yaml", {
    vm_password = random_password.password.result,
    hostname    = "elk"
  })

  lifecycle {
    ignore_changes = [
      user_data,
    ]
  }
}
