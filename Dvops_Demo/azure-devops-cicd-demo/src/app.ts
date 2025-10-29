import express, { Application } from 'express';
import { IndexController } from './controllers';

const app: Application = express();
const indexController = new IndexController();

// Basic middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => indexController.getIndex(req, res));

export { app };