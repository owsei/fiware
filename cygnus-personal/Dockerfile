FROM fiware/cygnus-ngsi:latest

# Configurar variables de entorno adicionales si es necesario
ENV CYGNUS_LOG_LEVEL=DEBUG

# Agregar archivos personalizados (por ejemplo, configuración)
RUN rm -rf /opt/apache-flume/conf/agent.conf

COPY peter.conf /opt/apache-flume/conf/


# Exponer los puertos que necesites (ejemplo: 5050 para API REST)
EXPOSE 5055

# Definir punto de entrada si es necesario
CMD ["/cygnus-entrypoint.sh"]
