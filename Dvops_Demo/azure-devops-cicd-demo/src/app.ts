import express from 'express';
import { IndexController } from './controllers/index';

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
const indexController = new IndexController();
app.get('/', indexController.getIndex.bind(indexController));

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});