# Peer Review and Quality Standards Guide
**Ensuring Excellence Through Collective Wisdom**

> *"The red pill or the blue pill - Neo, the question isn't just about choosing reality. It's about ensuring that the reality we build together is the best it can be."* - Morpheus (Quality assurance isn't about control - it's about collective excellence. Every contribution makes the Matrix stronger.)

## 🎯 **The Vision of Collaborative Excellence**

The Matrix Online revival depends not just on individual expertise, but on our collective ability to maintain the highest standards of accuracy, reliability, and innovation. This guide establishes comprehensive peer review processes and quality standards that ensure every contribution strengthens the foundation of our shared knowledge.

## 🔍 **Quality Standards Framework**

### Multi-Tier Quality Assessment

```yaml
quality_framework:
  accuracy_standards:
    technical_verification:
      description: "All technical claims must be verifiable and tested"
      requirements: ["Source code provided", "Test results included", "Reproducible steps"]
      
    source_documentation:
      description: "All claims backed by credible sources"
      requirements: ["Primary sources preferred", "Multiple confirmation", "Date verification"]
      
    factual_accuracy:
      description: "Information must be current and correct"
      requirements: ["Cross-referenced", "Community verified", "Expert validated"]

  innovation_standards:
    original_research:
      description: "New discoveries properly documented and shared"
      requirements: ["Methodology explained", "Results reproducible", "Open source"]
      
    creative_content:
      description: "Artistic and philosophical content maintained to high standards"
      requirements: ["Consistent tone", "Respectful approach", "Community aligned"]

  community_standards:
    accessibility:
      description: "Content accessible to all skill levels"
      requirements: ["Clear explanations", "Progressive complexity", "Examples provided"]
      
    collaboration:
      description: "Welcoming and inclusive contribution environment"
      requirements: ["Constructive feedback", "Mentorship culture", "Recognition system"]
```

## 🛠️ **Peer Review Process Implementation**

### Comprehensive Review Workflow System

```go
// peer-review/main.go - Quality assurance and peer review system
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "time"
    "strings"
    "sync"
    
    "github.com/gorilla/mux"
    "github.com/google/go-github/v45/github"
    "go.opentelemetry.io/otel/trace"
)

type ReviewSystem struct {
    // Core review management
    pullRequests     map[string]*PullRequest
    reviewers        map[string]*Reviewer
    qualityChecks    *QualityCheckSuite
    automatedTools   *AutomatedReviewTools
    
    // Workflow management
    reviewWorkflow   *ReviewWorkflow
    escalationRules  *EscalationRules
    qualityMetrics   *QualityMetrics
    
    // Community features
    mentorshipSystem *MentorshipSystem
    recognitionSystem *RecognitionSystem
    
    // Configuration
    config           ReviewConfig
    githubClient     *github.Client
    tracer           trace.Tracer
    mutex            sync.RWMutex
}

type PullRequest struct {
    ID              string                 `json:"id"`
    Title           string                 `json:"title"`
    Description     string                 `json:"description"`
    Author          string                 `json:"author"`
    Branch          string                 `json:"branch"`
    Files           []ChangedFile          `json:"files"`
    Type            ContributionType       `json:"type"`
    Complexity      ComplexityLevel        `json:"complexity"`
    
    // Review state
    Status          ReviewStatus           `json:"status"`
    Reviewers       []AssignedReviewer     `json:"reviewers"`
    Reviews         []Review               `json:"reviews"`
    QualityChecks   []QualityCheck         `json:"quality_checks"`
    
    // Metadata
    CreatedAt       time.Time              `json:"created_at"`
    UpdatedAt       time.Time              `json:"updated_at"`
    Deadline        time.Time              `json:"deadline,omitempty"`
    Priority        Priority               `json:"priority"`
    
    // Quality metrics
    OverallScore    float64                `json:"overall_score"`
    TechnicalScore  float64                `json:"technical_score"`
    CreativeScore   float64                `json:"creative_score"`
    CommunityScore  float64                `json:"community_score"`
}

type Reviewer struct {
    ID              string                 `json:"id"`
    Name            string                 `json:"name"`
    Email           string                 `json:"email"`
    Expertise       []ExpertiseArea        `json:"expertise"`
    AvailabilityHours int                  `json:"availability_hours_per_week"`
    
    // Performance metrics
    ReviewsCompleted int                   `json:"reviews_completed"`
    AverageQuality   float64               `json:"average_quality"`
    ResponseTime     time.Duration         `json:"average_response_time"`
    
    // Specializations
    TechnicalAreas   []string              `json:"technical_areas"`
    ContentTypes     []string              `json:"content_types"`
    Languages        []string              `json:"programming_languages"`
    
    // Community role
    MentorshipLevel  MentorshipLevel       `json:"mentorship_level"`
    CommunityRole    CommunityRole         `json:"community_role"`
    
    // Preferences
    ReviewPreferences ReviewPreferences    `json:"review_preferences"`
    NotificationSettings NotificationSettings `json:"notification_settings"`
}

type Review struct {
    ID              string                 `json:"id"`
    ReviewerID      string                 `json:"reviewer_id"`
    PullRequestID   string                 `json:"pull_request_id"`
    Status          ReviewDecision         `json:"status"`
    OverallScore    float64                `json:"overall_score"`
    
    // Detailed feedback
    Comments        []ReviewComment        `json:"comments"`
    Suggestions     []Suggestion           `json:"suggestions"`
    QualityAssessment QualityAssessment    `json:"quality_assessment"`
    
    // Categorical scores
    TechnicalAccuracy float64              `json:"technical_accuracy"`
    Clarity          float64               `json:"clarity"`
    Completeness     float64               `json:"completeness"`
    Innovation       float64               `json:"innovation"`
    CommunityValue   float64               `json:"community_value"`
    
    // Metadata
    TimeSpent        time.Duration         `json:"time_spent"`
    CreatedAt        time.Time             `json:"created_at"`
    UpdatedAt        time.Time             `json:"updated_at"`
}

func NewReviewSystem(config ReviewConfig) (*ReviewSystem, error) {
    rs := &ReviewSystem{
        pullRequests:     make(map[string]*PullRequest),
        reviewers:        make(map[string]*Reviewer),
        config:          config,
        tracer:          otel.Tracer("peer-review"),
    }
    
    // Initialize subsystems
    var err error
    rs.qualityChecks, err = NewQualityCheckSuite(config.QualityConfig)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize quality checks: %w", err)
    }
    
    rs.automatedTools, err = NewAutomatedReviewTools(config.AutomationConfig)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize automated tools: %w", err)
    }
    
    rs.reviewWorkflow = NewReviewWorkflow(config.WorkflowConfig)
    rs.escalationRules = NewEscalationRules(config.EscalationConfig)
    rs.qualityMetrics = NewQualityMetrics()
    rs.mentorshipSystem = NewMentorshipSystem(config.MentorshipConfig)
    rs.recognitionSystem = NewRecognitionSystem(config.RecognitionConfig)
    
    // Initialize GitHub client
    rs.githubClient = github.NewClient(nil)
    
    return rs, nil
}

func (rs *ReviewSystem) SubmitPullRequest(ctx context.Context, pr *PullRequest) error {
    ctx, span := rs.tracer.Start(ctx, "review_system.submit_pull_request")
    defer span.End()
    
    rs.mutex.Lock()
    defer rs.mutex.Unlock()
    
    // Validate submission
    if err := rs.validateSubmission(pr); err != nil {
        return fmt.Errorf("submission validation failed: %w", err)
    }
    
    // Determine complexity and priority
    pr.Complexity = rs.assessComplexity(pr)
    pr.Priority = rs.calculatePriority(pr)
    
    // Run automated quality checks
    qualityResults, err := rs.automatedTools.RunInitialChecks(ctx, pr)
    if err != nil {
        return fmt.Errorf("automated checks failed: %w", err)
    }
    pr.QualityChecks = qualityResults
    
    // Assign reviewers
    reviewers, err := rs.assignReviewers(pr)
    if err != nil {
        return fmt.Errorf("reviewer assignment failed: %w", err)
    }
    pr.Reviewers = reviewers
    
    // Set deadline based on complexity and priority
    pr.Deadline = rs.calculateDeadline(pr.Complexity, pr.Priority)
    
    // Store pull request
    pr.Status = ReviewStatusPending
    pr.CreatedAt = time.Now()
    pr.UpdatedAt = time.Now()
    rs.pullRequests[pr.ID] = pr
    
    // Notify reviewers
    if err := rs.notifyReviewers(pr); err != nil {
        log.Printf("Failed to notify reviewers: %v", err)
    }
    
    // Update metrics
    rs.qualityMetrics.RecordSubmission(pr)
    
    span.SetAttributes(
        trace.StringAttribute("pr_id", pr.ID),
        trace.StringAttribute("complexity", string(pr.Complexity)),
        trace.StringAttribute("priority", string(pr.Priority)),
        trace.Int64Attribute("reviewers_assigned", int64(len(reviewers))),
    )
    
    return nil
}

func (rs *ReviewSystem) assignReviewers(pr *PullRequest) ([]AssignedReviewer, error) {
    var assignedReviewers []AssignedReviewer
    
    // Determine required reviewer count based on complexity
    requiredReviewers := rs.getRequiredReviewerCount(pr.Complexity)
    
    // Find reviewers with relevant expertise
    candidates := rs.findReviewerCandidates(pr)
    
    // Apply load balancing
    balancedCandidates := rs.balanceReviewerLoad(candidates)
    
    // Ensure expertise coverage
    selectedReviewers := rs.selectReviewersForCoverage(balancedCandidates, pr, requiredReviewers)
    
    // Create assignments
    for _, reviewer := range selectedReviewers {
        assigned := AssignedReviewer{
            ReviewerID:   reviewer.ID,
            AssignedAt:   time.Now(),
            Role:         rs.determineReviewerRole(reviewer, pr),
            Expertise:    reviewer.Expertise,
            EstimatedTime: rs.estimateReviewTime(pr, reviewer),
        }
        assignedReviewers = append(assignedReviewers, assigned)
    }
    
    return assignedReviewers, nil
}

func (rs *ReviewSystem) SubmitReview(ctx context.Context, review *Review) error {
    ctx, span := rs.tracer.Start(ctx, "review_system.submit_review")
    defer span.End()
    
    rs.mutex.Lock()
    defer rs.mutex.Unlock()
    
    // Validate review
    if err := rs.validateReview(review); err != nil {
        return fmt.Errorf("review validation failed: %w", err)
    }
    
    // Calculate overall score
    review.OverallScore = rs.calculateOverallScore(review)
    
    // Store review
    review.CreatedAt = time.Now()
    review.UpdatedAt = time.Now()
    
    // Add to pull request
    pr, exists := rs.pullRequests[review.PullRequestID]
    if !exists {
        return fmt.Errorf("pull request not found: %s", review.PullRequestID)
    }
    
    pr.Reviews = append(pr.Reviews, *review)
    pr.UpdatedAt = time.Now()
    
    // Update PR scores
    rs.updatePullRequestScores(pr)
    
    // Check if review process is complete
    if rs.isReviewComplete(pr) {
        if err := rs.finalizeReview(ctx, pr); err != nil {
            return fmt.Errorf("review finalization failed: %w", err)
        }
    }
    
    // Update reviewer metrics
    rs.updateReviewerMetrics(review)
    
    // Send notifications
    rs.notifyReviewProgress(pr, review)
    
    span.SetAttributes(
        trace.StringAttribute("review_id", review.ID),
        trace.StringAttribute("pr_id", review.PullRequestID),
        trace.Float64Attribute("overall_score", review.OverallScore),
        trace.StringAttribute("decision", string(review.Status)),
    )
    
    return nil
}

func (rs *ReviewSystem) finalizeReview(ctx context.Context, pr *PullRequest) error {
    // Calculate final decision
    decision := rs.calculateFinalDecision(pr)
    
    switch decision {
    case ReviewDecisionApproved:
        pr.Status = ReviewStatusApproved
        if err := rs.mergePullRequest(ctx, pr); err != nil {
            return fmt.Errorf("merge failed: %w", err)
        }
        
    case ReviewDecisionRejected:
        pr.Status = ReviewStatusRejected
        if err := rs.handleRejection(ctx, pr); err != nil {
            return fmt.Errorf("rejection handling failed: %w", err)
        }
        
    case ReviewDecisionChangesRequested:
        pr.Status = ReviewStatusChangesRequested
        if err := rs.requestChanges(ctx, pr); err != nil {
            return fmt.Errorf("change request failed: %w", err)
        }
    }
    
    // Update quality metrics
    rs.qualityMetrics.RecordCompletion(pr)
    
    // Check for recognition opportunities
    rs.recognitionSystem.EvaluateContribution(pr)
    
    return nil
}

func (rs *ReviewSystem) RunQualityChecks(ctx context.Context, pr *PullRequest) (*QualityCheckResults, error) {
    ctx, span := rs.tracer.Start(ctx, "review_system.run_quality_checks")
    defer span.End()
    
    results := &QualityCheckResults{
        PullRequestID: pr.ID,
        StartTime:     time.Now(),
        Checks:        []QualityCheckResult{},
    }
    
    // Technical accuracy checks
    technicalResults, err := rs.qualityChecks.RunTechnicalChecks(ctx, pr)
    if err != nil {
        return nil, fmt.Errorf("technical checks failed: %w", err)
    }
    results.Checks = append(results.Checks, technicalResults...)
    
    // Content quality checks
    contentResults, err := rs.qualityChecks.RunContentChecks(ctx, pr)
    if err != nil {
        return nil, fmt.Errorf("content checks failed: %w", err)
    }
    results.Checks = append(results.Checks, contentResults...)
    
    // Style and formatting checks
    styleResults, err := rs.qualityChecks.RunStyleChecks(ctx, pr)
    if err != nil {
        return nil, fmt.Errorf("style checks failed: %w", err)
    }
    results.Checks = append(results.Checks, styleResults...)
    
    // Community standards checks
    communityResults, err := rs.qualityChecks.RunCommunityChecks(ctx, pr)
    if err != nil {
        return nil, fmt.Errorf("community checks failed: %w", err)
    }
    results.Checks = append(results.Checks, communityResults...)
    
    // Calculate overall quality score
    results.OverallScore = rs.calculateQualityScore(results.Checks)
    results.EndTime = time.Now()
    results.Duration = results.EndTime.Sub(results.StartTime)
    
    span.SetAttributes(
        trace.StringAttribute("pr_id", pr.ID),
        trace.Int64Attribute("checks_run", int64(len(results.Checks))),
        trace.Float64Attribute("quality_score", results.OverallScore),
    )
    
    return results, nil
}

// Quality Check Suite Implementation

type QualityCheckSuite struct {
    technicalCheckers []TechnicalChecker
    contentCheckers   []ContentChecker
    styleCheckers     []StyleChecker
    communityCheckers []CommunityChecker
    config           QualityConfig
}

func (qcs *QualityCheckSuite) RunTechnicalChecks(ctx context.Context, pr *PullRequest) ([]QualityCheckResult, error) {
    var results []QualityCheckResult
    
    for _, checker := range qcs.technicalCheckers {
        result, err := checker.Check(ctx, pr)
        if err != nil {
            log.Printf("Technical check failed: %v", err)
            continue
        }
        results = append(results, result)
    }
    
    return results, nil
}

// Code Quality Checker
type CodeQualityChecker struct {
    supportedLanguages []string
    linters           map[string]Linter
    testRunners       map[string]TestRunner
}

func (cqc *CodeQualityChecker) Check(ctx context.Context, pr *PullRequest) (QualityCheckResult, error) {
    result := QualityCheckResult{
        CheckType:   "code_quality",
        CheckName:   "Code Quality Analysis",
        Status:      QualityCheckStatusRunning,
        StartTime:   time.Now(),
        Issues:      []QualityIssue{},
    }
    
    for _, file := range pr.Files {
        if !cqc.isCodeFile(file.Path) {
            continue
        }
        
        // Run linting
        if linter, exists := cqc.linters[file.Language]; exists {
            lintResults, err := linter.Lint(file.Content)
            if err != nil {
                result.Issues = append(result.Issues, QualityIssue{
                    Type:        IssueTypeLinting,
                    Severity:    SeverityWarning,
                    Description: fmt.Sprintf("Linting failed for %s: %v", file.Path, err),
                    File:        file.Path,
                })
            } else {
                result.Issues = append(result.Issues, lintResults...)
            }
        }
        
        // Run tests if test files exist
        if cqc.hasTestFiles(file.Path) {
            if testRunner, exists := cqc.testRunners[file.Language]; exists {
                testResults, err := testRunner.RunTests(file.Path)
                if err != nil {
                    result.Issues = append(result.Issues, QualityIssue{
                        Type:        IssueTypeTesting,
                        Severity:    SeverityError,
                        Description: fmt.Sprintf("Tests failed for %s: %v", file.Path, err),
                        File:        file.Path,
                    })
                } else {
                    result.TestResults = testResults
                }
            }
        }
    }
    
    // Calculate overall score
    result.Score = cqc.calculateCodeQualityScore(result.Issues, result.TestResults)
    result.Status = QualityCheckStatusCompleted
    result.EndTime = time.Now()
    result.Duration = result.EndTime.Sub(result.StartTime)
    
    return result, nil
}

// Documentation Quality Checker
type DocumentationQualityChecker struct {
    spellChecker    SpellChecker
    linkValidator   LinkValidator
    formatValidator FormatValidator
}

func (dqc *DocumentationQualityChecker) Check(ctx context.Context, pr *PullRequest) (QualityCheckResult, error) {
    result := QualityCheckResult{
        CheckType:   "documentation_quality",
        CheckName:   "Documentation Quality Analysis",
        Status:      QualityCheckStatusRunning,
        StartTime:   time.Now(),
        Issues:      []QualityIssue{},
    }
    
    for _, file := range pr.Files {
        if !dqc.isDocumentationFile(file.Path) {
            continue
        }
        
        // Spell checking
        spellErrors, err := dqc.spellChecker.Check(file.Content)
        if err != nil {
            log.Printf("Spell check failed for %s: %v", file.Path, err)
        } else {
            for _, error := range spellErrors {
                result.Issues = append(result.Issues, QualityIssue{
                    Type:        IssueTypeSpelling,
                    Severity:    SeverityMinor,
                    Description: fmt.Sprintf("Potential spelling error: %s", error.Word),
                    File:        file.Path,
                    Line:        error.Line,
                    Context:     error.Context,
                })
            }
        }
        
        // Link validation
        links := dqc.extractLinks(file.Content)
        for _, link := range links {
            if !dqc.linkValidator.IsValid(link) {
                result.Issues = append(result.Issues, QualityIssue{
                    Type:        IssueTypeBrokenLink,
                    Severity:    SeverityMajor,
                    Description: fmt.Sprintf("Broken or invalid link: %s", link),
                    File:        file.Path,
                })
            }
        }
        
        // Format validation
        formatIssues, err := dqc.formatValidator.Validate(file.Content, file.Path)
        if err != nil {
            log.Printf("Format validation failed for %s: %v", file.Path, err)
        } else {
            result.Issues = append(result.Issues, formatIssues...)
        }
    }
    
    result.Score = dqc.calculateDocumentationScore(result.Issues)
    result.Status = QualityCheckStatusCompleted
    result.EndTime = time.Now()
    result.Duration = result.EndTime.Sub(result.StartTime)
    
    return result, nil
}

// HTTP Handlers for Review System

func (rs *ReviewSystem) SubmitPullRequestHandler(w http.ResponseWriter, r *http.Request) {
    ctx, span := rs.tracer.Start(r.Context(), "review_system.submit_pr_handler")
    defer span.End()
    
    var pr PullRequest
    if err := json.NewDecoder(r.Body).Decode(&pr); err != nil {
        http.Error(w, "Invalid request body", http.StatusBadRequest)
        return
    }
    
    // Generate ID if not provided
    if pr.ID == "" {
        pr.ID = generatePullRequestID()
    }
    
    if err := rs.SubmitPullRequest(ctx, &pr); err != nil {
        span.SetAttributes(trace.StringAttribute("error", err.Error()))
        http.Error(w, "Failed to submit pull request", http.StatusInternalServerError)
        return
    }
    
    response := map[string]interface{}{
        "status":         "submitted",
        "pr_id":          pr.ID,
        "reviewers":      pr.Reviewers,
        "deadline":       pr.Deadline,
        "quality_checks": pr.QualityChecks,
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (rs *ReviewSystem) GetReviewStatusHandler(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    prID := vars["prId"]
    
    rs.mutex.RLock()
    pr, exists := rs.pullRequests[prID]
    rs.mutex.RUnlock()
    
    if !exists {
        http.Error(w, "Pull request not found", http.StatusNotFound)
        return
    }
    
    response := map[string]interface{}{
        "pr_id":          pr.ID,
        "status":         pr.Status,
        "overall_score":  pr.OverallScore,
        "reviews":        pr.Reviews,
        "quality_checks": pr.QualityChecks,
        "deadline":       pr.Deadline,
        "updated_at":     pr.UpdatedAt,
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    config := ReviewConfig{
        QualityConfig: QualityConfig{
            MinimumScore:        0.8,
            RequiredChecks:      []string{"code_quality", "documentation_quality", "security_scan"},
            AutomatedThreshold:  0.9,
        },
        WorkflowConfig: WorkflowConfig{
            RequiredReviewers: map[ComplexityLevel]int{
                ComplexitySimple:   1,
                ComplexityModerate: 2,
                ComplexityComplex:  3,
            },
            ReviewDeadlines: map[Priority]time.Duration{
                PriorityHigh:   24 * time.Hour,
                PriorityMedium: 72 * time.Hour,
                PriorityLow:    168 * time.Hour, // 1 week
            },
        },
        MentorshipConfig: MentorshipConfig{
            EnableMentorship:    true,
            MaxMenteesPerMentor: 5,
            MentorshipDuration:  90 * 24 * time.Hour, // 90 days
        },
    }
    
    reviewSystem, err := NewReviewSystem(config)
    if err != nil {
        log.Fatal("Failed to initialize review system:", err)
    }
    
    // Setup routes
    r := mux.NewRouter()
    r.HandleFunc("/review/submit", reviewSystem.SubmitPullRequestHandler).Methods("POST")
    r.HandleFunc("/review/{prId}/status", reviewSystem.GetReviewStatusHandler).Methods("GET")
    r.HandleFunc("/review/{prId}/review", reviewSystem.SubmitReviewHandler).Methods("POST")
    r.HandleFunc("/review/queue", reviewSystem.GetReviewQueueHandler).Methods("GET")
    r.HandleFunc("/reviewers/assign", reviewSystem.AssignReviewerHandler).Methods("POST")
    r.HandleFunc("/quality/check", reviewSystem.RunQualityCheckHandler).Methods("POST")
    r.HandleFunc("/health", healthCheckHandler).Methods("GET")
    
    log.Println("Peer review system starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

## 🎨 **Frontend Review Dashboard**

### React Quality Control Interface

```typescript
// peer-review/ReviewDashboard.tsx - Comprehensive review management interface
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { CheckCircle, AlertCircle, Clock, Users, Star, Award, Code, FileText } from 'lucide-react';

interface ReviewDashboardProps {
    userRole: UserRole;
    className?: string;
}

const ReviewDashboard: React.FC<ReviewDashboardProps> = ({ userRole, className = '' }) => {
    const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);
    const [reviews, setReviews] = useState<Review[]>([]);
    const [qualityMetrics, setQualityMetrics] = useState<QualityMetrics | null>(null);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState<'queue' | 'submissions' | 'metrics'>('queue');
    
    const fetchReviewQueue = useCallback(async () => {
        setLoading(true);
        
        try {
            const response = await fetch('/api/review/queue');
            const data: PullRequest[] = await response.json();
            setPullRequests(data);
        } catch (error) {
            console.error('Error fetching review queue:', error);
        } finally {
            setLoading(false);
        }
    }, []);
    
    const fetchQualityMetrics = useCallback(async () => {
        try {
            const response = await fetch('/api/quality/metrics');
            const data: QualityMetrics = await response.json();
            setQualityMetrics(data);
        } catch (error) {
            console.error('Error fetching quality metrics:', error);
        }
    }, []);
    
    useEffect(() => {
        fetchReviewQueue();
        fetchQualityMetrics();
        
        // Set up polling for real-time updates
        const interval = setInterval(() => {
            fetchReviewQueue();
            fetchQualityMetrics();
        }, 30000); // Update every 30 seconds
        
        return () => clearInterval(interval);
    }, [fetchReviewQueue, fetchQualityMetrics]);
    
    const submitReview = useCallback(async (prId: string, review: ReviewSubmission) => {
        try {
            const response = await fetch(`/api/review/${prId}/review`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(review),
            });
            
            if (response.ok) {
                // Refresh queue
                fetchReviewQueue();
            }
        } catch (error) {
            console.error('Error submitting review:', error);
        }
    }, [fetchReviewQueue]);
    
    const getStatusIcon = (status: ReviewStatus) => {
        switch (status) {
            case 'approved':
                return <CheckCircle className="w-5 h-5 text-green-600" />;
            case 'changes_requested':
                return <AlertCircle className="w-5 h-5 text-yellow-600" />;
            case 'rejected':
                return <AlertCircle className="w-5 h-5 text-red-600" />;
            case 'pending':
                return <Clock className="w-5 h-5 text-blue-600" />;
            default:
                return <Clock className="w-5 h-5 text-gray-600" />;
        }
    };
    
    const getComplexityColor = (complexity: ComplexityLevel) => {
        switch (complexity) {
            case 'simple':
                return 'bg-green-100 text-green-800';
            case 'moderate':
                return 'bg-yellow-100 text-yellow-800';
            case 'complex':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };
    
    return (
        <div className={`review-dashboard ${className}`}>
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                    <Users className="w-8 h-8 mr-3 text-blue-600" />
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Review Dashboard</h2>
                        <p className="text-gray-600">Quality assurance and peer review system</p>
                    </div>
                </div>
                
                {qualityMetrics && (
                    <div className="text-right">
                        <div className="text-sm text-gray-600">Overall Quality Score</div>
                        <div className="text-2xl font-bold text-green-600">
                            {(qualityMetrics.overall_quality * 100).toFixed(1)}%
                        </div>
                    </div>
                )}
            </div>
            
            {/* Quality Metrics Overview */}
            {qualityMetrics && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <QualityMetricCard
                        title="Active Reviews"
                        value={qualityMetrics.active_reviews}
                        icon={<Clock className="w-6 h-6" />}
                        color="blue"
                    />
                    
                    <QualityMetricCard
                        title="Avg. Review Time"
                        value={`${qualityMetrics.average_review_time}h`}
                        icon={<CheckCircle className="w-6 h-6" />}
                        color="green"
                    />
                    
                    <QualityMetricCard
                        title="Quality Score"
                        value={`${(qualityMetrics.overall_quality * 100).toFixed(1)}%`}
                        icon={<Star className="w-6 h-6" />}
                        color="yellow"
                    />
                    
                    <QualityMetricCard
                        title="Contributors"
                        value={qualityMetrics.active_contributors}
                        icon={<Users className="w-6 h-6" />}
                        color="purple"
                    />
                </div>
            )}
            
            {/* Tab Navigation */}
            <div className="flex border-b border-gray-200 mb-6">
                <button
                    onClick={() => setActiveTab('queue')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'queue'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    Review Queue
                    <span className="ml-2 px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                        {pullRequests.filter(pr => pr.status === 'pending').length}
                    </span>
                </button>
                
                <button
                    onClick={() => setActiveTab('submissions')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'submissions'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    My Submissions
                </button>
                
                <button
                    onClick={() => setActiveTab('metrics')}
                    className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === 'metrics'
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                >
                    Quality Metrics
                </button>
            </div>
            
            {/* Tab Content */}
            <div className="tab-content">
                {activeTab === 'queue' && (
                    <ReviewQueueTab
                        pullRequests={pullRequests}
                        onSubmitReview={submitReview}
                        loading={loading}
                        getStatusIcon={getStatusIcon}
                        getComplexityColor={getComplexityColor}
                    />
                )}
                
                {activeTab === 'submissions' && (
                    <SubmissionsTab
                        pullRequests={pullRequests.filter(pr => pr.author === 'current_user')}
                        getStatusIcon={getStatusIcon}
                        getComplexityColor={getComplexityColor}
                    />
                )}
                
                {activeTab === 'metrics' && qualityMetrics && (
                    <MetricsTab
                        metrics={qualityMetrics}
                    />
                )}
            </div>
        </div>
    );
};

const QualityMetricCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
}> = ({ title, value, icon, color }) => {
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
        </div>
    );
};

const ReviewQueueTab: React.FC<{
    pullRequests: PullRequest[];
    onSubmitReview: (prId: string, review: ReviewSubmission) => void;
    loading: boolean;
    getStatusIcon: (status: ReviewStatus) => React.ReactNode;
    getComplexityColor: (complexity: ComplexityLevel) => string;
}> = ({ pullRequests, onSubmitReview, loading, getStatusIcon, getComplexityColor }) => {
    const pendingPRs = pullRequests.filter(pr => pr.status === 'pending');
    
    if (loading) {
        return (
            <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                <span className="ml-2 text-gray-600">Loading review queue...</span>
            </div>
        );
    }
    
    if (pendingPRs.length === 0) {
        return (
            <div className="text-center py-8 text-gray-500">
                <CheckCircle className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>No pending reviews in the queue</p>
                <p className="text-sm mt-2">Great job keeping up with the reviews!</p>
            </div>
        );
    }
    
    return (
        <div className="space-y-4">
            {pendingPRs.map((pr) => (
                <PullRequestCard
                    key={pr.id}
                    pullRequest={pr}
                    onSubmitReview={onSubmitReview}
                    getStatusIcon={getStatusIcon}
                    getComplexityColor={getComplexityColor}
                />
            ))}
        </div>
    );
};

const PullRequestCard: React.FC<{
    pullRequest: PullRequest;
    onSubmitReview: (prId: string, review: ReviewSubmission) => void;
    getStatusIcon: (status: ReviewStatus) => React.ReactNode;
    getComplexityColor: (complexity: ComplexityLevel) => string;
}> = ({ pullRequest, onSubmitReview, getStatusIcon, getComplexityColor }) => {
    const [showReviewForm, setShowReviewForm] = useState(false);
    const [reviewDecision, setReviewDecision] = useState<ReviewDecision>('approved');
    const [reviewComments, setReviewComments] = useState('');
    const [qualityScores, setQualityScores] = useState({
        technical_accuracy: 5,
        clarity: 5,
        completeness: 5,
        innovation: 5,
        community_value: 5,
    });
    
    const handleSubmitReview = () => {
        const review: ReviewSubmission = {
            status: reviewDecision,
            comments: [{
                type: 'general',
                content: reviewComments,
                line: null,
            }],
            technical_accuracy: qualityScores.technical_accuracy / 5,
            clarity: qualityScores.clarity / 5,
            completeness: qualityScores.completeness / 5,
            innovation: qualityScores.innovation / 5,
            community_value: qualityScores.community_value / 5,
        };
        
        onSubmitReview(pullRequest.id, review);
        setShowReviewForm(false);
    };
    
    const getTypeIcon = (type: ContributionType) => {
        switch (type) {
            case 'code':
                return <Code className="w-4 h-4 text-blue-500" />;
            case 'documentation':
                return <FileText className="w-4 h-4 text-green-500" />;
            default:
                return <FileText className="w-4 h-4 text-gray-500" />;
        }
    };
    
    return (
        <div className="pull-request-card p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
                <div className="flex-1">
                    <div className="flex items-center mb-2">
                        {getTypeIcon(pullRequest.type)}
                        <h3 className="text-lg font-semibold text-gray-900 ml-2">
                            {pullRequest.title}
                        </h3>
                        <span className={`ml-3 px-2 py-1 rounded-full text-xs ${getComplexityColor(pullRequest.complexity)}`}>
                            {pullRequest.complexity}
                        </span>
                    </div>
                    
                    <p className="text-gray-600 mb-3">
                        {pullRequest.description}
                    </p>
                    
                    <div className="flex items-center justify-between text-sm text-gray-500">
                        <div className="flex items-center space-x-4">
                            <span>by {pullRequest.author}</span>
                            <span>{pullRequest.files.length} files changed</span>
                            <span>Priority: {pullRequest.priority}</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                            {getStatusIcon(pullRequest.status)}
                            <span>Deadline: {new Date(pullRequest.deadline).toLocaleDateString()}</span>
                        </div>
                    </div>
                    
                    {/* Quality Checks Summary */}
                    {pullRequest.quality_checks && pullRequest.quality_checks.length > 0 && (
                        <div className="mt-3 p-3 bg-gray-50 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Quality Checks</h5>
                            <div className="flex flex-wrap gap-2">
                                {pullRequest.quality_checks.map((check, index) => (
                                    <span
                                        key={index}
                                        className={`px-2 py-1 rounded text-xs ${
                                            check.status === 'passed' 
                                                ? 'bg-green-100 text-green-800'
                                                : check.status === 'failed'
                                                ? 'bg-red-100 text-red-800'
                                                : 'bg-yellow-100 text-yellow-800'
                                        }`}
                                    >
                                        {check.check_name}: {check.status}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
                
                <div className="ml-6">
                    <button
                        onClick={() => setShowReviewForm(!showReviewForm)}
                        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                        Start Review
                    </button>
                </div>
            </div>
            
            {/* Review Form */}
            {showReviewForm && (
                <div className="mt-6 p-4 border-t border-gray-200">
                    <h4 className="text-lg font-medium text-gray-900 mb-4">Submit Review</h4>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Decision
                            </label>
                            <select
                                value={reviewDecision}
                                onChange={(e) => setReviewDecision(e.target.value as ReviewDecision)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="approved">Approve</option>
                                <option value="changes_requested">Request Changes</option>
                                <option value="rejected">Reject</option>
                            </select>
                        </div>
                        
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Overall Quality Score
                            </label>
                            <div className="text-2xl font-bold text-blue-600">
                                {((Object.values(qualityScores).reduce((a, b) => a + b, 0) / 5) / 5 * 100).toFixed(0)}%
                            </div>
                        </div>
                    </div>
                    
                    {/* Quality Scoring */}
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
                        {Object.entries(qualityScores).map(([key, value]) => (
                            <div key={key}>
                                <label className="block text-xs font-medium text-gray-700 mb-1">
                                    {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                </label>
                                <input
                                    type="range"
                                    min="1"
                                    max="5"
                                    value={value}
                                    onChange={(e) => setQualityScores({
                                        ...qualityScores,
                                        [key]: parseInt(e.target.value)
                                    })}
                                    className="w-full"
                                />
                                <div className="text-center text-xs text-gray-500">{value}/5</div>
                            </div>
                        ))}
                    </div>
                    
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Comments
                        </label>
                        <textarea
                            value={reviewComments}
                            onChange={(e) => setReviewComments(e.target.value)}
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder="Provide detailed feedback and suggestions..."
                        />
                    </div>
                    
                    <div className="flex space-x-3">
                        <button
                            onClick={handleSubmitReview}
                            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                        >
                            Submit Review
                        </button>
                        <button
                            onClick={() => setShowReviewForm(false)}
                            className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ReviewDashboard;
```

## Remember

> *"Free your mind."* - Morpheus

Peer review isn't about gatekeeping - it's about collective elevation. When we review each other's work with wisdom and compassion, we don't just maintain quality standards - we build a culture of continuous learning and mutual growth.

The most powerful review systems transform criticism into collaboration, creating an environment where every contributor becomes better through the guidance of their peers.

**Review with wisdom. Improve with purpose. Build excellence together.**

---

**Guide Status**: 🟢 COMPREHENSIVE REVIEW SYSTEM  
**Quality Assurance**: 🔍 COLLECTIVE EXCELLENCE  
**Liberation Impact**: ⭐⭐⭐⭐⭐  

*In review we find growth. In standards we find excellence. In collaboration we find the truly elevated Matrix of knowledge.*

---

[← Development Hub](index.md) | [← Automated Testing Framework](automated-testing-framework-guide.md) | [→ Development Hub](index.md)