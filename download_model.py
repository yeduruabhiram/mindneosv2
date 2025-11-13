from huggingface_hub import snapshot_download

print("🚀 Downloading Mistral 7B GGUF quantized model...")

snapshot_download(
    repo_id="bartowski/Mistral-7B-Instruct-v0.3-GGUF",   # ✅ working repo
    local_dir="./models",
    allow_patterns=["*Q4_K_M.gguf"]                      # only download quantized model
)

print("✅ Download complete! Check ./models/bartowski/Mistral-7B-Instruct-v0.3-GGUF/")
