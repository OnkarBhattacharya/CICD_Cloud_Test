import { app } from '../../src/app';
import request from 'supertest';

describe('Integration Tests', () => {
    it('should return welcome message', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
        expect(response.body.message).toBe('Welcome to the CI/CD Demo Application!');
    });
});