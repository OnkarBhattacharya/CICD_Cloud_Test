import request from 'supertest';
import app from '../../src/app';

describe('Integration Tests', () => {
    it('should return 200 for the root route', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('message', 'Welcome to the API!');
    });

    it('should return 404 for non-existing routes', async () => {
        const response = await request(app).get('/non-existing-route');
        expect(response.status).toBe(404);
    });

    // Add more integration tests as needed
});