# Jason's URL Shortener

Jason's URL Shortener is a simple, efficient, and customizable web-based application for shortening long URLs and managing their expiration time. Built with a FastAPI backend and a static HTML/CSS/JavaScript frontend, this project allows users to create shortened links and set an optional expiration time, after which the link becomes inaccessible.

## Features

- **URL Shortening**: Convert long URLs into shorter, easy-to-share links.
- **Expiration Management**: Set custom expiration times in minutes.
- **URL Redirection**: Redirect users to the original URL when they access the short link.
- **Expiration Check**: Directs expired links to an `expired` page.
- **User-friendly Interface**: Simple form-based UI for input and results.
- **Futuristic Favicon**: Unique and custom-designed icon for branding.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Database**: Redis (for storing and expiring short links)
- **Server**: Nginx (for serving static files and proxying API requests)
- **SSL**: Cloudflare Tunnel for HTTPS support


