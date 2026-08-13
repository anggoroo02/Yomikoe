from yomikoe.engines.environment import detect_environment

env = detect_environment()

print("=== Compute Environment ===")
print(f"CUDA Devices : {env.cuda_device_count}")
print(f"CUDA         : {env.has_cuda}")
print("Supported Compute Types:")

for compute_type in sorted(env.supported_compute_types):
    print(f"  - {compute_type}")
