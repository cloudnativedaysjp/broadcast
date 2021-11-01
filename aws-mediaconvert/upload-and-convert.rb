# frozen_string_literal: true

require 'csv'
require 'time'
require 'aws-sdk-s3'
require 'aws-sdk-mediaconvert'

def object_uploaded?(s3_client, bucket_name, object_key, filename)
  bucket = s3_client.bucket(bucket_name)
  response = bucket.object(object_key).put(body: File.open(filename))
  if response.etag
    true
  else
    false
  end
rescue StandardError => e
  puts "Error uploading object: #{e.message}"
  false
end

# Full example call:
def upload(id, filename)
  bucket_name = 'dreamkast-ivs-stream-archive-prd'
  object_key = "source/#{id}.mp4"
  region = 'us-east-1'
  s3_client = Aws::S3::Resource.new(region: region)

  if object_uploaded?(s3_client, bucket_name, object_key, filename)
    puts "Object '#{object_key}' uploaded to bucket '#{bucket_name}'."
  else
    puts "Object '#{object_key}' not uploaded to bucket '#{bucket_name}'."
  end
end

def create_convert_job(id)
  client = Aws::MediaConvert::Client.new(
    region: 'us-east-1',
    endpoint: 'https://lxlxpswfb.mediaconvert.us-east-1.amazonaws.com'
  )

  client.create_job(
    { acceleration_settings: { mode: 'DISABLED' },
      billing_tags_source: nil,
      hop_destinations: nil,
      job_template: nil,
      priority: 0,
      queue: 'arn:aws:mediaconvert:us-east-1:607167088920:queues/Default',
      queue_transitions: nil,
      retry_count: nil,
      role: 'arn:aws:iam::607167088920:role/service-role/MediaConvert_Default_Role',
      settings: {
        ad_avail_offset: nil,
        avail_blanking: nil,
        esam: nil,
        extended_data_services: nil,
        inputs: [
          {
            audio_selector_groups: nil,
            audio_selectors: {
              'Audio Selector 1' => {
                custom_language_code: nil,
                default_selection: 'DEFAULT',
                external_audio_file_input: nil,
                hls_rendition_group_settings: nil,
                language_code: nil,
                offset: nil,
                pids: nil,
                program_selection: nil,
                remix_settings: nil,
                selector_type: nil,
                tracks: nil
              }
            },
            caption_selectors: nil,
            crop: nil,
            deblock_filter: nil,
            decryption_settings: nil,
            denoise_filter: nil,
            file_input: "s3://dreamkast-ivs-stream-archive-prd/source/#{id}.mp4",
            filter_enable: nil,
            filter_strength: nil,
            image_inserter: nil,
            input_clippings: nil,
            input_scan_type: nil,
            position: nil,
            program_number: nil,
            psi_control: nil,
            supplemental_imps: nil,
            timecode_source: 'ZEROBASED',
            timecode_start: nil,
            video_selector: {
              alpha_behavior: nil,
              color_space: nil,
              color_space_usage: nil,
              hdr_10_metadata: nil,
              pid: nil,
              program_number: nil,
              rotate: nil,
              sample_range: nil
            }
          }
        ],
        kantar_watermark: nil,
        motion_image_inserter: nil,
        nielsen_configuration: nil,
        nielsen_non_linear_watermark: nil,
        output_groups: [
          { automated_encoding_settings: {
            abr_settings: {
              max_abr_bitrate: 2_000_000,
              max_renditions: nil,
              min_abr_bitrate: 100_000
            }
          },
            custom_name: 'Converted',
            name: 'Apple HLS',
            output_group_settings: {
              cmaf_group_settings: nil,
              dash_iso_group_settings: nil,
              file_group_settings: nil,
              hls_group_settings: {
                ad_markers: nil,
                additional_manifests: nil,
                audio_only_header: nil,
                base_url: nil,
                caption_language_mappings: nil,
                caption_language_setting: nil,
                client_cache: nil,
                codec_specification: nil,
                destination: "s3://dreamkast-ivs-stream-archive-prd/medialive/cndt2021/talks/#{id}/",
                destination_settings: nil,
                directory_structure: nil,
                encryption: nil,
                image_based_trick_play: nil,
                image_based_trick_play_settings: nil,
                manifest_compression: nil,
                manifest_duration_format: nil,
                min_final_segment_length: nil,
                min_segment_length: 0,
                output_selection: nil,
                program_date_time: nil,
                program_date_time_period: nil,
                segment_control: nil,
                segment_length: 10,
                segment_length_control: nil,
                segments_per_subdirectory: nil,
                stream_inf_resolution: nil,
                target_duration_compatibility_mode: nil,
                timed_metadata_id_3_frame: nil,
                timed_metadata_id_3_period: nil,
                timestamp_delta_milliseconds: nil
              },
              ms_smooth_group_settings: nil,
              type: 'HLS_GROUP_SETTINGS'
            },
            outputs: [
              { audio_descriptions: [{
                audio_channel_tagging_settings: nil,
                audio_normalization_settings: nil,
                audio_source_name: nil,
                audio_type: nil,
                audio_type_control: nil,
                codec_settings: {
                  aac_settings: {
                    audio_description_broadcaster_mix: nil,
                    bitrate: 96_000,
                    codec_profile: nil,
                    coding_mode: 'CODING_MODE_2_0',
                    rate_control_mode: nil,
                    raw_format: nil,
                    sample_rate: 48_000,
                    specification: nil,
                    vbr_quality: nil
                  },
                  ac_3_settings: nil,
                  aiff_settings: nil,
                  codec: 'AAC',
                  eac_3_atmos_settings: nil,
                  eac_3_settings: nil,
                  mp_2_settings: nil,
                  mp_3_settings: nil,
                  opus_settings: nil,
                  vorbis_settings: nil,
                  wav_settings: nil
                },
                custom_language_code: nil,
                language_code: nil,
                language_code_control: nil,
                remix_settings: nil,
                stream_name: nil
              }],
                caption_descriptions: nil,
                container_settings: {
                  cmfc_settings: nil,
                  container: 'M3U8',
                  f4v_settings: nil,
                  m2ts_settings: nil,
                  m3u_8_settings: {
                    audio_duration: nil,
                    audio_frames_per_pes: nil,
                    audio_pids: nil,
                    data_pts_control: nil,
                    max_pcr_interval: nil,
                    nielsen_id_3: nil,
                    pat_interval: nil,
                    pcr_control: nil,
                    pcr_pid: nil,
                    pmt_interval: nil,
                    pmt_pid: nil,
                    private_metadata_pid: nil,
                    program_number: nil,
                    scte_35_pid: nil,
                    scte_35_source: nil,
                    timed_metadata: nil,
                    timed_metadata_pid: nil,
                    transport_stream_id: nil,
                    video_pid: nil
                  }, mov_settings: nil, mp_4_settings: nil, mpd_settings: nil, mxf_settings: nil
                },
                extension: nil,
                name_modifier: 'playlist',
                output_settings: {
                  hls_settings: {
                    audio_group_id: nil, audio_only_container: nil, audio_rendition_sets: nil, audio_track_type: nil, descriptive_video_service_flag: nil, i_frame_only_manifest: nil, segment_modifier: nil
                  }
                },
                preset: nil,
                video_description: {
                  afd_signaling: nil,
                  anti_alias: nil,
                  codec_settings: {
                    av_1_settings: nil, avc_intra_settings: nil, codec: 'H_264', frame_capture_settings: nil, h264_settings: {
                      adaptive_quantization: nil, bitrate: nil, codec_level: nil, codec_profile: nil, dynamic_sub_gop: nil, entropy_encoding: nil, field_encoding: nil, flicker_adaptive_quantization: nil, framerate_control: 'INITIALIZE_FROM_SOURCE', framerate_conversion_algorithm: nil, framerate_denominator: nil, framerate_numerator: nil, gop_b_reference: nil, gop_closed_cadence: nil, gop_size: nil, gop_size_units: nil, hrd_buffer_initial_fill_percentage: nil, hrd_buffer_size: nil, interlace_mode: nil, max_bitrate: nil, min_i_interval: nil, number_b_frames_between_reference_frames: nil, number_reference_frames: nil, par_control: nil, par_denominator: nil, par_numerator: nil, quality_tuning_level: 'MULTI_PASS_HQ', qvbr_settings: nil, rate_control_mode: 'QVBR', repeat_pps: nil, scan_type_conversion_mode: nil, scene_change_detect: 'TRANSITION_DETECTION', slices: nil, slow_pal: nil, softness: nil, spatial_adaptive_quantization: nil, syntax: nil, telecine: nil, temporal_adaptive_quantization: nil, unregistered_sei_timecode: nil
                    }, h265_settings: nil, mpeg_2_settings: nil, prores_settings: nil, vc_3_settings: nil, vp_8_settings: nil, vp_9_settings: nil, xavc_settings: nil
                  },
                  color_metadata: nil,
                  crop: nil, drop_frame_timecode: nil, fixed_afd: nil, height: 1080, position: nil, respond_to_afd: nil, scaling_behavior: nil, sharpness: nil, timecode_insertion: nil, video_preprocessors: nil, width: 1920
                } }
            ] }
        ],
        timecode_config: { anchor: nil, source: 'ZEROBASED', start: nil, timestamp_offset: nil },
        timed_metadata_insertion: nil
      },
      simulate_reserved_queue: nil,
      status_update_interval: 'SECONDS_60',
      user_metadata: {} }
  )
end

tracks = {
  20 => 'A',
  21 => 'B',
  22 => 'C',
  23 => 'D',
  24 => 'E',
  25 => 'F'
}
conference_day = {
  11 => '1',
  12 => '2'
}

count = 0

CSV.foreach('talks.csv', headers: true) do |row|
  id = row[0]
  search_key = "#{conference_day[row[11].to_i]}#{tracks[row[12].to_i]}-#{Time.parse("#{row[4]} UTC").localtime.strftime('%H%M')}-#{Time.parse("#{row[5]} UTC").localtime.strftime('%H%M')}"
  found = Dir.glob("#{search_key}*")

  if found.length.positive?
    puts "Found:#{found}"
    puts "Start Uploading: #{found[0]} to #{id}.mp4"
    upload(id, found[0])
    puts 'Upload finished'
    puts 'Queue converting job'
    resp = create_convert_job(id)
    puts "Queued #{resp.job.id}"
    count += 1
  else
    puts 'Not Found'
  end
end

puts "Found: #{count}"

