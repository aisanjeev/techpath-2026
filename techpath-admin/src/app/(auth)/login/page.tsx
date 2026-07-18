'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import toast from 'react-hot-toast';
import Image from 'next/image';
import { Eye, EyeOff } from 'lucide-react';
import { loginSchema, type LoginFormData } from '@/lib/validations';
import { authService } from '@/services/auth.service';
import { useAuthStore } from '@/store/auth.store';
import { landingPathForRole } from '@/lib/auth/roles';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { FormField } from '@/components/ui/FormField';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    try {
      await authService.login(data.email, data.password);
      // Fetch the TechPath profile immediately so we know the role before redirecting.
      // Trainers go to /trainer; admins go to /dashboard.
      const user = await authService.getCurrentUser();
      login(user);
      router.push(landingPathForRole(user));
    } catch (error) {
      const firebaseError = error as { code?: string };
      const invalidCodes = [
        'auth/invalid-credential',
        'auth/user-not-found',
        'auth/wrong-password',
        'auth/invalid-email',
      ];
      if (firebaseError.code && invalidCodes.includes(firebaseError.code)) {
        toast.error('Invalid email or password');
      } else if (firebaseError.code === 'auth/too-many-requests') {
        toast.error('Too many failed attempts. Please try again later.');
      } else {
        toast.error('Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-teal-50 to-cyan-100 p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4">
            <Image
              src="/logo.png"
              alt="TechPath Logo"
              width={56}
              height={56}
              className="mx-auto"
              priority
            />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">TechPath Admin</h1>
          <p className="mt-1 text-sm text-gray-600">Sign in to your account</p>
        </div>

        <div className="rounded-2xl bg-white p-8 shadow-xl">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <FormField
              label="Email"
              htmlFor="email"
              error={errors.email?.message}
              required
            >
              <Input
                id="email"
                type="email"
                placeholder="admin@techpath.io"
                error={!!errors.email}
                {...register('email')}
              />
            </FormField>

            <FormField
              label="Password"
              htmlFor="password"
              error={errors.password?.message}
              required
            >
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  error={!!errors.password}
                  className="pr-10"
                  {...register('password')}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </FormField>

            <Button type="submit" className="w-full" loading={isLoading}>
              Sign In
            </Button>
          </form>
        </div>

        <p className="mt-6 text-center text-xs text-gray-500">
          TechPath Professional Services © {new Date().getFullYear()}
        </p>
      </div>
    </div>
  );
}
