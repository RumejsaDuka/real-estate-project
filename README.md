<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Contact Us - Grand Realty</title>
  <link rel="stylesheet" href="css/style.css" />
  <link rel="icon" type="image/x-icon" href="images/logo.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
</head>
<body>

<header class="navbar inner-page" id="navbar">
  <div class="nav-container">
    <a href="index.html" class="nav-logo">
      <img src="images/logo.jpg" alt="Grand Realty Logo" class="logo-icon" />
      <span class="logo-text">Grand Realty</span>
    </a>

    <nav class="nav-links">
      <a href="index.html" class="nav-link">Home</a>
      <a href="listings.html" class="nav-link">Listings</a>
      <a href="blog.html" class="nav-link">Blog</a>
      <a href="about.html" class="nav-link">About</a>
      <a href="contact.html" class="nav-link active">Contact</a>
    </nav>

    <button class="nav-toggle" id="navToggle">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</header>

<main>

<section class="hero-mini" style="background: var(--dark-blue); padding: 120px 0 60px; text-align: center; color: white;">
  <div class="container">
    <h1 class="section-title" style="color: white;">Get In Touch</h1>
    <p>We are here to help you with any inquiries regarding our premium properties.</p>
  </div>
</section>

<section class="contact-section" style="padding: 80px 0;">
  <div class="container">

    <div class="property-layout" style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 40px;">

    
      <div class="contact-form-container">
        <h2 class="prop-section-title">Send Us a Message</h2>

        <form id="contactForm" class="contact-form">

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div class="form-group">
              <label>Full Name</label>
              <input type="text" class="search-input" required>
            </div>

            <div class="form-group">
              <label>Email Address</label>
              <input type="email" class="search-input" required>
            </div>
          </div>

          <div class="form-group" style="margin-bottom: 20px;">
            <label>Subject</label>
            <input type="text" class="search-input">
          </div>

          <div class="form-group" style="margin-bottom: 20px;">
            <label>Message</label>
            <textarea class="search-input" style="height: 150px;" required></textarea>
          </div>

          <button type="submit" class="btn btn-gold" style="width: 100%;">Submit Inquiry</button>
        </form>
      </div>

      <div class="contact-info-sidebar">
        <h2 class="prop-section-title">Contact Details</h2>

        <div class="overview-grid" style="display: flex; flex-direction: column; gap: 20px;">

          <div class="overview-item">
            <span class="ov-label"><i class="fas fa-phone"></i> Phone</span>
            <span class="ov-value">
              <a href="tel:+13105550192">(310) 555-0192</a>
            </span>
          </div>

          <div class="overview-item">
            <span class="ov-label"><i class="fas fa-envelope"></i> Email</span>
            <span class="ov-value">
              <a href="mailto:hello@grandrealty.com">hello@grandrealty.com</a>
            </span>
          </div>

          <div class="overview-item">
            <span class="ov-label"><i class="fas fa-map-marker-alt"></i> Address</span>
            <span class="ov-value">
              <a href="https://www.google.com/maps?q=1420+Harbor+Blvd,+Los+Angeles" target="_blank">
                1420 Harbor Blvd, Los Angeles, CA
              </a>
            </span>
          </div>

          <div class="overview-item">
            <span class="ov-label"><i class="fas fa-clock"></i> Hours</span>
            <span class="ov-value">Mon - Fri: 09:00 - 18:00</span>
          </div>

        </div>
      </div>

    </div>

  </div>
</section>


<section class="map-section">
  <iframe
    src="https://www.google.com/maps?q=Los+Angeles&output=embed"
    width="100%"
    height="400"
    style="border:0;"
    allowfullscreen=""
    loading="lazy">
  </iframe>
</section>

</main>

<footer class="footer">
  <div class="container">
    <p>2025 Grand Realty. All rights reserved.</p>
  </div>
</footer>

</body>
</html>
