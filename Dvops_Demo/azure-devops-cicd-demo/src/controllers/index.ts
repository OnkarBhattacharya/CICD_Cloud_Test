export class IndexController {
    public getIndex(req: Request, res: Response): void {
        res.send('Welcome to the CI/CD Demo Application!');
    }

    // Additional route handlers can be added here
}