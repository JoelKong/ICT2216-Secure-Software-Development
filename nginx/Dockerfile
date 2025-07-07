FROM owasp/modsecurity-crs:nginx-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY modsecurity /etc/nginx/modsecurity

RUN mkdir -p /run && chown -R nginx:nginx /run

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
