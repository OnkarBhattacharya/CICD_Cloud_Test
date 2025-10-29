import request from 'supertest';
import app from '../../src/app';

describe('App', () => {
    it('should respond with a 200 status for the root route', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
    });

    it('should respond with JSON for the root route', async () => {
        const response = await request(app).get('/');
        expect(response.headers['content-type']).toEqual(expect.stringContaining('json'));
    });

    it('should return the expected response for the root route', async () => {
        const response = await request(app).get('/');
        expect(response.body).toEqual({ message: 'Welcome to the API!' });
    });
});