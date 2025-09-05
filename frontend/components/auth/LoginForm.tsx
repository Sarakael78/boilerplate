"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface LoginFormProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export default function LoginForm({ onSuccess, onError }: LoginFormProps) {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const { login } = useAuth();
  const router = useRouter();

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setErrors({});

    try {
      await login(formData.username, formData.password);
      onSuccess?.();
      router.push("/dashboard");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Login failed";
      setErrors({ general: errorMessage });
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  return (
    <div className="bg-card mx-auto max-w-md rounded-lg border p-6 shadow-md">
      <h2 className="text-card-foreground mb-6 text-center text-2xl font-bold">
        Sign In
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {errors.general && (
          <div className="border-destructive/50 bg-destructive/10 text-destructive rounded border px-4 py-3">
            {errors.general}
          </div>
        )}

        <div className="space-y-2">
          <label
            htmlFor="username"
            className="text-foreground text-sm font-medium"
          >
            Username
          </label>
          <Input
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
            disabled={isLoading}
            className={errors.username ? "border-destructive" : ""}
          />
          {errors.username && (
            <p className="text-destructive text-sm">{errors.username}</p>
          )}
        </div>

        <div className="space-y-2">
          <label
            htmlFor="password"
            className="text-foreground text-sm font-medium"
          >
            Password
          </label>
          <Input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            disabled={isLoading}
            className={errors.password ? "border-destructive" : ""}
          />
          {errors.password && (
            <p className="text-destructive text-sm">{errors.password}</p>
          )}
        </div>

        <Button type="submit" disabled={isLoading} className="w-full">
          {isLoading ? "Signing in..." : "Sign In"}
        </Button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-muted-foreground text-sm">
          Don't have an account?{" "}
          <Button
            variant="link"
            className="h-auto p-0 font-medium"
            onClick={() => router.push("/register")}
          >
            Sign up
          </Button>
        </p>
      </div>
    </div>
  );
}
