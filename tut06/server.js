const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const JWT_SECRET = 'super_secret_key';
const TOKEN_EXPIRY = '1h';

// MySQL config
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '', // default for XAMPP
  database: 'jwt_access_system'
});

db.connect(err => {
  if (err) throw err;
  console.log('✅ MySQL Connected');
});

// Generate JWT
function generateToken(user) {
  return jwt.sign(
    { id: user.id, username: user.username, role: user.role },
    JWT_SECRET,
    { expiresIn: TOKEN_EXPIRY }
  );
}

// Middleware to verify token
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader?.split(' ')[1];
  if (!token) return res.status(401).json({ message: 'Token required' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ message: 'Invalid/Expired token' });
    req.user = user;
    next();
  });
}

// Middleware for role-based access
function authorizeRoles(...roles) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Forbidden: Access denied' });
    }
    next();
  };
}

// Route: Register
app.post('/register', async (req, res) => {
  const { username, password, role } = req.body;

  if (!['admin', 'editor', 'viewer'].includes(role)) {
    return res.status(400).json({ message: 'Invalid role' });
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  db.query(
    'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
    [username, hashedPassword, role],
    (err, result) => {
      if (err) return res.status(500).json({ message: 'User creation failed', error: err });
      res.json({ message: 'User registered successfully' });
    }
  );
});

// Route: Login
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  db.query('SELECT * FROM users WHERE username = ?', [username], async (err, results) => {
    if (err) return res.status(500).json({ message: 'DB error' });
    if (results.length === 0) return res.status(401).json({ message: 'User not found' });

    const user = results[0];
    const validPassword = await bcrypt.compare(password, user.password_hash);

    if (!validPassword) {
      return res.status(401).json({ message: 'Invalid password' });
    }

    const token = generateToken(user);
    res.json({ token });
  });
});

// Route: User Dashboard
app.get('/dashboard', authenticateToken, (req, res) => {
  res.json({ message: `Welcome ${req.user.username} with role ${req.user.role}` });
});

// Route: Admin Access Only
app.get('/admin', authenticateToken, authorizeRoles('admin'), (req, res) => {
  res.json({ message: 'Admin content' });
});

// Route: Editor & Admin
app.get('/editor', authenticateToken, authorizeRoles('admin', 'editor'), (req, res) => {
  res.json({ message: 'Editor content' });
});

// Route: Viewer, Editor, Admin
app.get('/viewer', authenticateToken, authorizeRoles('admin', 'editor', 'viewer'), (req, res) => {
  res.json({ message: 'Viewer content' });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
