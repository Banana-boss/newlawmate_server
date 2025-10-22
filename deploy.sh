#!/bin/bash

# FastAPI 서버 배포 스크립트
# 테스트 통과 후 Docker 컨테이너를 재시작합니다.

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 Starting deployment process..."
echo ""

# 색상 정의
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 환경 변수 로드
echo "📋 Loading environment variables..."
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
    echo -e "${GREEN}✅ Environment variables loaded${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found, using defaults${NC}"
fi
echo ""

# 2. 의존성 확인
echo "📦 Checking dependencies..."
if [ ! -f requirements.txt ]; then
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies file found${NC}"
echo ""

# 3. 테스트 실행
echo "🧪 Running tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Docker Compose로 테스트 환경 구성
docker-compose up -d mysql
echo "⏳ Waiting for MySQL to be ready..."
sleep 10

# 테스트 실행 (docker-compose exec 사용)
if docker-compose run --rm fastapi pytest tests/ -v --tb=short; then
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo ""
    echo -e "${RED}❌ Tests failed! Deployment aborted.${NC}"
    docker-compose down
    exit 1
fi
echo ""

# 4. Docker 이미지 빌드
echo "🔨 Building Docker image..."
if docker-compose build; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi
echo ""

# 5. 기존 컨테이너 중단 및 새 컨테이너 시작
echo "🔄 Restarting containers..."
docker-compose down
docker-compose up -d

# 6. 헬스 체크
echo ""
echo "🏥 Performing health check..."
sleep 5

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:${PORT:-8000}/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server is healthy!${NC}"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "⏳ Waiting for server to be ready... ($RETRY_COUNT/$MAX_RETRIES)"
        sleep 2
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ Server health check failed${NC}"
    docker-compose logs fastapi
    exit 1
fi

# 7. 배포 완료
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "📊 Server Information:"
echo "  - API URL: http://localhost:${PORT:-8000}"
echo "  - API Docs: http://localhost:${PORT:-8000}/docs"
echo "  - ReDoc: http://localhost:${PORT:-8000}/redoc"
echo ""
echo "📝 Useful commands:"
echo "  - View logs: docker-compose logs -f fastapi"
echo "  - Stop server: docker-compose down"
echo "  - Restart server: docker-compose restart"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
