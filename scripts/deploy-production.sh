#!/bin/bash

# Pipeline Architect - Production Deployment Script
# Usage: ./scripts/deploy-production.sh [version] [environment]

set -e

# Configuration
APP_NAME="pipeline-architect"
IMAGE_NAME="pipeline-architect"
ENVIRONMENT=${2:-production}

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

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if running in production environment
    if [ "$ENVIRONMENT" != "production" ]; then
        warning "This script is for production deployment. Use staging script for staging environment."
        read -p "Are you sure you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deployment cancelled"
        fi
    fi
    
    # Check if Kubernetes is available
    if command -v kubectl &> /dev/null; then
        KUBERNETES=true
        log "Kubernetes detected"
    else
        KUBERNETES=false
        log "Kubernetes not available, using Docker Compose"
    fi
    
    success "Prerequisites check passed"
}

# Build and push Docker image
build_and_push_image() {
    local version=${1:-latest}
    
    log "Building and pushing Docker image: ${IMAGE_NAME}:${version}"
    
    # Build image
    docker build -t "${IMAGE_NAME}:${version}" .
    
    # Tag for registry (update with your registry)
    docker tag "${IMAGE_NAME}:${version}" "your-registry/${IMAGE_NAME}:${version}"
    
    # Push to registry
    docker push "your-registry/${IMAGE_NAME}:${version}"
    
    success "Docker image built and pushed successfully"
}

# Deploy using Kubernetes
deploy_kubernetes() {
    local version=${1:-latest}
    
    log "Deploying to Kubernetes cluster..."
    
    # Update image in deployment
    kubectl set image deployment/${APP_NAME} ${APP_NAME}=your-registry/${IMAGE_NAME}:${version}
    
    # Wait for rollout
    kubectl rollout status deployment/${APP_NAME} --timeout=300s
    
    success "Kubernetes deployment completed"
}

# Deploy using Docker Compose
deploy_docker_compose() {
    log "Deploying using Docker Compose..."
    
    # Use production compose file
    if [ -f "docker-compose.prod.yml" ]; then
        COMPOSE_FILE="docker-compose.prod.yml"
    else
        COMPOSE_FILE="docker-compose.yml"
    fi
    
    # Pull latest images
    docker-compose -f "$COMPOSE_FILE" pull
    
    # Restart services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    success "Docker Compose deployment completed"
}

# Health check
health_check() {
    log "Performing health check..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            success "Health check passed"
            return 0
        fi
        
        log "Health check attempt $attempt/$max_attempts failed, retrying in 10s..."
        sleep 10
        attempt=$((attempt + 1))
    done
    
    error "Health check failed after $max_attempts attempts"
}

# Run production tests
run_production_tests() {
    log "Running production tests..."
    
    # Run integration tests
    docker-compose exec -T pipeline-architect python -m pytest tests/integration/ -v --tb=short
    
    if [ $? -eq 0 ]; then
        success "Production tests passed"
    else
        warning "Production tests failed"
    fi
}

# Monitor deployment
monitor_deployment() {
    log "Monitoring deployment..."
    
    # Get pod status (Kubernetes)
    if [ "$KUBERNETES" = true ]; then
        kubectl get pods -l app=${APP_NAME}
    else
        # Get container status (Docker Compose)
        docker-compose ps
    fi
    
    # Check logs for errors
    log "Checking logs for errors..."
    sleep 5
    
    if [ "$KUBERNETES" = true ]; then
        kubectl logs deployment/${APP_NAME} --tail=50
    else
        docker-compose logs --tail=50 pipeline-architect
    fi
}

# Rollback function
rollback() {
    log "Rolling back deployment..."
    
    if [ "$KUBERNETES" = true ]; then
        kubectl rollout undo deployment/${APP_NAME}
        kubectl rollout status deployment/${APP_NAME} --timeout=300s
    else
        docker-compose -f docker-compose.yml down
        docker-compose -f docker-compose.yml up -d
    fi
    
    health_check
    success "Rollback completed"
}

# Cleanup old images
cleanup() {
    log "Cleaning up old Docker images..."
    
    # Remove dangling images
    docker image prune -f
    
    # Remove old tagged images (keep last 5)
    docker images "${IMAGE_NAME}" --format "table {{.Repository}}:{{.Tag}}" | tail -n +6 | xargs -r docker rmi
    
    success "Cleanup completed"
}

# Main deployment function
main() {
    log "Starting production deployment..."
    
    # Parse command line arguments
    VERSION=${1:-latest}
    
    # Run deployment steps
    check_prerequisites
    build_and_push_image "$VERSION"
    
    if [ "$KUBERNETES" = true ]; then
        deploy_kubernetes "$VERSION"
    else
        deploy_docker_compose
    fi
    
    health_check
    run_production_tests
    monitor_deployment
    cleanup
    
    success "Production deployment completed successfully!"
    log "Application available at: http://localhost:8000"
}

# Handle script interruption
trap 'error "Deployment interrupted"' INT TERM

# Run main function
main "$@"