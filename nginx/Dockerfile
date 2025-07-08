FROM owasp/modsecurity-crs:nginx-alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY modsecurity /etc/nginx/modsecurity

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
