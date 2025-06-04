# Kubernetes Orchestration Guide
**Container Orchestration for Scalable Matrix Online Infrastructure**

> *"I know kung fu."* - Neo (And with Kubernetes, your infrastructure will know how to scale, heal, and adapt automatically.)

## 🎯 **The Vision of Self-Managing Infrastructure**

Matrix Online's revival demands infrastructure that can automatically scale with player populations, heal from failures, and deploy updates seamlessly across global regions. Kubernetes transforms MXO from a traditional server setup into a cloud-native, self-managing platform that embodies the adaptability and resilience of the Matrix itself.

## 🏗️ **Kubernetes Architecture Overview**

### MXO Cluster Design

```yaml
cluster_architecture:
  control_plane:
    high_availability: "3 master nodes across availability zones"
    etcd_cluster: "Distributed configuration storage"
    api_server: "RESTful API for all cluster operations"
    scheduler: "Intelligent pod placement based on resources"
    controller_manager: "Desired state management"
    
  worker_nodes:
    game_servers:
      node_type: "compute-optimized"
      instance_types: ["c5.2xlarge", "c5.4xlarge", "c5.9xlarge"]
      auto_scaling: "2-50 nodes based on demand"
      
    database_nodes:
      node_type: "memory-optimized"
      instance_types: ["r5.xlarge", "r5.2xlarge", "r5.4xlarge"]
      persistent_storage: "EBS gp3 with encryption"
      
    cache_nodes:
      node_type: "memory-optimized"
      instance_types: ["r5.large", "r5.xlarge"]
      local_storage: "NVMe SSD for ultra-low latency"
      
  networking:
    cni: "AWS VPC CNI for native VPC networking"
    service_mesh: "Istio for advanced traffic management"
    load_balancer: "AWS ALB Ingress Controller"
    dns: "CoreDNS with custom game service discovery"
```

### Namespace Organization

```yaml
# namespaces.yml - Logical separation of MXO components
apiVersion: v1
kind: Namespace
metadata:
  name: mxo-production
  labels:
    environment: production
    app: matrix-online
---
apiVersion: v1
kind: Namespace
metadata:
  name: mxo-staging
  labels:
    environment: staging
    app: matrix-online
---
apiVersion: v1
kind: Namespace
metadata:
  name: mxo-monitoring
  labels:
    purpose: monitoring
    app: matrix-online
---
apiVersion: v1
kind: Namespace
metadata:
  name: mxo-ingress
  labels:
    purpose: ingress
    app: matrix-online
```

## 🎮 **Game Server Deployment**

### StatefulSet for Game Servers

```yaml
# game-server-statefulset.yml - Persistent game server instances
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mxo-game-server
  namespace: mxo-production
  labels:
    app: mxo-game-server
    component: game-logic
spec:
  serviceName: mxo-game-server-headless
  replicas: 3
  selector:
    matchLabels:
      app: mxo-game-server
  template:
    metadata:
      labels:
        app: mxo-game-server
        component: game-logic
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: mxo-game-server
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: game-server
        image: mxo/game-server:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 7000
          name: game-port
          protocol: TCP
        - containerPort: 7001
          name: admin-port
          protocol: TCP
        - containerPort: 8080
          name: metrics
          protocol: TCP
        env:
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: SERVER_ID
          value: "$(POD_NAME)"
        - name: CLUSTER_MODE
          value: "kubernetes"
        envFrom:
        - configMapRef:
            name: mxo-game-config
        - secretRef:
            name: mxo-game-secrets
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: admin-port
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: admin-port
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health/startup
            port: admin-port
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
        volumeMounts:
        - name: game-data
          mountPath: /opt/mxo/data
        - name: config-volume
          mountPath: /opt/mxo/config
          readOnly: true
        - name: logs
          mountPath: /opt/mxo/logs
      volumes:
      - name: config-volume
        configMap:
          name: mxo-game-config
      - name: logs
        emptyDir: {}
      initContainers:
      - name: database-migration
        image: mxo/database-migrator:v1.2.3
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: mxo-database-secret
              key: host
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mxo-database-secret
              key: password
        command:
        - /bin/sh
        - -c
        - |
          echo "Running database migrations..."
          /opt/mxo/migrate --config /opt/mxo/config/migration.yml up
          echo "Database migrations completed"
  volumeClaimTemplates:
  - metadata:
      name: game-data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: gp3-encrypted
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: Service
metadata:
  name: mxo-game-server-headless
  namespace: mxo-production
  labels:
    app: mxo-game-server
spec:
  clusterIP: None
  selector:
    app: mxo-game-server
  ports:
  - name: game-port
    port: 7000
    targetPort: 7000
  - name: admin-port
    port: 7001
    targetPort: 7001
---
apiVersion: v1
kind: Service
metadata:
  name: mxo-game-server-lb
  namespace: mxo-production
  labels:
    app: mxo-game-server
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
spec:
  type: LoadBalancer
  selector:
    app: mxo-game-server
  ports:
  - name: game-port
    port: 7000
    targetPort: 7000
    protocol: TCP
```

### Horizontal Pod Autoscaler

```yaml
# game-server-hpa.yml - Auto-scaling based on metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mxo-game-server-hpa
  namespace: mxo-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: mxo-game-server
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: mxo_players_per_server
      target:
        type: AverageValue
        averageValue: "80"  # Scale when avg players per server > 80
  - type: External
    external:
      metric:
        name: mxo_queue_length
        selector:
          matchLabels:
            queue: player-login
      target:
        type: AverageValue
        averageValue: "10"  # Scale when login queue > 10
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
---
apiVersion: autoscaling/v2
kind: VerticalPodAutoscaler
metadata:
  name: mxo-game-server-vpa
  namespace: mxo-production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: mxo-game-server
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: game-server
      minAllowed:
        cpu: 500m
        memory: 1Gi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
```

## 🗄️ **Database and Persistence**

### MySQL Cluster with Operators

```yaml
# mysql-cluster.yml - High-availability MySQL deployment
apiVersion: mysql.oracle.com/v2
kind: InnoDBCluster
metadata:
  name: mxo-mysql-cluster
  namespace: mxo-production
spec:
  secretName: mxo-mysql-secret
  tlsUseSelfSigned: true
  instances: 3
  router:
    instances: 2
  datadirVolumeClaimTemplate:
    accessModes:
      - ReadWriteOnce
    resources:
      requests:
        storage: 100Gi
    storageClassName: gp3-encrypted
  mycnf: |
    [mysqld]
    max_connections = 1000
    innodb_buffer_pool_size = 4G
    innodb_log_file_size = 512M
    innodb_flush_log_at_trx_commit = 2
    innodb_file_per_table = 1
    
    # Matrix Online specific optimizations
    sql_mode = "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO"
    character_set_server = utf8mb4
    collation_server = utf8mb4_unicode_ci
    
    # Query optimization
    query_cache_type = 1
    query_cache_size = 256M
    tmp_table_size = 128M
    max_heap_table_size = 128M
    
    # Binary logging for replication
    log_bin = mysql-bin
    binlog_format = ROW
    expire_logs_days = 7
    
    # Performance monitoring
    performance_schema = ON
    
  podSpec:
    resources:
      requests:
        cpu: 2000m
        memory: 8Gi
      limits:
        cpu: 4000m
        memory: 16Gi
    nodeSelector:
      workload-type: database
    tolerations:
    - key: database-node
      operator: Equal
      value: "true"
      effect: NoSchedule
---
apiVersion: v1
kind: Secret
metadata:
  name: mxo-mysql-secret
  namespace: mxo-production
type: Opaque
stringData:
  rootUser: root
  rootHost: "%"
  rootPassword: "mxo_secure_root_password_2025"
```

### Redis Cluster for Caching

```yaml
# redis-cluster.yml - High-performance caching layer
apiVersion: redis.io/v1beta2
kind: RedisCluster
metadata:
  name: mxo-redis-cluster
  namespace: mxo-production
spec:
  numberOfMaster: 3
  replicationFactor: 1
  
  redisLeader:
    replicas: 3
    resources:
      requests:
        cpu: 1000m
        memory: 4Gi
      limits:
        cpu: 2000m
        memory: 8Gi
    storage:
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 20Gi
          storageClassName: gp3-encrypted
    nodeSelector:
      workload-type: cache
    redisConfig:
      maxmemory: "6gb"
      maxmemory-policy: "allkeys-lru"
      save: "900 1 300 10 60 10000"
      tcp-keepalive: "60"
      timeout: "300"
      
  redisFollower:
    replicas: 3
    resources:
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: 1000m
        memory: 4Gi
    storage:
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 20Gi
          storageClassName: gp3-encrypted
    nodeSelector:
      workload-type: cache
    redisConfig:
      maxmemory: "3gb"
      maxmemory-policy: "allkeys-lru"
      tcp-keepalive: "60"
      timeout: "300"
      
  sentinel:
    replicas: 3
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
    sentinelConfig:
      down-after-milliseconds: "5000"
      failover-timeout: "10000"
      parallel-syncs: "1"
```

## 🌐 **Service Mesh and Networking**

### Istio Service Mesh Configuration

```yaml
# istio-gateway.yml - Ingress gateway for MXO traffic
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: mxo-gateway
  namespace: mxo-production
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "mxo.example.com"
    - "api.mxo.example.com"
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "mxo.example.com"
    - "api.mxo.example.com"
    tls:
      mode: SIMPLE
      credentialName: mxo-tls-cert
  - port:
      number: 7000
      name: game-tcp
      protocol: TCP
    hosts:
    - "game.mxo.example.com"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: mxo-virtualservice
  namespace: mxo-production
spec:
  hosts:
  - "mxo.example.com"
  - "api.mxo.example.com"
  gateways:
  - mxo-gateway
  http:
  - match:
    - uri:
        prefix: "/api/v1/"
    route:
    - destination:
        host: mxo-api-service
        port:
          number: 8080
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
  - match:
    - uri:
        prefix: "/game-assets/"
    route:
    - destination:
        host: mxo-asset-service
        port:
          number: 8080
    headers:
      response:
        add:
          cache-control: "public, max-age=86400"
  - match:
    - uri:
        prefix: "/"
    route:
    - destination:
        host: mxo-web-service
        port:
          number: 8080
  tcp:
  - match:
    - port: 7000
    route:
    - destination:
        host: mxo-game-server-lb
        port:
          number: 7000
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: mxo-game-server-dr
  namespace: mxo-production
spec:
  host: mxo-game-server-lb
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1000
        connectTimeout: 30s
        keepAlive:
          time: 7200s
          interval: 75s
      http:
        http1MaxPendingRequests: 100
        maxRequestsPerConnection: 10
    loadBalancer:
      consistentHash:
        httpHeaderName: "X-Player-ID"  # Sticky sessions by player
    outlierDetection:
      consecutiveGatewayErrors: 3
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: mxo-mtls
  namespace: mxo-production
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: mxo-authz
  namespace: mxo-production
spec:
  selector:
    matchLabels:
      app: mxo-game-server
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/mxo-production/sa/mxo-api-service"]
    - source:
        principals: ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]
    to:
    - operation:
        methods: ["GET", "POST"]
        ports: ["7000", "7001"]
```

## 📊 **Monitoring and Observability**

### Prometheus Monitoring Stack

```yaml
# prometheus-stack.yml - Comprehensive monitoring for MXO
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: mxo-prometheus
  namespace: mxo-monitoring
spec:
  serviceAccountName: prometheus
  serviceMonitorSelector:
    matchLabels:
      team: mxo
  ruleSelector:
    matchLabels:
      team: mxo
  resources:
    requests:
      memory: 4Gi
      cpu: 2000m
    limits:
      memory: 8Gi
      cpu: 4000m
  retention: 30d
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: gp3-encrypted
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
  nodeSelector:
    workload-type: monitoring
  tolerations:
  - key: monitoring-node
    operator: Equal
    value: "true"
    effect: NoSchedule
  additionalScrapeConfigs:
    name: additional-scrape-configs
    key: prometheus-additional.yaml
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: mxo-game-server-metrics
  namespace: mxo-monitoring
  labels:
    team: mxo
spec:
  selector:
    matchLabels:
      app: mxo-game-server
  namespaceSelector:
    matchNames:
    - mxo-production
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    honorLabels: true
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: mxo-alerts
  namespace: mxo-monitoring
  labels:
    team: mxo
spec:
  groups:
  - name: mxo.game-server
    interval: 30s
    rules:
    - alert: MXOGameServerDown
      expr: up{job="mxo-game-server"} == 0
      for: 5m
      labels:
        severity: critical
        component: game-server
      annotations:
        summary: "MXO Game Server is down"
        description: "Game server {{ $labels.instance }} has been down for more than 5 minutes"
        
    - alert: MXOHighPlayerLatency
      expr: histogram_quantile(0.95, rate(mxo_player_latency_seconds_bucket[5m])) > 0.5
      for: 2m
      labels:
        severity: warning
        component: network
      annotations:
        summary: "High player latency detected"
        description: "95th percentile latency is {{ $value }}s on {{ $labels.instance }}"
        
    - alert: MXOHighMemoryUsage
      expr: (container_memory_usage_bytes{pod=~"mxo-game-server-.*"} / container_spec_memory_limit_bytes) > 0.9
      for: 10m
      labels:
        severity: warning
        component: resources
      annotations:
        summary: "High memory usage on game server"
        description: "Memory usage is {{ $value | humanizePercentage }} on {{ $labels.pod }}"
        
    - alert: MXODatabaseConnectionPool
      expr: mysql_global_status_threads_connected / mysql_global_variables_max_connections > 0.8
      for: 5m
      labels:
        severity: warning
        component: database
      annotations:
        summary: "Database connection pool nearly exhausted"
        description: "{{ $value | humanizePercentage }} of database connections in use"
        
    - alert: MXOLowPlayerCount
      expr: sum(mxo_players_online_total) < 10
      for: 30m
      labels:
        severity: info
        component: business
      annotations:
        summary: "Low player count detected"
        description: "Only {{ $value }} players online across all servers"
```

### Custom Resource Definitions

```yaml
# mxo-crd.yml - Custom resources for Matrix Online
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: gameservers.mxo.io
spec:
  group: mxo.io
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              region:
                type: string
                enum: ["us-east", "eu-west", "asia-pacific"]
              maxPlayers:
                type: integer
                minimum: 50
                maximum: 200
              gameMode:
                type: string
                enum: ["production", "staging", "dev"]
              districts:
                type: array
                items:
                  type: object
                  properties:
                    name:
                      type: string
                    maxPlayers:
                      type: integer
                    enabled:
                      type: boolean
          status:
            type: object
            properties:
              phase:
                type: string
                enum: ["Pending", "Running", "Failed"]
              currentPlayers:
                type: integer
              readyDistricts:
                type: integer
              lastHeartbeat:
                type: string
                format: date-time
    additionalPrinterColumns:
    - name: Region
      type: string
      jsonPath: .spec.region
    - name: Current Players
      type: integer
      jsonPath: .status.currentPlayers
    - name: Max Players
      type: integer
      jsonPath: .spec.maxPlayers
    - name: Phase
      type: string
      jsonPath: .status.phase
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
  scope: Namespaced
  names:
    plural: gameservers
    singular: gameserver
    kind: GameServer
    shortNames:
    - gs
---
apiVersion: mxo.io/v1
kind: GameServer
metadata:
  name: us-east-1
  namespace: mxo-production
spec:
  region: us-east
  maxPlayers: 150
  gameMode: production
  districts:
  - name: downtown
    maxPlayers: 50
    enabled: true
  - name: westview
    maxPlayers: 50
    enabled: true
  - name: international
    maxPlayers: 50
    enabled: true
```

## 🔄 **CI/CD Integration**

### GitOps with ArgoCD

```yaml
# argocd-application.yml - GitOps deployment for MXO
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mxo-production
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: mxo
  source:
    repoURL: https://github.com/mxo-team/k8s-manifests
    targetRevision: main
    path: environments/production
    helm:
      valueFiles:
      - values.yaml
      - secrets+gpg-import:///helm-secrets-private-keys/key.asc?values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: mxo-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
---
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: mxo
  namespace: argocd
spec:
  description: Matrix Online Project
  sourceRepos:
  - 'https://github.com/mxo-team/*'
  destinations:
  - namespace: 'mxo-*'
    server: https://kubernetes.default.svc
  - namespace: istio-system
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: rbac.authorization.k8s.io
    kind: ClusterRole
  - group: rbac.authorization.k8s.io
    kind: ClusterRoleBinding
  namespaceResourceWhitelist:
  - group: ''
    kind: ConfigMap
  - group: ''
    kind: Secret
  - group: ''
    kind: Service
  - group: apps
    kind: Deployment
  - group: apps
    kind: StatefulSet
  - group: networking.k8s.io
    kind: Ingress
  roles:
  - name: admin
    description: Full access to MXO project
    policies:
    - p, proj:mxo:admin, applications, *, mxo/*, allow
    - p, proj:mxo:admin, repositories, *, *, allow
    groups:
    - mxo-team:admins
  - name: developer
    description: Developer access to MXO project
    policies:
    - p, proj:mxo:developer, applications, get, mxo/*, allow
    - p, proj:mxo:developer, applications, sync, mxo/*, allow
    groups:
    - mxo-team:developers
```

### Pipeline Integration

```yaml
# tekton-pipeline.yml - CI/CD pipeline for MXO
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: mxo-build-deploy
  namespace: mxo-ci
spec:
  description: Build and deploy Matrix Online components
  params:
  - name: git-url
    type: string
    description: Git repository URL
  - name: git-revision
    type: string
    description: Git revision to build
    default: main
  - name: image-registry
    type: string
    description: Container registry URL
    default: "your-registry.com/mxo"
  - name: environment
    type: string
    description: Target environment
    default: staging
  workspaces:
  - name: shared-data
    description: Shared workspace for pipeline
  - name: git-credentials
    description: Git credentials
  - name: registry-credentials
    description: Container registry credentials
    
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
    workspaces:
    - name: output
      workspace: shared-data
    - name: ssh-directory
      workspace: git-credentials
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)
      
  - name: run-tests
    runAfter: ["fetch-source"]
    taskRef:
      name: golang-test
    workspaces:
    - name: source
      workspace: shared-data
    params:
    - name: package
      value: "./..."
    - name: flags
      value: "-v -race -coverprofile=coverage.out"
      
  - name: security-scan
    runAfter: ["fetch-source"]
    taskRef:
      name: trivy-scanner
    workspaces:
    - name: source
      workspace: shared-data
    params:
    - name: ARGS
      value: ["filesystem", "--exit-code", "1", "--severity", "HIGH,CRITICAL", "."]
      
  - name: build-image
    runAfter: ["run-tests", "security-scan"]
    taskRef:
      name: buildah
    workspaces:
    - name: source
      workspace: shared-data
    - name: dockerconfig
      workspace: registry-credentials
    params:
    - name: IMAGE
      value: "$(params.image-registry)/game-server:$(params.git-revision)"
    - name: DOCKERFILE
      value: "./Dockerfile"
      
  - name: deploy-staging
    when:
    - input: "$(params.environment)"
      operator: in
      values: ["staging", "production"]
    runAfter: ["build-image"]
    taskRef:
      name: argocd-task-sync-and-wait
    params:
    - name: application-name
      value: "mxo-$(params.environment)"
    - name: revision
      value: "$(params.git-revision)"
    - name: flags
      value: "--grpc-web"
      
  - name: integration-tests
    when:
    - input: "$(params.environment)"
      operator: in
      values: ["staging"]
    runAfter: ["deploy-staging"]
    taskRef:
      name: mxo-integration-tests
    params:
    - name: environment
      value: "$(params.environment)"
    - name: test-suite
      value: "smoke"
      
  finally:
  - name: notify
    taskRef:
      name: slack-notify
    params:
    - name: webhook-secret
      value: slack-webhook
    - name: message
      value: |
        MXO Pipeline $(context.pipelineRun.name) completed with status: $(tasks.status)
        Environment: $(params.environment)
        Revision: $(params.git-revision)
```

## 🔒 **Security and Compliance**

### Pod Security Standards

```yaml
# pod-security-policy.yml - Security constraints for MXO pods
apiVersion: v1
kind: Namespace
metadata:
  name: mxo-production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mxo-network-policy
  namespace: mxo-production
spec:
  podSelector:
    matchLabels:
      app: mxo-game-server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: istio-system
    - namespaceSelector:
        matchLabels:
          name: mxo-production
    ports:
    - protocol: TCP
      port: 7000
    - protocol: TCP
      port: 7001
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: mxo-production
    ports:
    - protocol: TCP
      port: 3306  # MySQL
    - protocol: TCP
      port: 6379  # Redis
  - to: []  # Allow all external traffic for API calls
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 80
    - protocol: UDP
      port: 53
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mxo-game-server
  namespace: mxo-production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT:role/MXOGameServerRole
automountServiceAccountToken: true
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: mxo-production
  name: mxo-game-server-role
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["mxo.io"]
  resources: ["gameservers"]
  verbs: ["get", "list", "watch", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mxo-game-server-binding
  namespace: mxo-production
subjects:
- kind: ServiceAccount
  name: mxo-game-server
  namespace: mxo-production
roleRef:
  kind: Role
  name: mxo-game-server-role
  apiGroup: rbac.authorization.k8s.io
```

## Remember

> *"What is real? How do you define real?"* - Morpheus

Kubernetes isn't just container orchestration - it's the infrastructure that makes the Matrix truly resilient and scalable. Every pod that heals itself, every service that routes traffic intelligently, and every deployment that rolls out seamlessly brings us closer to a self-managing digital world.

In Kubernetes, we find not just orchestration, but liberation from the constraints of traditional infrastructure. The Matrix becomes truly elastic, adapting to demand, healing from failures, and evolving without human intervention.

**Orchestrate with purpose. Scale with intelligence. Build the self-managing Matrix.**

---

**Guide Status**: 🟢 COMPREHENSIVE ORCHESTRATION  
**Infrastructure Intelligence**: 🤖 SELF-MANAGING  
**Liberation Impact**: ⭐⭐⭐⭐⭐  

*In containers we find portability. In orchestration we find intelligence. In Kubernetes we find the autonomous Matrix that manages itself.*

---

[← Development Hub](index.md) | [← Cloud Deployment](cloud-deployment-guides.md) | [→ Microservices Architecture](microservices-architecture-guide.md)