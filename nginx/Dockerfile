FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/nginx.conf

COPY nginx.conf /etc/nginx/conf.d/

# Copy static files from frontend build
# (This will be replaced by a volume mount in docker-compose)
COPY ./frontend/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]