from huggingface_hub import snapshot_download

# download the real quantized gguf file from HF
snapshot_download(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    local_dir="./models",          # where to save
    ignore_patterns=["*.safetensors", "*.bin", "*.pt"]  # optional: skip big pytorch weights
)
print("✅ Download complete. Check ./models directory.")