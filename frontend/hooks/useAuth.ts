/**
 * Custom hook for API calls using React Query.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';

// User types
export interface User {
  id: number;
  email: string;
  username: string;
  isActive: boolean;
  isSuperuser: boolean;
  createdAt: string;
  updatedAt?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

// API functions
export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const response = await apiClient.post('/api/v1/users/login', credentials);
    return response.data;
  },
  
  register: async (data: RegisterData) => {
    const response = await apiClient.post('/api/v1/users/', data);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/v1/users/me');
    return response.data;
  },
};

// React Query hooks
export const useLogin = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      // Store token and update cache
      localStorage.setItem('access_token', data.access_token);
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });
};

export const useRegister = () => {
  return useMutation({
    mutationFn: authApi.register,
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: authApi.getCurrentUser,
    enabled: !!localStorage.getItem('access_token'),
  });
};
