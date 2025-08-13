# 🚀 Production Deployment Guide

## 📋 Overview

This guide explains how to deploy your HTMX Django application to production using Docker and docker-compose. The setup includes:

- **Django app** running on gunicorn
- **Nginx** reverse proxy for static files and load balancing
- **PostgreSQL** database (optional)
- **Redis** caching (optional)
- **SSL/HTTPS** support (ready to configure)

## 🏗️ Architecture

```
Internet → Nginx (Port 80/443) → Django + Gunicorn (Port 8000)
                ↓
            Static Files
            Media Files
            SSL Termination
```

## 🚀 Quick Start

### 1. **Prerequisites**
- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificates (for HTTPS)

### 2. **Clone and Setup**
```bash
git clone <your-repo>
cd htmx_demo
```

### 3. **Environment Configuration**
Create a `.env` file:
```bash
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_DEBUG=False

# Database (if using PostgreSQL)
POSTGRES_DB=htmx_demo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure-password-here
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis (if using Redis)
REDIS_URL=redis://redis:6379/0
```

### 4. **Build and Deploy**
```bash
# Build the application
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### 5. **Access Your Application**
- **HTTP**: http://yourdomain.com
- **HTTPS**: https://yourdomain.com (after SSL setup)

## 🔧 Configuration Options

### **Basic Setup (SQLite)**
The default setup uses SQLite and is ready to run immediately. Just uncomment the database section in `docker-compose.yml` if you want to use PostgreSQL.

### **PostgreSQL Database**
1. Uncomment the `db` service in `docker-compose.yml`
2. Uncomment the database settings in `htmx_demo/production.py`
3. Set database environment variables in `.env`

### **Redis Caching**
1. Uncomment the `redis` service in `docker-compose.yml`
2. Uncomment the cache settings in `htmx_demo/production.py`
3. Set Redis environment variables in `.env`

### **HTTPS/SSL Setup**
1. Place your SSL certificates in `./ssl/`
2. Uncomment the SSL volume in `docker-compose.yml`
3. Uncomment the HTTPS server block in `nginx/conf.d/default.conf`
4. Update the server name in nginx config

## 📊 Production Settings

### **Django Production Settings**
The `htmx_demo/production.py` file includes:
- Security headers and HTTPS settings
- Performance optimizations
- Proper logging configuration
- Database and cache settings
- Static file handling with WhiteNoise

### **Nginx Configuration**
The nginx setup includes:
- Reverse proxy to Django
- Static file serving
- Gzip compression
- Rate limiting
- Security headers
- SSL termination (when configured)

### **Gunicorn Configuration**
Gunicorn is configured with:
- 3 worker processes
- 120-second timeout
- Health checks
- Non-root user for security

## 🔒 Security Features

### **Django Security**
- CSRF protection enabled
- XSS protection headers
- HSTS headers
- Secure cookie settings
- Content type sniffing protection

### **Nginx Security**
- Rate limiting
- Security headers
- Request size limits
- SSL/TLS configuration ready

### **Docker Security**
- Non-root user in containers
- Minimal base images
- Health checks
- Resource limits

## 📈 Performance Optimizations

### **Static Files**
- WhiteNoise for serving static files
- Gzip compression
- Long-term caching headers
- CDN ready

### **Database**
- Connection pooling
- Query optimization ready
- Migration management

### **Caching**
- Redis integration ready
- Cache middleware configured
- Session caching support

## 🚨 Monitoring and Health Checks

### **Health Check Endpoints**
- `/health/` - Application health
- Docker health checks for all services
- Nginx health monitoring

### **Logging**
- Structured logging configuration
- File and console output
- Log rotation ready

### **Metrics**
- Response time monitoring
- Error rate tracking
- Resource usage monitoring

## 🔄 Deployment Workflow

### **1. Development**
```bash
# Run locally with development settings
python manage.py runserver
```

### **2. Testing**
```bash
# Test with production settings
DJANGO_SETTINGS_MODULE=htmx_demo.production python manage.py check
```

### **3. Staging**
```bash
# Deploy to staging environment
docker-compose -f docker-compose.staging.yml up -d
```

### **4. Production**
```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

## 🛠️ Maintenance

### **Updates**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **Database Backups**
```bash
# PostgreSQL backup
docker-compose exec db pg_dump -U postgres htmx_demo > backup.sql

# Restore
docker-compose exec -T db psql -U postgres htmx_demo < backup.sql
```

### **Log Rotation**
```bash
# View logs
docker-compose logs -f web

# Clear logs
docker-compose exec web truncate -s 0 /var/log/django/django.log
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Application Won't Start**
```bash
# Check logs
docker-compose logs web

# Check container status
docker-compose ps

# Restart services
docker-compose restart web
```

#### **Static Files Not Loading**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check nginx logs
docker-compose logs nginx
```

#### **Database Connection Issues**
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# Check Django database
docker-compose exec web python manage.py dbshell
```

### **Performance Issues**
```bash
# Check resource usage
docker stats

# Monitor nginx access logs
docker-compose exec nginx tail -f /var/log/nginx/access.log
```

## 📚 Additional Resources

### **Docker Commands**
```bash
# View running containers
docker ps

# Execute commands in container
docker-compose exec web python manage.py shell

# View container logs
docker-compose logs -f [service-name]

# Scale services
docker-compose up -d --scale web=3
```

### **Environment Variables**
- `DJANGO_SETTINGS_MODULE`: Which settings file to use
- `DJANGO_DEBUG`: Enable/disable debug mode
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection string

## 🎯 Next Steps

1. **SSL Setup**: Configure Let's Encrypt or your SSL provider
2. **Domain Configuration**: Point your domain to your server
3. **Monitoring**: Set up application monitoring (Prometheus, Grafana)
4. **Backup Strategy**: Implement automated database backups
5. **CI/CD Pipeline**: Set up automated deployment
6. **Load Balancing**: Add multiple application instances
7. **CDN**: Configure CDN for static files

## 🆘 Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables
3. Check Docker and Docker Compose versions
4. Ensure all ports are accessible
5. Verify SSL certificates (if using HTTPS)

---

**Happy Deploying! 🚀**

This setup provides a solid foundation for production deployment. Customize it based on your specific needs and infrastructure requirements.
