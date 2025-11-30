#!/bin/bash

# Pipeline Architect - Staging Deployment Script
# Usage: ./scripts/deploy-staging.sh [version]

set -e

# Configuration
APP_NAME="pipeline-architect-staging"
IMAGE_NAME="pipeline-architect"
CONTAINER_NAME="${APP_NAME}"
ENVIRONMENT="staging"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if required tools are installed
check_requirements() {
    log "Checking requirements..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
    fi
    
    success "Requirements check passed"
}

# Build Docker image
build_image() {
    local version=${1:-latest}
    
    log "Building Docker image: ${IMAGE_NAME}:${version}"
    
    docker build -t "${IMAGE_NAME}:${version}" .
    
    if [ $? -eq 0 ]; then
        success "Docker image built successfully"
    else
        error "Failed to build Docker image"
    fi
}

# Deploy to staging
deploy_staging() {
    log "Deploying to staging environment..."
    
    # Stop and remove existing container
    if docker ps -q -f name="${CONTAINER_NAME}" | grep -q .; then
        log "Stopping existing container..."
        docker stop "${CONTAINER_NAME}"
        docker rm "${CONTAINER_NAME}"
    fi
    
    # Start new container
    log "Starting new container..."
    docker-compose -f docker-compose.yml up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Health check
    if curl -f http://localhost:8000/health &> /dev/null; then
        success "Staging deployment completed successfully"
    else
        error "Health check failed"
    fi
}

# Run tests in staging
test_staging() {
    log "Running staging tests..."
    
    # Run smoke tests
    docker-compose exec -T pipeline-architect python -m pytest tests/smoke/ -v
    
    if [ $? -eq 0 ]; then
        success "Staging tests passed"
    else
        warning "Staging tests failed"
    fi
}

# Rollback function
rollback() {
    log "Rolling back deployment..."
    
    # Get previous image
    local previous_image=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep "${IMAGE_NAME}" | sed -n '2p')
    
    if [ -n "$previous_image" ]; then
        log "Rolling back to ${previous_image}"
        docker tag "$previous_image" "${IMAGE_NAME}:latest"
        deploy_staging
        success "Rollback completed"
    else
        error "No previous image found for rollback"
    fi
}

# Main deployment function
main() {
    log "Starting staging deployment..."
    
    # Parse command line arguments
    VERSION=${1:-latest}
    
    # Run deployment steps
    check_requirements
    build_image "$VERSION"
    deploy_staging
    test_staging
    
    success "Staging deployment completed successfully!"
    log "Application available at: http://localhost:8000"
    log "API documentation: http://localhost:8000/docs"
}

# Handle script interruption
trap 'error "Deployment interrupted"' INT TERM

# Run main function
main "$@"