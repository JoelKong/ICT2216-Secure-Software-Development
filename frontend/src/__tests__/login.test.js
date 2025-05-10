// import React from 'react';
// import { render, screen, fireEvent, waitFor } from '@testing-library/react';
// import '@testing-library/jest-dom';
// import Login from '../Login';

// // Mock the API calls
// jest.mock('../../services/api', () => ({
//   login: jest.fn()
// }));

// import { login } from '../../services/api';

// describe('Login Component', () => {
//   beforeEach(() => {
//     login.mockClear();
//   });

//   test('renders login form', () => {
//     render(<Login />);

//     expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
//     expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
//     expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
//   });

//   test('validates form inputs', async () => {
//     render(<Login />);

//     // Try to submit without values
//     fireEvent.click(screen.getByRole('button', { name: /login/i }));

//     // Check validation errors appear
//     expect(await screen.findByText(/username is required/i)).toBeInTheDocument();
//     expect(await screen.findByText(/password is required/i)).toBeInTheDocument();

//     // API should not be called
//     expect(login).not.toHaveBeenCalled();
//   });

//   test('submits form with valid inputs', async () => {
//     // Mock successful login
//     login.mockResolvedValueOnce({ success: true });

//     render(<Login />);

//     // Fill out the form
//     fireEvent.change(screen.getByLabelText(/username/i), {
//       target: { value: 'testuser' }
//     });

//     fireEvent.change(screen.getByLabelText(/password/i), {
//       target: { value: 'password123' }
//     });

//     // Submit form
//     fireEvent.click(screen.getByRole('button', { name: /login/i }));

//     // API should be called with correct values
//     await waitFor(() => {
//       expect(login).toHaveBeenCalledWith({
//         username: 'testuser',
//         password: 'password123'
//       });
//     });
//   });

//   test('handles login error', async () => {
//     // Mock failed login
//     login.mockRejectedValueOnce({ message: 'Invalid credentials' });

//     render(<Login />);

//     // Fill out the form
//     fireEvent.change(screen.getByLabelText(/username/i), {
//       target: { value: 'testuser' }
//     });

//     fireEvent.change(screen.getByLabelText(/password/i), {
//       target: { value: 'wrongpassword' }
//     });

//     // Submit form
//     fireEvent.click(screen.getByRole('button', { name: /login/i }));

//     // Error message should appear
//     expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
//   });
// });
