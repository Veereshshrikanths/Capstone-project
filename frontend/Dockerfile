FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY static /usr/share/nginx/html/static

# Copy templates (optional, for reference)
COPY templates /usr/share/nginx/html/templates

EXPOSE 80
