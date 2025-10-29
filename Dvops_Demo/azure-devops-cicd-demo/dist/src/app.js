"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.app = void 0;
const express_1 = __importDefault(require("express"));
const controllers_1 = require("./controllers");
const app = (0, express_1.default)();
exports.app = app;
const indexController = new controllers_1.IndexController();
// Basic middleware
app.use(express_1.default.json());
app.use(express_1.default.urlencoded({ extended: true }));
// Routes
app.get('/', (req, res) => indexController.getIndex(req, res));
