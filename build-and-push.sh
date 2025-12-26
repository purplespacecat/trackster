#!/bin/bash
# Build and push Trackster Docker image to Docker Hub

set -e

DOCKER_USERNAME="spacecrab"
IMAGE_NAME="trackster"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================"
echo "Trackster Docker Build & Push"
echo -e "======================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Error: docker not found. Please install docker first.${NC}"
    exit 1
fi

# Check if we need sudo for docker
DOCKER_CMD="docker"
if ! docker ps &> /dev/null; then
    if sudo docker ps &> /dev/null 2>&1; then
        echo -e "${YELLOW}Note: Using sudo for Docker commands${NC}"
        echo "To avoid this, add your user to the docker group:"
        echo "  sudo usermod -aG docker $USER"
        echo ""
        DOCKER_CMD="sudo docker"
    else
        echo -e "${YELLOW}Error: Cannot access Docker daemon. Please check Docker installation.${NC}"
        exit 1
    fi
fi

# Determine tag
if [ -n "$1" ]; then
    TAG="$1"
else
    # Try to get git tag or commit hash
    if git rev-parse --git-dir > /dev/null 2>&1; then
        # Check if there's a git tag
        GIT_TAG=$(git describe --tags --exact-match 2>/dev/null || echo "")
        if [ -n "$GIT_TAG" ]; then
            TAG="$GIT_TAG"
        else
            # Use short commit hash
            TAG="$(git rev-parse --short HEAD)"
        fi
    else
        # Default to latest
        TAG="latest"
    fi
fi

FULL_IMAGE="${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}"
LATEST_IMAGE="${DOCKER_USERNAME}/${IMAGE_NAME}:latest"

echo -e "${BLUE}Configuration:${NC}"
echo "  Image: ${FULL_IMAGE}"
echo "  Also tagging as: ${LATEST_IMAGE}"
echo ""

# Confirm
read -p "Continue with build and push? [Y/n]: " CONFIRM
if [[ "$CONFIRM" =~ ^[Nn]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Build image
echo ""
echo -e "${BLUE}Building Docker image...${NC}"
$DOCKER_CMD build -t "${FULL_IMAGE}" .

# Tag as latest
echo ""
echo -e "${BLUE}Tagging as latest...${NC}"
$DOCKER_CMD tag "${FULL_IMAGE}" "${LATEST_IMAGE}"

# Check if logged in to Docker Hub
echo ""
echo -e "${BLUE}Checking Docker Hub authentication...${NC}"
if ! $DOCKER_CMD info | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo -e "${YELLOW}Not logged in to Docker Hub. Please log in:${NC}"
    $DOCKER_CMD login
fi

# Push images
echo ""
echo -e "${BLUE}Pushing ${FULL_IMAGE}...${NC}"
$DOCKER_CMD push "${FULL_IMAGE}"

echo ""
echo -e "${BLUE}Pushing ${LATEST_IMAGE}...${NC}"
$DOCKER_CMD push "${LATEST_IMAGE}"

# Summary
echo ""
echo -e "${GREEN}======================================"
echo "✓ Build and Push Successful!"
echo -e "======================================${NC}"
echo ""
echo "Images pushed:"
echo "  - ${FULL_IMAGE}"
echo "  - ${LATEST_IMAGE}"
echo ""
echo "Use in Kubernetes:"
echo "  image: ${FULL_IMAGE}"
echo ""
echo "Pull the image:"
echo "  docker pull ${FULL_IMAGE}"
echo ""
echo -e "${GREEN}=====================================${NC}"
