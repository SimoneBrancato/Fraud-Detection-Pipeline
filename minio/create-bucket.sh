#!/bin/bash
mc alias set myminio http://localhost:9000 admin password

# Check if bucket exists before creating
if ! mc ls myminio/warehouse > /dev/null 2>&1; then
    echo "📦 Creating bucket warehouse..."
    mc mb myminio/warehouse
else
    echo "📦 Bucket warehouse already exists"
fi