"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IndexController = void 0;
class IndexController {
    getIndex(req, res) {
        res.status(200).json({ message: 'Welcome to the CI/CD Demo Application!' });
    }
}
exports.IndexController = IndexController;
