from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="AURADECOR.ai - AI Interior Design Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Go up from app/ to project root
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, "static")), name="static")
app.mount("/ai-studio", StaticFiles(directory=os.path.join(PROJECT_ROOT, "static", "google-studio")), name="ai-studio")

# Templates directory
templates = Jinja2Templates(directory=os.path.join(PROJECT_ROOT, "templates"))

# Simple user database (in-memory)
users_db = {}


# ------------------ Homepage ------------------ #

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ------------------ داشبورد مالک ------------------ #

@app.get("/register/owner", response_class=HTMLResponse)
async def owner_dashboard():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Owner Dashboard | AURADECOR.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter',sans-serif;
            background:#050505;
            color:#fff;
        }
        .topbar {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:16px 32px;
            border-bottom:1px solid #333;
            background:rgba(5,5,5,0.96);
            position:sticky;
            top:0;
            z-index:10;
        }
        .brand {
            font-weight:600;
            color:#D4AF37;
        }
        .user {
            font-size:14px;
            color:#aaa;
        }
        .layout {
            display:grid;
            grid-template-columns:260px 1fr;
            min-height:100vh;
        }
        .sidebar {
            border-right:1px solid #222;
            padding:24px 18px;
            background:#070707;
        }
        .sidebar h2 {
            font-size:14px;
            color:#777;
            margin-bottom:16px;
        }
        .nav-item {
            padding:10px 12px;
            border-radius:10px;
            font-size:14px;
            color:#ccc;
            cursor:pointer;
            margin-bottom:6px;
        }
        .nav-item.active {
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
        }
        .nav-item:hover {
            background:rgba(255,255,255,0.05);
        }
        .content {
            padding:28px 32px 40px;
        }
        .section-title {
            font-size:22px;
            margin-bottom:8px;
        }
        .section-sub {
            font-size:14px;
            color:#aaa;
            margin-bottom:24px;
        }
        .card-row {
            display:grid;
            grid-template-columns:2fr 1.3fr;
            gap:24px;
            margin-bottom:32px;
        }
        .card {
            background:rgba(255,255,255,0.03);
            border-radius:20px;
            border:1px solid rgba(212,175,55,0.20);
            padding:20px 18px;
        }
        .card h3 {
            font-size:16px;
            margin-bottom:10px;
            color:#D4AF37;
        }
        .card p {
            font-size:13px;
            color:#aaa;
            margin-bottom:14px;
        }
        .upload-box {
            border:1px dashed rgba(212,175,55,0.5);
            border-radius:16px;
            padding:18px;
            text-align:center;
            background:rgba(0,0,0,0.5);
        }
        .upload-box input[type=file] {
            margin-top:12px;
            color:#ccc;
        }
        .btn {
            display:inline-block;
            padding:10px 20px;
            border-radius:999px;
            border:none;
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
            font-size:14px;
            cursor:pointer;
            margin-top:10px;
        }
        .btn:hover {
            box-shadow:0 12px 30px rgba(212,175,55,0.4);
            transform:translateY(-1px);
        }
        .projects-list {
            margin-top:10px;
        }
        .project-item {
            padding:10px 0;
            border-bottom:1px solid #222;
            font-size:13px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }
        .badge {
            padding:3px 9px;
            border-radius:999px;
            font-size:11px;
        }
        .badge-processing {
            background:#333;
            color:#F1C40F;
        }
        .badge-ready {
            background:#16361a;
            color:#2ecc71;
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="brand">AURADECOR.ai · Owner</div>
        <div class="user">You are logged in as <span style="color:#D4AF37;">Homeowner</span></div>
    </div>

    <div class="layout">
        <aside class="sidebar">
            <h2>Navigation</h2>
            <div class="nav-item active">Dashboard</div>
            <a href="/owner/projects" style="text-decoration:none;">
                <div class="nav-item">My Projects</div>
            </a>
            <div class="nav-item">Downloads</div>
            <div class="nav-item">Subscription</div>
            <div class="nav-item">Account Settings</div>
        </aside>

        <main class="content">
            <h1 class="section-title">Welcome to your design studio</h1>
            <p class="section-sub">Upload a floor plan, choose a style and let AURADECOR.ai generate stunning interiors for you.</p>

            <div class="card-row">
                <div class="card">
                    <h3>Start a new project</h3>
                    <p>Upload your floor plan and select your preferred style. We’ll generate multiple AI-powered designs for you.</p>
                    <div class="upload-box">
                        <p style="font-size:13px;">Drop your floor plan file here, or click to select.</p>
                        <input type="file" name="floorplan" accept="image/*,.pdf">
                        <div style="margin-top:12px;">
                            <select name="style" style="padding:8px 10px;border-radius:999px;border:1px solid #555;background:#000;color:#fff;font-size:13px;">
                                <option value="modern">Modern</option>
                                <option value="luxury">Luxury</option>
                                <option value="minimal">Minimal</option>
                                <option value="classic">Classic</option>
                                <option value="industrial">Industrial</option>
                            </select>
                        </div>
                        <button class="btn" type="button">Generate Design (mock)</button>
                    </div>
                </div>

                <div class="card">
                    <h3>Subscription status</h3>
                    <p>Your free trial is active. You can generate 1 design for free before subscribing.</p>
                    <p style="font-size:13px;color:#ddd;">
                        Upgrade to unlock unlimited projects and priority AI rendering.
                    </p>
                    <button class="btn" type="button" onclick="alert('Subscription flow will be implemented later.')">
                        View plans
                    </button>
                </div>
            </div>

            <div class="card">
                <h3>Your recent projects</h3>
                <div class="projects-list">
                    <div class="project-item">
                        <span>Modern Apartment · Living + Kitchen</span>
                        <span class="badge badge-processing">processing (mock)</span>
                    </div>
                    <div class="project-item">
                        <span>Luxury Villa · Master Bedroom</span>
                        <span class="badge badge-ready">ready (mock)</span>
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
    """)


# ------------------ داشبورد تأمین‌کننده ------------------ #

@app.get("/register/contractor", response_class=HTMLResponse)
async def contractor_dashboard():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contractor Dashboard | AURADECOR.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter',sans-serif;
            background:#050505;
            color:#fff;
        }
        .topbar {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:16px 32px;
            border-bottom:1px solid #333;
            background:rgba(5,5,5,0.96);
            position:sticky;
            top:0;
            z-index:10;
        }
        .brand {
            font-weight:600;
            color:#D4AF37;
        }
        .user {
            font-size:14px;
            color:#aaa;
        }
        .layout {
            display:grid;
            grid-template-columns:260px 1fr;
            min-height:100vh;
        }
        .sidebar {
            border-right:1px solid #222;
            padding:24px 18px;
            background:#070707;
        }
        .sidebar h2 {
            font-size:14px;
            color:#777;
            margin-bottom:16px;
        }
        .nav-item {
            padding:10px 12px;
            border-radius:10px;
            font-size:14px;
            color:#ccc;
            cursor:pointer;
            margin-bottom:6px;
        }
        .nav-item.active {
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
        }
        .nav-item:hover {
            background:rgba(255,255,255,0.05);
        }
        .content {
            padding:28px 32px 40px;
        }
        .section-title {
            font-size:22px;
            margin-bottom:8px;
        }
        .section-sub {
            font-size:14px;
            color:#aaa;
            margin-bottom:24px;
        }
        .card-row {
            display:grid;
            grid-template-columns:1.5fr 1.2fr;
            gap:24px;
            margin-bottom:32px;
        }
        .card {
            background:rgba(255,255,255,0.03);
            border-radius:20px;
            border:1px solid rgba(212,175,55,0.20);
            padding:20px 18px;
        }
        .card h3 {
            font-size:16px;
            margin-bottom:10px;
            color:#D4AF37;
        }
        .card p {
            font-size:13px;
            color:#aaa;
            margin-bottom:14px;
        }
        .field {
            margin-bottom:14px;
        }
        .field label {
            display:block;
            font-size:13px;
            margin-bottom:6px;
            color:#ddd;
        }
        .field input, .field textarea, .field select {
            width:100%;
            padding:10px 12px;
            border-radius:12px;
            border:1px solid #444;
            background:#000;
            color:#fff;
            font-size:13px;
        }
        .field textarea {
            min-height:70px;
            resize:vertical;
        }
        .hint {
            font-size:11px;
            color:#777;
            margin-top:2px;
        }
        .btn {
            display:inline-block;
            padding:10px 20px;
            border-radius:999px;
            border:none;
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
            font-size:14px;
            cursor:pointer;
            margin-top:8px;
        }
        .btn:hover {
            box-shadow:0 12px 30px rgba(212,175,55,0.4);
            transform:translateY(-1px);
        }
        .lead-list {
            margin-top:10px;
        }
        .lead-item {
            padding:10px 0;
            border-bottom:1px solid #222;
            font-size:13px;
        }
        .badge-lead {
            padding:3px 9px;
            border-radius:999px;
            font-size:11px;
            background:#1b2836;
            color:#4aa3ff;
        }
        .portfolio-grid {
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
            gap:10px;
            margin-top:10px;
            font-size:11px;
            color:#aaa;
        }
        .portfolio-item {
            border-radius:12px;
            border:1px dashed #444;
            padding:8px;
            text-align:center;
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="brand">AURADECOR.ai · Contractor</div>
        <div class="user">You are logged in as <span style="color:#D4AF37;">Supplier / Contractor</span></div>
    </div>

    <div class="layout">
        <aside class="sidebar">
            <h2>Navigation</h2>
            <div class="nav-item active">Dashboard</div>
            <div class="nav-item">Incoming Projects</div>
            <div class="nav-item">Profile & Portfolio</div>
            <div class="nav-item">Subscription</div>
            <div class="nav-item">Account Settings</div>
        </aside>

        <main class="content">
            <h1 class="section-title">Get projects from AURADECOR owners</h1>
            <p class="section-sub">Complete your profile, upload your portfolio and start receiving design leads.</p>

            <div class="card-row">
                <div class="card">
                    <h3>Profile & resume</h3>
                    <p>Introduce your company so homeowners can quickly understand who you are and what you do.</p>
                    <form>
                        <div class="field">
                            <label>Company / Brand name</label>
                            <input type="text" placeholder="e.g. Golden Space Interiors">
                        </div>
                        <div class="field">
                            <label>Location</label>
                            <input type="text" placeholder="City, Country">
                        </div>
                        <div class="field">
                            <label>Specialization</label>
                            <select>
                                <option>Interior fit-out</option>
                                <option>Furniture supplier</option>
                                <option>Lighting & electrical</option>
                                <option>Full turnkey contractor</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>WhatsApp number</label>
                            <input type="text" placeholder="+971 5x xxx xxxx">
                            <div class="hint">This number will be used to connect you directly with homeowners.</div>
                        </div>
                        <div class="field">
                            <label>Website / Instagram</label>
                            <input type="text" placeholder="https://yourwebsite.com or @yourinstagram">
                        </div>
                        <div class="field">
                            <label>Resume link (optional)</label>
                            <input type="text" placeholder="Link to your PDF resume on Drive / Dropbox">
                        </div>
                        <div class="field">
                            <label>Short bio</label>
                            <textarea placeholder="Describe your experience, style and what makes you unique."></textarea>
                        </div>
                        <button class="btn" type="button">Save profile (mock)</button>
                    </form>
                </div>

                <div class="card">
                    <h3>Portfolio / sample projects</h3>
                    <p>Upload a few of your best projects so homeowners can see your style and quality.</p>
                    <div class="field">
                        <label>Upload sample images</label>
                        <input type="file" multiple accept="image/*">
                        <div class="hint">You can upload multiple JPG/PNG images. In production, these will be stored in your portfolio.</div>
                    </div>
                    <div class="portfolio-grid">
                        <div class="portfolio-item">Sample project 1 (mock)</div>
                        <div class="portfolio-item">Sample project 2 (mock)</div>
                        <div class="portfolio-item">Sample project 3 (mock)</div>
                    </div>
                    <button class="btn" type="button" onclick="alert('Portfolio upload will be implemented later.')">
                        Save portfolio (mock)
                    </button>
                </div>
            </div>

            <div class="card">
                <h3>Latest design leads</h3>
                <p style="font-size:13px;color:#ddd;">Once your subscription is active, you’ll see real-time projects that match your profile here.</p>
                <div class="lead-list">
                    <div class="lead-item">
                        <strong>Dubai · 2BR Apartment</strong><br>
                        Modern living + kitchen design ready.
                        <span class="badge-lead">preview (mock)</span>
                    </div>
                    <div class="lead-item">
                        <strong>Tehran · Office lobby</strong><br>
                        Luxury reception area design ready.
                        <span class="badge-lead">preview (mock)</span>
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
    """)


# ------------------ صفحات احراز هویت (Login / Register) ------------------ #

# ------------------ Login Page ------------------ #

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Get Started | AURADECOR.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter',sans-serif;
            background:#050505;
            color:#fff;
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
        }
        .card {
            background:rgba(255,255,255,0.03);
            border:1px solid rgba(212,175,55,0.25);
            border-radius:24px;
            padding:40px 32px;
            width:100%;
            max-width:480px;
            box-shadow:0 20px 60px rgba(0,0,0,0.6);
        }
        h1 {
            font-size:24px;
            margin-bottom:8px;
            color:#D4AF37;
        }
        p.sub {
            font-size:14px;
            color:#aaa;
            margin-bottom:24px;
        }
        .role-row {
            display:flex;
            gap:12px;
            margin-bottom:22px;
        }
        .role {
            flex:1;
            padding:14px 12px;
            border-radius:16px;
            border:1px solid rgba(212,175,55,0.35);
            background:rgba(0,0,0,0.7);
            text-align:left;
            cursor:pointer;
        }
        .role h3 {
            font-size:14px;
            margin-bottom:4px;
            color:#D4AF37;
        }
        .role p {
            font-size:12px;
            color:#aaa;
        }
        .field {
            margin-bottom:18px;
        }
        .field label {
            display:block;
            font-size:13px;
            margin-bottom:6px;
            color:#ddd;
        }
        .field input {
            width:100%;
            padding:12px 14px;
            border-radius:12px;
            border:1px solid rgba(212,175,55,0.3);
            background:rgba(0,0,0,0.6);
            color:#fff;
            font-size:14px;
        }
        .field input:focus {
            outline:none;
            border-color:#D4AF37;
            box-shadow:0 0 0 2px rgba(212,175,55,0.25);
        }
        button {
            width:100%;
            padding:14px;
            border-radius:999px;
            border:none;
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
            cursor:pointer;
            font-size:15px;
        }
        button:hover {
            box-shadow:0 16px 40px rgba(212,175,55,0.45);
            transform:translateY(-1px);
        }
        .link-row {
            margin-top:18px;
            font-size:13px;
            color:#bbb;
            text-align:center;
        }
        .link-row a {
            color:#D4AF37;
            text-decoration:none;
            font-weight:500;
        }
        .top-link {
            position:fixed;
            top:20px;
            left:30px;
            font-size:13px;
        }
        .top-link a {
            color:#D4AF37;
            text-decoration:none;
        }
    </style>
</head>
<body>
    <div class="top-link"><a href="/">← Back to Home</a></div>
    <div class="card">
        <h1>Create your account</h1>
        <p class="sub">Choose your role and start using AURADECOR.ai in minutes.</p>

        <div style="margin-bottom: 18px;">
            <button type="button"
                    style="
                        width:100%;
                        padding:12px;
                        border-radius:999px;
                        border:1px solid rgba(212,175,55,0.4);
                        background:#111;
                        color:#fff;
                        font-weight:500;
                        font-size:14px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        gap:8px;
                        cursor:pointer;
                    "
                    onclick="window.location.href='/auth/google'">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                     alt="Google" style="width:18px;height:18px;">
                <span>Continue with Google</span>
            </button>
        </div>
        <div style="text-align:center;margin:12px 0 18px;color:#777;font-size:12px;">
            <span style="background:#050505;padding:0 8px;">or sign up with email</span>
            <hr style="border:none;border-top:1px solid #333;margin-top:-10px;">
        </div>

        <form action="/register" method="post">
            <div class="role-row">
                <label class="role">
                    <input type="radio" name="role" value="owner" required style="margin-right:6px;">
                    <h3>Homeowner</h3>
                    <p>Upload floor plans and get AI-generated interiors.</p>
                </label>
                <label class="role">
                    <input type="radio" name="role" value="contractor" required style="margin-right:6px;">
                    <h3>Contractor</h3>
                    <p>Receive projects and connect with clients.</p>
                </label>
            </div>
            <div class="field">
                <label for="email">Email address</label>
                <input id="email" name="email" type="email" required placeholder="you@example.com">
            </div>
            <div class="field">
                <label for="password">Password</label>
                <input id="password" name="password" type="password" required placeholder="••••••••">
            </div>
            <button type="submit">Get Started</button>
        </form>
        <div class="link-row">
            Already have an account?
            <a href="/login">Sign in</a>
        </div>
    </div>
</body>
</html>
    """)


@app.get("/auth/google", response_class=HTMLResponse)
async def auth_google_mock():
    return HTMLResponse(
        "<h2 style='font-family:Arial;color:#D4AF37;text-align:center;margin-top:80px;'>"
        "Google OAuth will be implemented here soon 🚀</h2>"
    )


# ------------------ صفحات پروژه‌های Owner ------------------ #

@app.get("/owner/projects", response_class=HTMLResponse)
async def owner_projects():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Projects | AURADECOR.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter',sans-serif;
            background:#050505;
            color:#fff;
            min-height:100vh;
        }
        .topbar {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:16px 32px;
            border-bottom:1px solid #333;
            background:rgba(5,5,5,0.96);
            position:sticky;
            top:0;
            z-index:10;
        }
        .brand { font-weight:600; color:#D4AF37; }
        .layout {
            display:grid;
            grid-template-columns:260px 1fr;
            min-height:100vh;
        }
        .sidebar {
            border-right:1px solid #222;
            padding:24px 18px;
            background:#070707;
        }
        .sidebar h2 {
            font-size:14px;
            color:#777;
            margin-bottom:16px;
        }
        .nav-item {
            padding:10px 12px;
            border-radius:10px;
            font-size:14px;
            color:#ccc;
            cursor:pointer;
            margin-bottom:6px;
        }
        .nav-item.active {
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
        }
        .nav-item:hover {
            background:rgba(255,255,255,0.05);
        }
        .content {
            padding:28px 32px 40px;
        }
        .section-title {
            font-size:22px;
            margin-bottom:8px;
        }
        .section-sub {
            font-size:14px;
            color:#aaa;
            margin-bottom:24px;
        }
        .projects-table {
            width:100%;
            border-collapse:collapse;
            font-size:13px;
        }
        .projects-table th, .projects-table td {
            padding:10px 8px;
            border-bottom:1px solid #222;
            text-align:left;
        }
        .projects-table th {
            color:#bbb;
            font-weight:500;
        }
        .badge {
            padding:3px 9px;
            border-radius:999px;
            font-size:11px;
        }
        .badge-processing {
            background:#333;
            color:#F1C40F;
        }
        .badge-ready {
            background:#16361a;
            color:#2ecc71;
        }
        .new-btn {
            display:inline-block;
            padding:9px 18px;
            border-radius:999px;
            border:none;
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
            font-size:13px;
            text-decoration:none;
        }
        .new-btn:hover {
            box-shadow:0 10px 26px rgba(212,175,55,0.4);
            transform:translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="brand">AURADECOR.ai · Owner</div>
        <a href="/register/owner" style="color:#D4AF37;font-size:13px;text-decoration:none;">Back to dashboard</a>
    </div>

    <div class="layout">
        <aside class="sidebar">
            <h2>Navigation</h2>
            <a href="/register/owner" style="text-decoration:none;">
                <div class="nav-item">Dashboard</div>
            </a>
            <div class="nav-item active">My Projects</div>
            <div class="nav-item">Downloads</div>
            <div class="nav-item">Subscription</div>
            <div class="nav-item">Account Settings</div>
        </aside>

        <main class="content">
            <h1 class="section-title">My Projects</h1>
            <p class="section-sub">All floor plans you have uploaded and the designs generated by AURADECOR.ai.</p>

            <div style="margin-bottom:18px;">
                <a href="/owner/projects/new" class="new-btn">+ New Project</a>
            </div>

            <table class="projects-table">
                <thead>
                    <tr>
                        <th>Project name</th>
                        <th>Type</th>
                        <th>Style</th>
                        <th>Status</th>
                        <th>Last update</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Modern Apartment · Living + Kitchen</td>
                        <td>Residential</td>
                        <td>Modern</td>
                        <td><span class="badge badge-processing">processing (mock)</span></td>
                        <td>Today · 12:30</td>
                    </tr>
                    <tr>
                        <td>Luxury Villa · Master Bedroom</td>
                        <td>Residential</td>
                        <td>Luxury</td>
                        <td><span class="badge badge-ready">ready (mock)</span></td>
                        <td>Yesterday · 19:05</td>
                    </tr>
                </tbody>
            </table>
        </main>
    </div>
</body>
</html>
    """)


@app.get("/owner/projects/new", response_class=HTMLResponse)
async def owner_new_project():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>New Project | AURADECOR.ai</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Inter',sans-serif;
            background:#050505;
            color:#fff;
            min-height:100vh;
        }
        .topbar {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:16px 32px;
            border-bottom:1px solid #333;
            background:rgba(5,5,5,0.96);
            position:sticky;
            top:0;
            z-index:10;
        }
        .brand { font-weight:600; color:#D4AF37; }
        .container {
            max-width:900px;
            margin:0 auto;
            padding:28px 20px 40px;
        }
        .section-title {
            font-size:22px;
            margin-bottom:8px;
        }
        .section-sub {
            font-size:14px;
            color:#aaa;
            margin-bottom:24px;
        }
        .card {
            background:rgba(255,255,255,0.03);
            border-radius:20px;
            border:1px solid rgba(212,175,55,0.20);
            padding:24px 20px;
        }
        .field {
            margin-bottom:16px;
        }
        .field label {
            display:block;
            font-size:13px;
            margin-bottom:6px;
            color:#ddd;
        }
        .field input, .field select, .field textarea {
            width:100%;
            padding:10px 12px;
            border-radius:12px;
            border:1px solid #444;
            background:#000;
            color:#fff;
            font-size:13px;
        }
        .field textarea {
            min-height:70px;
            resize:vertical;
        }
        .upload-box {
            border:1px dashed rgba(212,175,55,0.6);
            border-radius:16px;
            padding:18px;
            background:rgba(0,0,0,0.5);
            text-align:center;
        }
        .upload-box p {
            font-size:13px;
            color:#ccc;
            margin-bottom:8px;
        }
        .btn {
            display:inline-block;
            padding:11px 22px;
            border-radius:999px;
            border:none;
            background:linear-gradient(135deg,#D4AF37,#F1C40F);
            color:#000;
            font-weight:600;
            font-size:14px;
            cursor:pointer;
            margin-top:14px;
        }
        .btn:hover {
            box-shadow:0 12px 30px rgba(212,175,55,0.4);
            transform:translateY(-1px);
        }
        .hint {
            font-size:11px;
            color:#777;
            margin-top:4px;
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="brand">AURADECOR.ai · Owner</div>
        <a href="/owner/projects" style="color:#D4AF37;font-size:13px;text-decoration:none;">Back to My Projects</a>
    </div>

    <div class="container">
        <h1 class="section-title">Create a new project</h1>
        <p class="section-sub">Upload a floor plan, choose the space type and style, and let AURADECOR.ai generate designs.</p>

        <div class="card">
            <form>
                <div class="field">
                    <label>Project name</label>
                    <input type="text" placeholder="e.g. Modern apartment - living + kitchen">
                </div>
                <div class="field">
                    <label>Project type</label>
                    <select>
                        <option>Residential</option>
                        <option>Office</option>
                        <option>Retail</option>
                        <option>Hospitality</option>
                    </select>
                </div>
                <div class="field">
                    <label>Preferred style</label>
                    <select>
                        <option>Modern</option>
                        <option>Luxury</option>
                        <option>Minimal</option>
                        <option>Classic</option>
                        <option>Industrial</option>
                    </select>
                </div>
                <div class="field">
                    <label>Floor plan file</label>
                    <div class="upload-box">
                        <p>Drop your floor plan image/PDF here, or click to choose.</p>
                        <input type="file" accept="image/*,.pdf">
                        <div class="hint">Supported formats: JPG, PNG, PDF. Max 25MB (mock for now).</div>
                    </div>
                </div>
                <div class="field">
                    <label>Notes for designer (optional)</label>
                    <textarea placeholder="Any specific requirements, colors, furniture brands, etc."></textarea>
                </div>
                <button class="btn" type="button" onclick="alert('Project creation will be implemented with database in the next step.')">
                    Create project (mock)
                </button>
            </form>
        </div>
    </div>
</body>
</html>
    """)


# ------------------ Login Handler ------------------ #

@app.post("/api/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user_id = f"user_{len(users_db) + 1}"
    users_db[user_id] = {"email": email, "password": password, "projects": []}
    print(f"[DEBUG LOGIN] Created user_id: {user_id}, users_db keys: {list(users_db.keys())}")
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=user_id, httponly=True, samesite="lax")
    print(f"[DEBUG LOGIN] Set cookie: user_id={user_id}")
    return response

# ------------------ Dashboard ------------------ #

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = request.cookies.get("user_id")
    all_cookies = dict(request.cookies)
    print(f"[DEBUG DASHBOARD] All cookies: {all_cookies}")
    print(f"[DEBUG DASHBOARD] user_id from cookie: {user_id}")
    print(f"[DEBUG DASHBOARD] users_db keys: {list(users_db.keys())}")
    
    if not user_id or user_id not in users_db:
        print(f"[DEBUG DASHBOARD] Authentication failed - redirecting to /login")
        return RedirectResponse(url="/login", status_code=303)
    
    print(f"[DEBUG DASHBOARD] Authentication successful for user_id: {user_id}")
    user = users_db.get(user_id, {})
    projects = user.get("projects", [])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects": projects
    })

# ------------------ New Project (Google AI Studio) ------------------ #

@app.get("/new-project")
async def new_project(request: Request):
    user_id = request.cookies.get("user_id")
    print(f"[DEBUG NEW-PROJECT] user_id from cookie: {user_id}")
    if not user_id or user_id not in users_db:
        print(f"[DEBUG NEW-PROJECT] Authentication failed - redirecting to /login")
        return RedirectResponse(url="/login", status_code=303)
    return FileResponse(os.path.join(PROJECT_ROOT, "static", "google-studio", "index.html"))

# ------------------ Logout ------------------ #

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_id")
    return response

# ------------------ Google AI Studio Assets (Root Paths) ------------------ #
# Serve assets from static/google-studio/ at root paths for the React app
@app.get("/{file_path:path}")
async def serve_google_studio_assets(request: Request, file_path: str):
    """
    Serve assets from static/google-studio/ directory at root paths.
    This allows the React app to load files like /index.tsx, /App.tsx, etc.
    """
    # Reserved routes that should not be handled here
    reserved_routes = ["login", "dashboard", "new-project", "logout", "api", "static", "ai-studio", "register", "owner", "auth"]
    first_segment = file_path.split("/")[0] if "/" in file_path else file_path
    
    # If it's a reserved route or empty, return 404
    if not file_path or first_segment in reserved_routes:
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check if file exists in static/google-studio/
    studio_path = os.path.join(PROJECT_ROOT, "static", "google-studio", file_path)
    
    # Security check: ensure path is within google-studio directory
    abs_studio_path = os.path.abspath(studio_path)
    abs_studio_dir = os.path.join(PROJECT_ROOT, "static", "google-studio")
    
    if not abs_studio_path.startswith(abs_studio_dir):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check if file exists
    if os.path.exists(studio_path) and os.path.isfile(studio_path):
        return FileResponse(studio_path)
    
    # If file doesn't exist, return 404
    raise HTTPException(status_code=404, detail="File not found")

# ------------------ پردازش فرم‌ها (ساده / Mock) ------------------ #


@app.post("/register")
async def register_submit(
    role: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    if role == "owner":
        redirect_url = "/register/owner"
    else:
        redirect_url = "/register/contractor"

    html = (
        "<h2 style='color:#D4AF37;"
        "font-family:Arial;"
        "text-align:center;"
        "margin-top:80px;'>"
        f"Registered as {role}. Next: "
        f"<a href='{redirect_url}'>continue</a></h2>"
    )
    return HTMLResponse(html)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
