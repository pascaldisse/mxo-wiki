# Automated Testing Framework for Code Examples Guide
**Ensuring Code Quality and Reliability Across the Digital Realm**

> *"There is a difference between knowing the path and walking the path."* - Morpheus (And there is a difference between writing code and knowing it works. Automated testing transforms uncertainty into confidence, ensuring every example guides users down the correct path.)

## 🎯 **The Vision of Verified Knowledge**

Documentation with untested code examples is like maps to places that may not exist. This guide presents a comprehensive automated testing framework that continuously validates every code example, tutorial, and implementation guide across the Matrix Online wiki, ensuring that knowledge remains accurate, functional, and trustworthy.

## 🧪 **Testing Philosophy and Architecture**

### Multi-Language Test Orchestration

```yaml
testing_architecture:
  testing_principles:
    living_documentation:
      description: "Code examples that execute and validate continuously"
      benefit: "Examples stay current with technology changes"
      
    polyglot_support:
      description: "Test runners for multiple programming languages"
      languages: ["Go", "TypeScript", "Python", "Rust", "JavaScript", "Bash"]
      
    environment_isolation:
      description: "Containerized testing prevents conflicts"
      benefits: ["Reproducible results", "Clean state", "Version control"]
      
    progressive_complexity:
      description: "Simple tests for basic examples, comprehensive for complex systems"
      levels: ["Syntax validation", "Unit tests", "Integration tests", "End-to-end tests"]

  test_execution_strategy:
    continuous_validation:
      frequency: "Every commit, daily full suite"
      scope: "All modified examples plus dependencies"
      
    parallel_execution:
      description: "Concurrent testing across multiple environments"
      scaling: "Dynamic container allocation based on load"
      
    smart_dependency_tracking:
      description: "Only test affected examples when dependencies change"
      optimization: "Reduces test time by 70-80%"
```

## 🚀 **Core Testing Framework Implementation**

### Multi-Language Test Orchestrator

```go
// testing-framework/main.go - Comprehensive code example testing system
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"
    "path/filepath"
    "strings"
    "sync"
    "time"
    
    "github.com/docker/docker/api/types"
    "github.com/docker/docker/api/types/container"
    "github.com/docker/docker/client"
    "github.com/gorilla/mux"
    "go.opentelemetry.io/otel/trace"
)

type TestFramework struct {
    // Core components
    dockerClient    *client.Client
    testRunners     map[string]TestRunner
    dependencyGraph *DependencyGraph
    resultStore     *TestResultStore
    
    // Execution management
    executionQueue  chan TestJob
    workerPool      *WorkerPool
    
    // Configuration and monitoring
    config          TestConfig
    metrics         *TestMetrics
    tracer          trace.Tracer
    mutex           sync.RWMutex
}

type TestJob struct {
    ID              string                 `json:"id"`
    ExampleID       string                 `json:"example_id"`
    FilePath        string                 `json:"file_path"`
    Language        string                 `json:"language"`
    TestType        TestType               `json:"test_type"`
    Dependencies    []string               `json:"dependencies"`
    Environment     map[string]string      `json:"environment"`
    Timeout         time.Duration          `json:"timeout"`
    Priority        Priority               `json:"priority"`
    RetryPolicy     RetryPolicy            `json:"retry_policy"`
    CreatedAt       time.Time              `json:"created_at"`
    ScheduledAt     time.Time              `json:"scheduled_at,omitempty"`
}

type TestResult struct {
    JobID           string                 `json:"job_id"`
    ExampleID       string                 `json:"example_id"`
    Status          TestStatus             `json:"status"`
    ExecutionTime   time.Duration          `json:"execution_time"`
    Output          string                 `json:"output"`
    ErrorOutput     string                 `json:"error_output,omitempty"`
    ExitCode        int                    `json:"exit_code"`
    
    // Detailed test information
    TestDetails     TestDetails            `json:"test_details"`
    Coverage        *CoverageInfo          `json:"coverage,omitempty"`
    Performance     *PerformanceMetrics    `json:"performance,omitempty"`
    
    // Metadata
    Environment     map[string]string      `json:"environment"`
    StartTime       time.Time              `json:"start_time"`
    EndTime         time.Time              `json:"end_time"`
    WorkerID        string                 `json:"worker_id"`
    
    // Quality metrics
    CodeQuality     *CodeQualityMetrics    `json:"code_quality,omitempty"`
    SecurityScan    *SecurityScanResult    `json:"security_scan,omitempty"`
}

type TestRunner interface {
    Name() string
    SupportedLanguages() []string
    CanHandle(example CodeExample) bool
    PrepareTest(ctx context.Context, example CodeExample) (*TestConfiguration, error)
    ExecuteTest(ctx context.Context, config TestConfiguration) (*TestResult, error)
    ValidateExample(example CodeExample) []ValidationIssue
}

// Language-specific test runners

type GoTestRunner struct {
    goVersion       string
    buildCache      *BuildCache
    moduleCache     *ModuleCache
    lintTools       []string
}

func (gtr *GoTestRunner) Name() string {
    return "go-test-runner"
}

func (gtr *GoTestRunner) SupportedLanguages() []string {
    return []string{"go", "golang"}
}

func (gtr *GoTestRunner) CanHandle(example CodeExample) bool {
    return example.Language == "go" || 
           strings.Contains(example.Content, "package ") ||
           strings.Contains(example.FilePath, ".go")
}

func (gtr *GoTestRunner) PrepareTest(ctx context.Context, example CodeExample) (*TestConfiguration, error) {
    ctx, span := trace.SpanFromContext(ctx).TracerProvider().Tracer("test-framework").Start(ctx, "go_prepare_test")
    defer span.End()
    
    config := &TestConfiguration{
        Language:     "go",
        WorkingDir:   fmt.Sprintf("/tmp/test_%s", example.ID),
        TestCommands: []string{},
        Environment:  make(map[string]string),
        Dependencies: []string{},
    }
    
    // Analyze Go code to determine test strategy
    if strings.Contains(example.Content, "func main()") {
        // Executable Go program
        config.TestType = TestTypeExecution
        config.TestCommands = []string{
            "go mod init test_module",
            "go mod tidy",
            "go build -o test_binary .",
            "./test_binary",
        }
    } else if strings.Contains(example.Content, "func Test") {
        // Go test file
        config.TestType = TestTypeUnit
        config.TestCommands = []string{
            "go mod init test_module",
            "go mod tidy",
            "go test -v -cover ./...",
        }
    } else if strings.Contains(example.Content, "package ") {
        // Go package/library
        config.TestType = TestTypeCompilation
        config.TestCommands = []string{
            "go mod init test_module",
            "go mod tidy",
            "go build ./...",
            "go vet ./...",
            "golint ./...",
        }
    }
    
    // Extract Go module dependencies
    dependencies := gtr.extractGoDependencies(example.Content)
    config.Dependencies = dependencies
    
    // Set Go environment
    config.Environment["GO111MODULE"] = "on"
    config.Environment["GOPROXY"] = "https://proxy.golang.org,direct"
    config.Environment["CGO_ENABLED"] = "0"
    
    // Add Go version specification
    config.DockerImage = fmt.Sprintf("golang:%s-alpine", gtr.goVersion)
    
    return config, nil
}

func (gtr *GoTestRunner) ExecuteTest(ctx context.Context, config TestConfiguration) (*TestResult, error) {
    ctx, span := trace.SpanFromContext(ctx).TracerProvider().Tracer("test-framework").Start(ctx, "go_execute_test")
    defer span.End()
    
    startTime := time.Now()
    
    // Create Docker container for isolated execution
    containerConfig := &container.Config{
        Image:        config.DockerImage,
        WorkingDir:   "/workspace",
        Env:          envMapToSlice(config.Environment),
        Cmd:          []string{"sh", "-c", strings.Join(config.TestCommands, " && ")},
    }
    
    hostConfig := &container.HostConfig{
        AutoRemove: true,
        Resources: container.Resources{
            Memory:   512 * 1024 * 1024, // 512MB
            CPUQuota: 50000,              // 0.5 CPU
        },
    }
    
    // Execute in container
    result, err := gtr.executeInContainer(ctx, containerConfig, hostConfig, config.WorkingDir)
    if err != nil {
        return &TestResult{
            Status:        TestStatusFailed,
            ErrorOutput:   err.Error(),
            ExecutionTime: time.Since(startTime),
            StartTime:     startTime,
            EndTime:       time.Now(),
        }, nil
    }
    
    // Analyze results
    testResult := &TestResult{
        Status:        gtr.determineStatus(result.ExitCode, result.Output),
        ExecutionTime: time.Since(startTime),
        Output:        result.Output,
        ErrorOutput:   result.ErrorOutput,
        ExitCode:      result.ExitCode,
        StartTime:     startTime,
        EndTime:       time.Now(),
    }
    
    // Parse Go-specific outputs
    if strings.Contains(result.Output, "coverage:") {
        testResult.Coverage = gtr.parseCoverage(result.Output)
    }
    
    if strings.Contains(result.Output, "go vet") {
        testResult.CodeQuality = gtr.parseVetOutput(result.Output)
    }
    
    return testResult, nil
}

func (gtr *GoTestRunner) extractGoDependencies(content string) []string {
    var dependencies []string
    
    // Simple import parsing - in production, use go/parser
    lines := strings.Split(content, "\n")
    inImport := false
    
    for _, line := range lines {
        line = strings.TrimSpace(line)
        
        if strings.HasPrefix(line, "import (") {
            inImport = true
            continue
        }
        
        if inImport && line == ")" {
            inImport = false
            continue
        }
        
        if inImport || strings.HasPrefix(line, "import ") {
            // Extract import path
            if strings.Contains(line, "\"") {
                start := strings.Index(line, "\"")
                end := strings.LastIndex(line, "\"")
                if start != end && start != -1 {
                    importPath := line[start+1 : end]
                    if strings.Contains(importPath, ".") && !strings.HasPrefix(importPath, ".") {
                        dependencies = append(dependencies, importPath)
                    }
                }
            }
        }
    }
    
    return dependencies
}

// TypeScript/JavaScript Test Runner

type TypeScriptTestRunner struct {
    nodeVersion     string
    packageManager  string
    testFramework   string
}

func (tstr *TypeScriptTestRunner) Name() string {
    return "typescript-test-runner"
}

func (tstr *TypeScriptTestRunner) SupportedLanguages() []string {
    return []string{"typescript", "javascript", "ts", "js"}
}

func (tstr *TypeScriptTestRunner) PrepareTest(ctx context.Context, example CodeExample) (*TestConfiguration, error) {
    config := &TestConfiguration{
        Language:     "typescript",
        WorkingDir:   fmt.Sprintf("/tmp/test_%s", example.ID),
        TestCommands: []string{},
        Environment:  make(map[string]string),
        Dependencies: []string{},
    }
    
    // Create package.json
    packageJson := map[string]interface{}{
        "name":    "test-example",
        "version": "1.0.0",
        "scripts": map[string]string{
            "build": "tsc",
            "test":  "jest",
            "start": "node dist/index.js",
        },
        "devDependencies": map[string]string{
            "typescript": "^5.0.0",
            "@types/node": "^20.0.0",
            "jest":       "^29.0.0",
            "@types/jest": "^29.0.0",
            "ts-jest":    "^29.0.0",
        },
    }
    
    // Analyze code to add specific dependencies
    if strings.Contains(example.Content, "import React") {
        deps := packageJson["devDependencies"].(map[string]string)
        deps["react"] = "^18.0.0"
        deps["@types/react"] = "^18.0.0"
        deps["@testing-library/react"] = "^13.0.0"
    }
    
    config.PackageJson = packageJson
    
    // Determine test strategy
    if strings.Contains(example.Content, "describe(") || strings.Contains(example.Content, "test(") {
        config.TestType = TestTypeUnit
        config.TestCommands = []string{
            "npm install",
            "npm run test",
        }
    } else if strings.Contains(example.Content, "export") {
        config.TestType = TestTypeCompilation
        config.TestCommands = []string{
            "npm install",
            "npm run build",
        }
    } else {
        config.TestType = TestTypeExecution
        config.TestCommands = []string{
            "npm install",
            "npm run build",
            "npm start",
        }
    }
    
    config.DockerImage = fmt.Sprintf("node:%s-alpine", tstr.nodeVersion)
    
    return config, nil
}

// Python Test Runner

type PythonTestRunner struct {
    pythonVersion   string
    virtualEnv      bool
    linters         []string
}

func (ptr *PythonTestRunner) PrepareTest(ctx context.Context, example CodeExample) (*TestConfiguration, error) {
    config := &TestConfiguration{
        Language:     "python",
        WorkingDir:   fmt.Sprintf("/tmp/test_%s", example.ID),
        TestCommands: []string{},
        Environment:  make(map[string]string),
        Dependencies: []string{},
    }
    
    // Extract Python dependencies from imports
    dependencies := ptr.extractPythonDependencies(example.Content)
    config.Dependencies = dependencies
    
    // Create requirements.txt
    requirementsContent := strings.Join(dependencies, "\n")
    config.RequirementsTxt = requirementsContent
    
    // Determine test strategy
    if strings.Contains(example.Content, "def test_") || strings.Contains(example.Content, "import pytest") {
        config.TestType = TestTypeUnit
        config.TestCommands = []string{
            "pip install -r requirements.txt",
            "pip install pytest",
            "pytest -v",
        }
    } else if strings.Contains(example.Content, "if __name__ == '__main__':") {
        config.TestType = TestTypeExecution
        config.TestCommands = []string{
            "pip install -r requirements.txt",
            "python main.py",
        }
    } else {
        config.TestType = TestTypeCompilation
        config.TestCommands = []string{
            "pip install -r requirements.txt",
            "python -m py_compile *.py",
            "pylint *.py",
        }
    }
    
    config.DockerImage = fmt.Sprintf("python:%s-alpine", ptr.pythonVersion)
    
    return config, nil
}

// Test Orchestration and Scheduling

type TestOrchestrator struct {
    framework       *TestFramework
    scheduler       *TestScheduler
    dependencyGraph *DependencyGraph
    resultAggregator *ResultAggregator
}

func (to *TestOrchestrator) ProcessWikiUpdate(ctx context.Context, updateEvent WikiUpdateEvent) error {
    ctx, span := trace.SpanFromContext(ctx).TracerProvider().Tracer("test-orchestrator").Start(ctx, "process_wiki_update")
    defer span.End()
    
    // Extract code examples from updated content
    examples := to.extractCodeExamples(updateEvent.Content)
    
    // Determine which examples need testing
    var testJobs []TestJob
    
    for _, example := range examples {
        // Check if example has changed
        if to.hasExampleChanged(example, updateEvent) {
            job := TestJob{
                ID:           generateJobID(),
                ExampleID:    example.ID,
                FilePath:     example.FilePath,
                Language:     example.Language,
                TestType:     to.determineTestType(example),
                Dependencies: to.extractDependencies(example),
                Timeout:      to.calculateTimeout(example),
                Priority:     to.calculatePriority(example, updateEvent),
                CreatedAt:    time.Now(),
            }
            testJobs = append(testJobs, job)
        }
    }
    
    // Schedule dependent tests
    dependentExamples := to.dependencyGraph.FindDependents(examples)
    for _, depExample := range dependentExamples {
        job := TestJob{
            ID:           generateJobID(),
            ExampleID:    depExample.ID,
            FilePath:     depExample.FilePath,
            Language:     depExample.Language,
            TestType:     TestTypeDependency,
            Priority:     PriorityMedium,
            CreatedAt:    time.Now(),
        }
        testJobs = append(testJobs, job)
    }
    
    // Submit jobs to execution queue
    for _, job := range testJobs {
        select {
        case to.framework.executionQueue <- job:
            // Job queued successfully
        case <-ctx.Done():
            return ctx.Err()
        }
    }
    
    span.SetAttributes(
        trace.StringAttribute("wiki_page", updateEvent.PageID),
        trace.Int64Attribute("examples_found", int64(len(examples))),
        trace.Int64Attribute("jobs_scheduled", int64(len(testJobs))),
    )
    
    return nil
}

func (to *TestOrchestrator) RunFullSuite(ctx context.Context) (*TestSuiteResult, error) {
    ctx, span := trace.SpanFromContext(ctx).TracerProvider().Tracer("test-orchestrator").Start(ctx, "run_full_suite")
    defer span.End()
    
    startTime := time.Now()
    
    // Discover all code examples
    allExamples, err := to.discoverAllCodeExamples()
    if err != nil {
        return nil, fmt.Errorf("failed to discover code examples: %w", err)
    }
    
    // Create test plan with optimal execution order
    testPlan := to.createOptimalTestPlan(allExamples)
    
    // Execute test plan
    results := make([]*TestResult, 0, len(testPlan.Jobs))
    resultsChan := make(chan *TestResult, len(testPlan.Jobs))
    
    // Submit all jobs
    for _, job := range testPlan.Jobs {
        select {
        case to.framework.executionQueue <- job:
        case <-ctx.Done():
            return nil, ctx.Err()
        }
    }
    
    // Collect results
    for i := 0; i < len(testPlan.Jobs); i++ {
        select {
        case result := <-resultsChan:
            results = append(results, result)
        case <-ctx.Done():
            return nil, ctx.Err()
        }
    }
    
    // Aggregate results
    suiteResult := &TestSuiteResult{
        StartTime:       startTime,
        EndTime:         time.Now(),
        TotalTests:      len(results),
        PassedTests:     0,
        FailedTests:     0,
        SkippedTests:    0,
        TotalDuration:   time.Since(startTime),
        Results:         results,
        Coverage:        to.calculateOverallCoverage(results),
        QualityMetrics:  to.calculateQualityMetrics(results),
    }
    
    // Count test outcomes
    for _, result := range results {
        switch result.Status {
        case TestStatusPassed:
            suiteResult.PassedTests++
        case TestStatusFailed:
            suiteResult.FailedTests++
        case TestStatusSkipped:
            suiteResult.SkippedTests++
        }
    }
    
    suiteResult.SuccessRate = float64(suiteResult.PassedTests) / float64(suiteResult.TotalTests)
    
    return suiteResult, nil
}

// Continuous Integration Integration

type CIIntegration struct {
    framework   *TestFramework
    webhookHandler *WebhookHandler
    reportGenerator *ReportGenerator
    notificationSender *NotificationSender
}

func (ci *CIIntegration) HandleGitWebhook(ctx context.Context, webhook GitWebhook) error {
    // Extract changed files
    changedFiles := webhook.ChangedFiles
    
    // Find affected code examples
    affectedExamples := ci.findAffectedExamples(changedFiles)
    
    if len(affectedExamples) == 0 {
        return nil // No code examples affected
    }
    
    // Create test suite for affected examples
    testSuite := ci.createTestSuite(affectedExamples)
    
    // Execute tests
    results, err := ci.framework.ExecuteTestSuite(ctx, testSuite)
    if err != nil {
        return fmt.Errorf("test execution failed: %w", err)
    }
    
    // Generate report
    report := ci.reportGenerator.GenerateReport(results)
    
    // Send notifications
    if results.FailedTests > 0 {
        ci.notificationSender.SendFailureNotification(webhook.CommitSHA, report)
    } else {
        ci.notificationSender.SendSuccessNotification(webhook.CommitSHA, report)
    }
    
    // Update commit status
    ci.updateCommitStatus(webhook.CommitSHA, results)
    
    return nil
}

// Test Result Visualization and Reporting

type TestDashboard struct {
    resultStore     *TestResultStore
    metricsCalculator *MetricsCalculator
    reportGenerator *ReportGenerator
}

func (td *TestDashboard) GenerateDashboardData(ctx context.Context, timeRange TimeRange) (*DashboardData, error) {
    // Fetch test results for time range
    results, err := td.resultStore.GetResultsInRange(ctx, timeRange)
    if err != nil {
        return nil, err
    }
    
    // Calculate metrics
    metrics := td.metricsCalculator.CalculateMetrics(results)
    
    // Generate trend data
    trendData := td.generateTrendData(results, timeRange)
    
    // Language-specific breakdown
    languageBreakdown := td.calculateLanguageBreakdown(results)
    
    // Test type analysis
    testTypeAnalysis := td.analyzeTestTypes(results)
    
    dashboard := &DashboardData{
        Overview: DashboardOverview{
            TotalTests:       len(results),
            SuccessRate:      metrics.OverallSuccessRate,
            AverageExecTime:  metrics.AverageExecutionTime,
            TrendDirection:   trendData.Direction,
        },
        TrendData:         trendData,
        LanguageBreakdown: languageBreakdown,
        TestTypeAnalysis:  testTypeAnalysis,
        RecentResults:     results[max(0, len(results)-10):], // Last 10 results
        QualityMetrics:    metrics.QualityMetrics,
        TimeRange:         timeRange,
        GeneratedAt:       time.Now(),
    }
    
    return dashboard, nil
}

// HTTP API for Test Management

func (tf *TestFramework) RunTestHandler(w http.ResponseWriter, r *http.Request) {
    ctx, span := tf.tracer.Start(r.Context(), "test_framework.run_test_handler")
    defer span.End()
    
    var req RunTestRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }
    
    // Create test job
    job := TestJob{
        ID:           generateJobID(),
        ExampleID:    req.ExampleID,
        Language:     req.Language,
        TestType:     req.TestType,
        Priority:     PriorityHigh, // API requests get high priority
        CreatedAt:    time.Now(),
    }
    
    // Submit to execution queue
    select {
    case tf.executionQueue <- job:
    case <-ctx.Done():
        http.Error(w, "Request timeout", http.StatusRequestTimeout)
        return
    }
    
    // Wait for result or timeout
    resultChan := tf.subscribeToResult(job.ID)
    select {
    case result := <-resultChan:
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(result)
    case <-time.After(time.Minute * 5):
        http.Error(w, "Test execution timeout", http.StatusRequestTimeout)
    case <-ctx.Done():
        http.Error(w, "Request cancelled", http.StatusRequestTimeout)
    }
}

func (tf *TestFramework) GetTestResultsHandler(w http.ResponseWriter, r *http.Request) {
    exampleID := r.URL.Query().Get("example_id")
    limit := 50 // Default limit
    
    results, err := tf.resultStore.GetResultsByExample(exampleID, limit)
    if err != nil {
        http.Error(w, "Failed to fetch results", http.StatusInternalServerError)
        return
    }
    
    response := TestResultsResponse{
        ExampleID: exampleID,
        Results:   results,
        Count:     len(results),
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    config := TestConfig{
        WorkerCount:     10,
        QueueSize:      1000,
        DefaultTimeout: time.Minute * 5,
        Languages: map[string]LanguageConfig{
            "go": {
                Version:     "1.21",
                TestRunner:  "go-test-runner",
                DockerImage: "golang:1.21-alpine",
            },
            "typescript": {
                Version:     "5.0",
                TestRunner:  "typescript-test-runner",
                DockerImage: "node:20-alpine",
            },
            "python": {
                Version:     "3.11",
                TestRunner:  "python-test-runner",
                DockerImage: "python:3.11-alpine",
            },
        },
    }
    
    framework, err := NewTestFramework(config)
    if err != nil {
        log.Fatal("Failed to initialize test framework:", err)
    }
    
    // Start worker pool
    framework.Start()
    defer framework.Stop()
    
    // Setup HTTP routes
    r := mux.NewRouter()
    r.HandleFunc("/test/run", framework.RunTestHandler).Methods("POST")
    r.HandleFunc("/test/results", framework.GetTestResultsHandler).Methods("GET")
    r.HandleFunc("/test/dashboard", framework.GetDashboardHandler).Methods("GET")
    r.HandleFunc("/test/suite/run", framework.RunFullSuiteHandler).Methods("POST")
    r.HandleFunc("/health", healthCheckHandler).Methods("GET")
    
    log.Println("Test framework API starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

## 🎨 **Frontend Testing Dashboard**

### React Testing Interface

```typescript
// testing-dashboard/TestingDashboard.tsx - Comprehensive test monitoring interface
import React, { useState, useEffect, useCallback } from 'react';
import { Play, CheckCircle, XCircle, Clock, AlertTriangle, TrendingUp, Code, Database } from 'lucide-react';

interface TestingDashboardProps {
    className?: string;
}

const TestingDashboard: React.FC<TestingDashboardProps> = ({ className = '' }) => {
    const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
    const [selectedTimeRange, setSelectedTimeRange] = useState<string>('7d');
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState<'overview' | 'results' | 'trends'>('overview');
    
    const fetchDashboardData = useCallback(async (timeRange: string) => {
        setLoading(true);
        
        try {
            const response = await fetch(`/api/test/dashboard?range=${timeRange}`);
            const data: DashboardData = await response.json();
            setDashboardData(data);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
        } finally {
            setLoading(false);
        }
    }, []);
    
    useEffect(() => {
        fetchDashboardData(selectedTimeRange);
        
        // Set up polling for real-time updates
        const interval = setInterval(() => {
            fetchDashboardData(selectedTimeRange);
        }, 30000); // Update every 30 seconds
        
        return () => clearInterval(interval);
    }, [selectedTimeRange, fetchDashboardData]);
    
    const runFullSuite = useCallback(async () => {
        setLoading(true);
        
        try {
            const response = await fetch('/api/test/suite/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    full_suite: true,
                    priority: 'high',
                }),
            });
            
            if (response.ok) {
                // Refresh dashboard after initiating test run
                setTimeout(() => {
                    fetchDashboardData(selectedTimeRange);
                }, 2000);
            }
        } catch (error) {
            console.error('Error running test suite:', error);
        } finally {
            setLoading(false);
        }
    }, [selectedTimeRange, fetchDashboardData]);
    
    if (loading && !dashboardData) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                <span className="ml-3 text-gray-600">Loading test data...</span>
            </div>
        );
    }
    
    return (
        <div className={`testing-dashboard ${className}`}>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                    <Code className="w-8 h-8 mr-3 text-blue-600" />
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Code Testing Dashboard</h2>
                        <p className="text-gray-600">Automated validation of wiki code examples</p>
                    </div>
                </div>
                
                <div className="flex items-center space-x-4">
                    <select
                        value={selectedTimeRange}
                        onChange={(e) => setSelectedTimeRange(e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-md text-sm"
                    >
                        <option value="1d">Last 24 hours</option>
                        <option value="7d">Last 7 days</option>
                        <option value="30d">Last 30 days</option>
                        <option value="90d">Last 90 days</option>
                    </select>
                    
                    <button
                        onClick={runFullSuite}
                        disabled={loading}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
                    >
                        <Play className="w-4 h-4 mr-2" />
                        Run Full Suite
                    </button>
                </div>
            </div>
            
            {/* Overview Cards */}
            {dashboardData && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <OverviewCard
                        title="Total Tests"
                        value={dashboardData.overview.total_tests}
                        icon={<Database className="w-6 h-6" />}
                        color="blue"
                    />
                    
                    <OverviewCard
                        title="Success Rate"
                        value={`${(dashboardData.overview.success_rate * 100).toFixed(1)}%`}
                        icon={<CheckCircle className="w-6 h-6" />}
                        color={dashboardData.overview.success_rate > 0.95 ? "green" : 
                               dashboardData.overview.success_rate > 0.85 ? "yellow" : "red"}
                        trend={dashboardData.overview.trend_direction}
                    />
                    
                    <OverviewCard
                        title="Avg. Execution Time"
                        value={`${dashboardData.overview.average_exec_time.toFixed(2)}s`}
                        icon={<Clock className="w-6 h-6" />}
                        color="purple"
                    />
                    
                    <OverviewCard
                        title="Failed Tests"
                        value={dashboardData.overview.total_tests - Math.round(dashboardData.overview.total_tests * dashboardData.overview.success_rate)}
                        icon={<XCircle className="w-6 h-6" />}
                        color="red"
                    />
                </div>
            )}
            
            {/* Tab Navigation */}
            <div className="flex border-b border-gray-200 mb-6">
                <button
                    onClick={() => setActiveTab('overview')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'overview'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    Overview
                </button>
                
                <button
                    onClick={() => setActiveTab('results')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'results'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    Recent Results
                </button>
                
                <button
                    onClick={() => setActiveTab('trends')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'trends'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    Trends & Analytics
                </button>
            </div>
            
            {/* Tab Content */}
            {dashboardData && (
                <div className="tab-content">
                    {activeTab === 'overview' && (
                        <OverviewTab
                            data={dashboardData}
                            onRefresh={() => fetchDashboardData(selectedTimeRange)}
                        />
                    )}
                    
                    {activeTab === 'results' && (
                        <ResultsTab
                            results={dashboardData.recent_results}
                            onRefresh={() => fetchDashboardData(selectedTimeRange)}
                        />
                    )}
                    
                    {activeTab === 'trends' && (
                        <TrendsTab
                            trendData={dashboardData.trend_data}
                            languageBreakdown={dashboardData.language_breakdown}
                            testTypeAnalysis={dashboardData.test_type_analysis}
                        />
                    )}
                </div>
            )}
        </div>
    );
};

const OverviewCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
    trend?: 'up' | 'down' | 'stable';
}> = ({ title, value, icon, color, trend }) => {
    const colorClasses = {
        blue: 'bg-blue-50 text-blue-700 border-blue-200',
        green: 'bg-green-50 text-green-700 border-green-200',
        yellow: 'bg-yellow-50 text-yellow-700 border-yellow-200',
        red: 'bg-red-50 text-red-700 border-red-200',
        purple: 'bg-purple-50 text-purple-700 border-purple-200',
    };
    
    return (
        <div className={`p-6 rounded-lg border ${colorClasses[color as keyof typeof colorClasses]}`}>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium opacity-75">{title}</p>
                    <p className="text-2xl font-bold">{value}</p>
                </div>
                <div className="opacity-75">
                    {icon}
                </div>
            </div>
            
            {trend && (
                <div className="mt-2 flex items-center text-xs">
                    {trend === 'up' && <TrendingUp className="w-3 h-3 mr-1" />}
                    {trend === 'down' && <TrendingUp className="w-3 h-3 mr-1 rotate-180" />}
                    <span>
                        {trend === 'up' ? 'Improving' : trend === 'down' ? 'Declining' : 'Stable'}
                    </span>
                </div>
            )}
        </div>
    );
};

const OverviewTab: React.FC<{
    data: DashboardData;
    onRefresh: () => void;
}> = ({ data, onRefresh }) => {
    return (
        <div className="overview-tab">
            {/* Language Breakdown */}
            <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Language Distribution</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(data.language_breakdown).map(([language, stats]) => (
                        <div key={language} className="p-4 bg-white border border-gray-200 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-medium text-gray-900 capitalize">
                                    {language}
                                </span>
                                <span className="text-xs text-gray-500">
                                    {stats.total_tests} tests
                                </span>
                            </div>
                            
                            <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: `${(stats.success_rate * 100)}%` }}
                                />
                            </div>
                            
                            <div className="text-xs text-gray-600">
                                {(stats.success_rate * 100).toFixed(1)}% success rate
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            
            {/* Quality Metrics */}
            <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quality Metrics</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <QualityMetricCard
                        title="Code Coverage"
                        value={`${(data.quality_metrics.average_coverage * 100).toFixed(1)}%`}
                        description="Average test coverage across all examples"
                        color="green"
                    />
                    
                    <QualityMetricCard
                        title="Performance Score"
                        value={data.quality_metrics.performance_score.toFixed(1)}
                        description="Average execution performance rating"
                        color="blue"
                    />
                    
                    <QualityMetricCard
                        title="Security Score"
                        value={data.quality_metrics.security_score.toFixed(1)}
                        description="Average security scan rating"
                        color="purple"
                    />
                </div>
            </div>
        </div>
    );
};

const ResultsTab: React.FC<{
    results: TestResult[];
    onRefresh: () => void;
}> = ({ results, onRefresh }) => {
    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'passed':
                return <CheckCircle className="w-5 h-5 text-green-600" />;
            case 'failed':
                return <XCircle className="w-5 h-5 text-red-600" />;
            case 'running':
                return <Clock className="w-5 h-5 text-blue-600" />;
            default:
                return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
        }
    };
    
    return (
        <div className="results-tab">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Example
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Language
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Duration
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Executed
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {results.map((result) => (
                            <tr key={result.job_id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-medium text-gray-900">
                                        {result.example_id}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">
                                        {result.test_details?.language || 'unknown'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        {getStatusIcon(result.status)}
                                        <span className="ml-2 text-sm text-gray-900 capitalize">
                                            {result.status}
                                        </span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {(result.execution_time / 1000000000).toFixed(2)}s
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {new Date(result.end_time).toLocaleString()}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TestingDashboard;
```

## Remember

> *"Welcome to the real world."* - Morpheus

Automated testing isn't just about finding bugs - it's about building trust in the knowledge we share. Every validated code example becomes a reliable guide for others walking the path of understanding. When documentation is tested, uncertainty transforms into confidence.

The most powerful testing systems don't just check if code works - they ensure that learning remains unbroken, that each example teaches correctly, and that knowledge stays current as technology evolves.

**Test with purpose. Validate with confidence. Build the reliable Matrix of knowledge.**

---

**Guide Status**: 🟢 COMPREHENSIVE TESTING SYSTEM  
**Validation Coverage**: 🧪 CONTINUOUS VERIFICATION  
**Liberation Impact**: ⭐⭐⭐⭐⭐  

*In testing we find reliability. In automation we find consistency. In continuous validation we find the truly trustworthy Matrix of knowledge.*

---

[← Development Hub](index.md) | [← Cross-Reference Linking](cross-reference-linking-guide.md) | [→ Development Hub](index.md)