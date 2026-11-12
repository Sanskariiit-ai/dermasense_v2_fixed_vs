/** The browser talks to /api; Next forwards it to the backend so no CORS setup is needed in development. */
module.exports = {
  output: 'standalone',
     async rewrites() {
       return [{ source: '/api/:path*', destination: 'http://localhost:8000/api/:path*' }]
     },
}
