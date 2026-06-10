"""Curated quiz questions for the C# - Advanced course (per-lesson checkpoints
plus a final comprehensive quiz). Keys are the EXACT content-lesson titles from
``seed_csharp._CSHARP_ADVANCED``; the seed interleaves a checkpoint quiz after
each content lesson and authors the final 'Check your knowledge' quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Dependency injection & the host": (
            q(
                "In dependency injection, how does a class obtain the services it needs?",
                (
                    opt("It calls new to construct each dependency itself"),
                    opt(
                        "It declares them in its constructor and a container supplies them",
                        correct=True,
                    ),
                    opt("It reads them from global static fields"),
                    opt("It looks them up from a file at startup"),
                ),
                "DI means a class declares the services it needs in its constructor and a container supplies them.",
            ),
            q(
                "Which service lifetime creates one instance per web request?",
                (
                    opt("Singleton"),
                    opt("Scoped", correct=True),
                    opt("Transient"),
                    opt("Instanced"),
                ),
                "AddScoped gives one instance per request, which is why DbContext is registered scoped.",
            ),
            q(
                "Why is injecting a scoped service into a singleton a pitfall?",
                (
                    opt("The scoped object would outlive its scope", correct=True),
                    opt("Singletons cannot accept constructor parameters"),
                    opt("Scoped services are slower than singletons"),
                    opt("The container forbids more than one interface per class"),
                ),
                "A scoped service captured by a singleton would outlive its intended scope, which the container warns about in development.",
            ),
        ),
        "Building a REST API with ASP.NET Core": (
            q(
                "In the minimal hosting model, where is the request pipeline and services configured?",
                (
                    opt("Startup.cs"),
                    opt("Program.cs", correct=True),
                    opt("appsettings.json"),
                    opt("web.config"),
                ),
                "Everything is configured in Program.cs: register services on the builder, then build the app and wire the pipeline.",
            ),
            q(
                "Which helper returns a 201 status with a Location header for a created resource?",
                (
                    opt("Ok()"),
                    opt("NotFound()"),
                    opt("CreatedAtAction()", correct=True),
                    opt("BadRequest()"),
                ),
                "CreatedAtAction returns a 201 response together with a Location header pointing at the new resource.",
            ),
            q(
                "In a minimal API endpoint, how are dependencies like IUserService supplied?",
                (
                    opt("As lambda parameters", correct=True),
                    opt("As static class fields"),
                    opt("Through the [FromBody] attribute"),
                    opt("By calling BuildServiceProvider in the handler"),
                ),
                "With minimal APIs, dependencies are just lambda parameters on the endpoint handler.",
            ),
        ),
        "Data access with Entity Framework Core": (
            q(
                "What does a DbContext expose for each table in EF Core?",
                (
                    opt("A DbSet<T>", correct=True),
                    opt("A DbTable<T>"),
                    opt("A Repository<T>"),
                    opt("A DataReader"),
                ),
                "The DbContext exposes a DbSet<T> per table.",
            ),
            q(
                "What does calling SaveChangesAsync do with pending changes?",
                (
                    opt("Writes each change as its own separate transaction"),
                    opt("Writes all pending changes in a single transaction", correct=True),
                    opt("Discards tracked changes that were not explicitly committed"),
                    opt("Only saves inserts, never updates"),
                ),
                "SaveChangesAsync writes all pending changes in a single transaction.",
            ),
            q(
                "How do you avoid the N+1 query trap when loading related data?",
                (
                    opt("Lazy-load the navigation property inside a loop"),
                    opt(
                        "Use .Include(...) or a projection with .Select to fetch in one round trip",
                        correct=True,
                    ),
                    opt("Call FindAsync once per related row"),
                    opt("Disable change tracking on the context"),
                ),
                "Using .Include or a .Select projection fetches related data in one round trip instead of one query per row.",
            ),
        ),
        "Middleware, auth & cross-cutting concerns": (
            q(
                "What can each middleware component do as a request flows through the pipeline?",
                (
                    opt(
                        "Inspect the request, short-circuit it, or pass it to the next component",
                        correct=True,
                    ),
                    opt("Only log the request without altering it"),
                    opt("Run only after the endpoint has produced a response"),
                    opt("Replace the controller entirely"),
                ),
                "Each middleware can inspect the request, short-circuit it, or pass it to the next component and act on the response.",
            ),
            q(
                "What is the difference between UseAuthentication and UseAuthorization?",
                (
                    opt(
                        "Authentication establishes who the caller is; authorization enforces what they may do",
                        correct=True,
                    ),
                    opt("Authentication enforces permissions; authorization identifies the user"),
                    opt("They are interchangeable and order does not matter"),
                    opt("Authentication runs only in development"),
                ),
                "UseAuthentication establishes who the caller is and UseAuthorization enforces what they may do.",
            ),
            q(
                "What method must a custom middleware class implement to participate in the pipeline?",
                (
                    opt("Handle(HttpContext)"),
                    opt("InvokeAsync(HttpContext, ...)", correct=True),
                    opt("Process(HttpRequest)"),
                    opt("OnRequest(HttpContext)"),
                ),
                "A custom middleware is a class with an InvokeAsync(HttpContext, ...) that calls _next.",
            ),
        ),
        "Advanced async & performance": (
            q(
                "Why might you return ValueTask<T> instead of Task<T>?",
                (
                    opt(
                        "It avoids a heap allocation when the method often completes synchronously",
                        correct=True,
                    ),
                    opt("It always runs work on a background thread"),
                    opt("It can be awaited any number of times safely"),
                    opt("It guarantees the result is cached forever"),
                ),
                "ValueTask<T> avoids the heap allocation a Task incurs when a method often completes synchronously, such as a cache hit.",
            ),
            q(
                "What does IAsyncEnumerable<T> consumed with await foreach let you do?",
                (
                    opt("Buffer all items in memory before processing them"),
                    opt(
                        "Stream items as they become available without buffering everything",
                        correct=True,
                    ),
                    opt("Run synchronous loops on a hot path"),
                    opt("Replace Task.WhenAll for parallel work"),
                ),
                "IAsyncEnumerable<T> streams items as they become available, and await foreach consumes them without buffering everything.",
            ),
            q(
                "What does ConfigureAwait(false) communicate in library code?",
                (
                    opt("That the continuation does not need the original context", correct=True),
                    opt("That the call should block until completion"),
                    opt("That the task must run on the UI thread"),
                    opt("That exceptions should be swallowed"),
                ),
                "ConfigureAwait(false) says the continuation does not need the original context, avoiding deadlocks and reducing overhead.",
            ),
        ),
        "Testing .NET applications": (
            q(
                "Which xUnit attributes run the same test over many inputs?",
                (
                    opt("[Fact] alone"),
                    opt("[Theory] with [InlineData]", correct=True),
                    opt("[Setup] with [Teardown]"),
                    opt("[Test] with [Repeat]"),
                ),
                "[Theory] combined with [InlineData] runs the same test over many inputs, while [Fact] is a single test.",
            ),
            q(
                "What is the purpose of a mock created with Moq?",
                (
                    opt("To replace a dependency with a fake you program and verify", correct=True),
                    opt("To compile the code faster"),
                    opt("To generate random test data automatically"),
                    opt("To deploy the application to production"),
                ),
                "Mocks replace a class's dependencies with fakes you program and verify so the class can be tested in isolation.",
            ),
            q(
                "What does WebApplicationFactory<Program> enable for integration tests?",
                (
                    opt("Running unit tests without any dependencies"),
                    opt(
                        "Spinning up the whole pipeline in-memory and hitting it with a real HttpClient",
                        correct=True,
                    ),
                    opt("Mocking the database layer automatically"),
                    opt("Generating Swagger documentation"),
                ),
                "WebApplicationFactory<Program> spins up the whole ASP.NET Core pipeline in-memory and lets a real HttpClient hit it with no network or port.",
            ),
        ),
        "Design patterns & modern C#": (
            q(
                "What does the Factory pattern centralise?",
                (
                    opt("Object creation behind a method", correct=True),
                    opt("Database transactions"),
                    opt("Request routing"),
                    opt("Exception logging"),
                ),
                "The Factory pattern centralises object creation behind a method.",
            ),
            q(
                "What does a C# 12 primary constructor provide?",
                (
                    opt("Parameters available across the class", correct=True),
                    opt("A way to seal a class"),
                    opt("Automatic JSON serialization"),
                    opt("A second base class"),
                ),
                "A primary constructor (C# 12) makes its parameters available across the class.",
            ),
            q(
                "What do nullable reference types make a compile-time conversation?",
                (
                    opt("Whether a value can be null", correct=True),
                    opt("Whether a method is async"),
                    opt("Whether a class is sealed"),
                    opt("Whether a property is computed"),
                ),
                "Nullable reference types turn 'can this be null?' into a compile-time conversation, the biggest defence against NullReferenceException.",
            ),
        ),
    },
    final=(
        q(
            "How does dependency injection make code more testable?",
            (
                opt(
                    "It depends on an interface like IUserRepository instead of a concrete class, so a mock can be swapped in",
                    correct=True,
                ),
                opt("It compiles tests automatically alongside production code"),
                opt("It removes the need for any constructors"),
                opt("It forces all services to be singletons"),
            ),
            "Depending on an interface rather than a concrete class lets tests swap in a mock, which is why DI makes code testable.",
        ),
        q(
            "Which lifetime should a DbContext use when registered for an ASP.NET Core app?",
            (
                opt("Singleton"),
                opt("Scoped", correct=True),
                opt("Transient"),
                opt("Static"),
            ),
            "DbContext is registered scoped, giving one instance per request.",
        ),
        q(
            "What technique fetches related entities in one round trip to avoid N+1 queries?",
            (
                opt("Lazy loading inside a foreach loop"),
                opt("Using .Include(...) on the query", correct=True),
                opt("Calling SaveChangesAsync more often"),
                opt("Disabling migrations"),
            ),
            ".Include eager-loads related data with a JOIN in one round trip, avoiding the N+1 trap.",
        ),
        q(
            "Why should you avoid blocking on async code with .Result or .Wait()?",
            (
                opt(
                    "It can deadlock when the continuation needs a context the blocked thread holds",
                    correct=True,
                ),
                opt("It makes the method synchronous and faster"),
                opt("It prevents exceptions from being thrown"),
                opt("It is required only in unit tests"),
            ),
            "Blocking on async code can deadlock because the continuation may need a context the blocked thread is holding.",
        ),
        q(
            "Which test type uses WebApplicationFactory to exercise the full pipeline in-memory?",
            (
                opt("Unit tests"),
                opt("Integration tests", correct=True),
                opt("Load tests"),
                opt("Smoke tests run against production"),
            ),
            "Integration tests use WebApplicationFactory<Program> to run the whole pipeline in-memory and hit it with a real HttpClient.",
        ),
    ),
)
