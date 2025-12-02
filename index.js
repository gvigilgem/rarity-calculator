export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/" || url.pathname === "/login") {
      return new Response(loginHtml, { headers: { "Content-Type": "text/html" } });
    }

    if (url.pathname === "/auth" && request.method === "POST") {
      const form = await request.formData();
      const email = form.get("email");
      const password = form.get("password");

      const res = await fetch(`${env.SUPABASE_URL}/auth/v1/token?grant_type=password`, {
        method: "POST",
        headers: {
          apikey: env.SUPABASE_ANON_KEY,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      if (res.ok) {
        const { access_token } = await res.json();
        return new Response(successHtml(access_token), { headers: { "Content-Type": "text/html" } });
      }
      return new Response(failHtml, { headers: { "Content-Type": "text/html" } });
    }

    if (url.pathname === "/portal") {
      return new Response(portalHtml, { headers: { "Content-Type": "text/html" } });
    }

    return new Response("404", { status: 404 });
  }
};

const loginHtml = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>FBI Access Portal</title>
<style>body{background:#0d1b2a;font-family:Arial,Helvetica,sans-serif;color:#e0e1dd;margin:0;padding:0}
.container{max-width:420px;margin:8% auto;background:#1b263b;padding:40px;border-radius:8px;box-shadow:0 0 20px #ff006e33}
h1{color:#ff006e;text-align:center;margin-bottom:30px}
input{width:100%;padding:14px;margin:10px 0;border:none;border-radius:4px;background:#283845;color:#e0e1dd}
button{width:100%;padding:14px;background:#ff006e;border:none;color:white;font-weight:bold;border-radius:4px;cursor:pointer}
button:hover{background:#d4005b}
.warning{background:#8b0000;color:#ffcccc;padding:12px;border-radius:4px;margin-bottom:20px;text-align:center}
</style></head>
<body><div class="container">
<div class="warning">RESTRICTED ACCESS — FEDERAL BUREAU OF INVESTIGATION</div>
<h1>FBI SECURE ACCESS</h1>
<form action="/auth" method="post">
<input type="email" name="email" placeholder="AGENT EMAIL" required autocomplete="off">
<input type="password" name="password" placeholder="PASSWORD" required>
<button type="submit">AUTHENTICATE</button>
</form></div></body></html>`;

const failHtml = `<html><body style="background:#0d1b2a;color:#ff006e;text-align:center;margin-top:15%">
<h1>ACCESS DENIED</h1><p>Invalid credentials.</p><a href="/" style="color:#ff006e">Return</a></body></html>`;

const successHtml = (token) => `<html><body style="background:#0d1b2a;color:#e0e1dd;text-align:center;margin-top:15%">
<h1 style="color:#ff006e">AUTHENTICATION SUCCESSFUL</h1>
<script>localStorage.setItem('sb-access', '${token}'); setTimeout(()=>location='/portal',800)</script>
<p>Redirecting to secure portal...</p></body></html>`;

const portalHtml = `<!DOCTYPE html>
<html><body style="background:#0d1b2a;color:#e0e1dd;font-family:Arial;margin:0;padding:20px">
<div style="max-width:900px;margin:auto;background:#1b263b;padding:30px;border-radius:8px">
<div style="background:#8b0000;color:#ffcccc;padding:15px;text-align:center;font-weight:bold">
FEDERAL BUREAU OF INVESTIGATION — CLASSIFIED DOCUMENT REPOSITORY
</div>
<h1 style="color:#ff006e;text-align:center">Welcome, Agent</h1>
<p style="text-align:center">You are now inside the secure zone.</p>
<div style="text-align:center;margin:40px">
<button onclick="fetch('${env?.SUPABASE_URL || ''}/rest/v1/documents',{headers:{'apikey':localStorage.getItem('sb-access'),'Authorization':'Bearer '+localStorage.getItem('sb-access')}})
.then(r=>r.json()).then(d=>alert('Documents loaded'))" 
style="padding:15px 40px;background:#ff006e;border:none;color:white;font-size:18px;cursor:pointer">
LOAD CLASSIFIED DOCUMENTS
</button>
</div>
<div style="text-align:center"><a href="/" style="color:#ff006e">Logout</a></div>
</div></body></html>`;
