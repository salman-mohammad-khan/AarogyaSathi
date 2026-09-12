#!/bin/bash
# Rewrite .env with a single clean OLLAMA_API_KEY line.
KEY=$(grep '^OLLAMA_API_KEY=' /opt/healthbot/.env | grep -v '^OLLAMA_API_KEY=$' | cut -d= -f2 | head -1)
{
  echo "# AarogyaSathi environment (created by deploy script)"
  echo "OLLAMA_API_KEY=$KEY"
  echo "LLM_MODEL=qwen3:1.7b"
  echo "LLM_CLOUD_MODEL=gpt-oss:20b"
} > /opt/healthbot/.env
echo "clean .env written. key length: ${#KEY}"
grep -c '^OLLAMA_API_KEY=' /opt/healthbot/.env
