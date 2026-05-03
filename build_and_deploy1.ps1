# -------- CONFIG --------
$repo = "telemetry-pipeline"
$registry = "585369386233.dkr.ecr.us-east-2.amazonaws.com"
$region = "us-east-2"
$tag = "latest"   # change to v1, v2, etc if needed

$imageLocal = "$repo`:$tag"
$imageRemote = "$registry/$repo`:$tag"

# -------- LOGIN --------
Write-Host "Logging into ECR..."
$pw = aws ecr get-login-password --region $region
docker login --username AWS --password $pw $registry

# -------- BUILD --------
Write-Host "Building image..."
docker build -t $imageLocal .

# -------- TAG --------
Write-Host "Tagging image..."
docker tag $imageLocal $imageRemote

# -------- PUSH --------
Write-Host "Pushing image to ECR..."
docker push $imageRemote

Write-Host "Done!"