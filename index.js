export default {
  async fetch(request, env) {
    const SUPABASE_URL = env.SUPABASE_URL;
    const SUPABASE_ANON_KEY = env.SUPABASE_ANON_KEY;

    const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IWC TERMINAL ACCESS POINT</title>
  <link href="https://fonts.googleapis.com/css2?family=Bahnschrift&display=swap" rel="stylesheet">
  <style>
    body{font-family:'Bahnschrift',Consolas,monospace;background:#000;color:#0f0;margin:0;height:100vh;display:flex;flex-direction:column;}
    #banner{background:#8b0000;color:#fff;text-align:center;padding:8px;font-weight:bold;letter-spacing:2px;}
    #timer{color:#8b0000;text-align:center;font-size:1.3em;margin:10px;}
    #terminal{flex:1;padding:20px;overflow-y:auto;background:#000;color:#0f0;}
    #input-line{display:flex;padding:0 20px 20px;}
    #input{background:#000;color:#0f0;border:none;outline:none;font-family:inherit;font-size:inherit;flex:1;}
    .blink{animation:blink 1s steps(1) infinite;}@keyframes blink{50%{opacity:0}}
    .lockout{color:#f00;font-size:2em;text-align:center;margin-top:40vh;}
  </style>
</head>
<body>
<div id="banner">UNCLASSIFIED // FOUO // IWC TERMINAL ACCESS POINT</div>
<div id="timer">SYSTEM LOCKOUT IN 300s</div>
<div id="terminal"></div>
<div id="input-line"><span>[IWC-0219D] $</span><input id="input" autocomplete="off"></div>

<script>
  const SUPABASE_URL = "${SUPABASE_URL}";
  const SUPABASE_ANON_KEY = "${SUPABASE_ANON_KEY}";
  let attempts = 0;
  let username = "";

  async function logEntry(data) {
    try {
      await fetch(`${SUPABASE_URL}/rest/v1/fbi_logs`, {
        method: "POST",
        headers: {
          "apikey": SUPABASE_ANON_KEY,
          "Authorization": "Bearer " + SUPABASE_ANON_KEY,
          "Content-Type": "application/json",
          "Prefer": "return=minimal"
        },
        body: JSON.stringify(data)
      });
    } catch(e) {}
  }

  document.addEventListener("DOMContentLoaded", () => {
    const term = document.getElementById("terminal");
    const input = document.getElementById("input");
    term.innerHTML = "<div style='color:#8b0000;font-weight:bold'>UNCLASSIFIED // FOUO</div>IWC // INTELLIGENCE WARFARE CELL<br>POLICY DIRECTIVE 0219D<br><span style='color:#ff0;'>*** WARNING: 3 failed attempts = SYSTEM LOCKOUT (18 USC § 1030) ***</span><br><br>Last login: Wed Dec 3 00:12:01 2025 from Cloudflare<br>login: ";
    input.focus();

    input.addEventListener("keydown", async e => {
      if (e.key !== "Enter") return;
      const cmd = input.value.trim();
      term.innerHTML += cmd + "<br>";
      input.value = "";

      if (!username) {
        username = cmd;
        term.innerHTML += "Password: ";
      } else {
        attempts++;
        await logEntry({ip:"Cloudflare",user_agent:navigator.userAgent,username,command:cmd,phase:"failed_login_"+attempts,raw:"login:"+username+" pass:"+cmd});

        if (attempts >= 3) {
          term.innerHTML += "<br><span class='lockout'>SYSTEM LOCKOUT INITIATED<br>TERMINAL SELF-DESTRUCT IN 10 SECONDS</span>";
          input.disabled = true;
          setTimeout(() => document.body.innerHTML = "<h1 style='color:#f00;text-align:center;margin-top:40vh'>TERMINAL SELF-DESTRUCTED</h1>", 10000);
        } else {
          term.innerHTML += "Login incorrect. Attempt " + attempts + "/3<br>login: ";
        }
      }
      term.scrollTop = term.scrollHeight;
    });
  });

  let timeLeft = 300;
  const timer = setInterval(() => {
    timeLeft--;
    document.getElementById('timer').textContent = "SYSTEM LOCKOUT IN " + timeLeft + "s";
    if (timeLeft <= 0) document.body.innerHTML = "<h1 style='color:#f00;text-align:center;margin-top:40vh'>TERMINAL SELF-DESTRUCTED</h1>";
  }, 1000);
</script>
</body>
</html>`;

    return new Response(html, { headers: { "Content-Type": "text/html" } });
  }
};
