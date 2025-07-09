const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');

console.log('Starting server...');

try {
  // Load environment variables from .env
  dotenv.config();
  console.log('✅ Environment variables loaded');

  // Try to connect to database
  console.log('Attempting to connect to database...');
  const connectDB = require('./config/db');
  connectDB();
  console.log('✅ Database connection initiated');

  // Initialize express app
  const app = express();
  console.log('✅ Express app initialized');

  // Middlewares
  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));
  console.log('✅ Middlewares configured');

  console.log('Loading routes...');

  // Test each route import individually
  try {
    console.log('Loading auth routes...');
    app.use('/api/auth', require('./routes/auth'));
    console.log('✅ Auth routes loaded');
  } catch (error) {
    console.error('❌ Error loading auth routes:', error.message);
  }

  try {
    console.log('Loading profile routes...');
    app.use('/api/profile', require('./routes/profile'));
    console.log('✅ Profile routes loaded');
  } catch (error) {
    console.error('❌ Error loading profile routes:', error.message);
  }

  try {
    console.log('Loading notes routes...');
    app.use('/api/notes', require('./routes/notes'));
    console.log('✅ Notes routes loaded');
  } catch (error) {
    console.error('❌ Error loading notes routes:', error.message);
  }

  try {
    console.log('Loading threads routes...');
    app.use('/api/threads', require('./routes/threads'));
    console.log('✅ Threads routes loaded');
  } catch (error) {
    console.error('❌ Error loading threads routes:', error.message);
  }

  try {
    console.log('Loading posts routes...');
    app.use('/api/posts', require('./routes/posts'));
    console.log('✅ Posts routes loaded');
  } catch (error) {
    console.error('❌ Error loading posts routes:', error.message);
  }

  try {
    console.log('Loading dashboard routes...');
    app.use('/api/dashboard', require('./routes/dashboard'));
    console.log('✅ Dashboard routes loaded');
  } catch (error) {
    console.error('❌ Error loading dashboard routes:', error.message);
  }

  try {
    console.log('Loading upload routes...');
    app.use('/api/upload', require('./routes/upload'));
    console.log('✅ Upload routes loaded');
  } catch (error) {
    console.error('❌ Error loading upload routes:', error.message);
  }

  try {
    console.log('Loading dev routes...');
    app.use('/api/dev', require('./routes/dev'));
    console.log('✅ Dev routes loaded');
  } catch (error) {
    console.error('❌ Error loading dev routes:', error.message);
  }

  // Root test route
  app.get('/', (req, res) => {
    res.send('🎓 Student Hub Backend is Running');
  });

  // Start server
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`🚀 Server successfully running at http://localhost:${PORT}`);
  });

} catch (error) {
  console.error('❌ Fatal error starting server:', error.message);
  console.error('Stack trace:', error.stack);
  process.exit(1);
}
