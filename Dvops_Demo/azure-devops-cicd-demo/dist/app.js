"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const index_1 = require("./controllers/index");
const app = (0, express_1.default)();
const port = process.env.PORT || 3000;
// Middleware
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
// Routes
const indexController = new index_1.IndexController();
app.get('/', indexController.getIndex.bind(indexController));
// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
