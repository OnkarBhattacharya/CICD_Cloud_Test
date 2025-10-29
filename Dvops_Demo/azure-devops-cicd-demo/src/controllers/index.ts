import { Request, Response } from 'express';

export class IndexController {
    public getIndex(req: Request, res: Response): void {
        res.status(200).json({ message: 'Welcome to the CI/CD Demo Application!' });
    }
}